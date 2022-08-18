const { SlashCommandBuilder } = require('@discordjs/builders');
const fuzzysort = require('fuzzysort');
const axios = require('axios');
const { MessageEmbed, Message } = require('discord.js');
const Tokenizer = require('sentence-tokenizer');


// Creating Slash Commands
module.exports = {
	data: new SlashCommandBuilder()
		.setName('steam')
		.setDescription('Steam Commands.')
		.addSubcommand(subcommand =>
			subcommand
				.setName('search')
				.setDescription('Search for a game.')
				.addStringOption(option => 
					option.setName('game')
					.setDescription('The name of game.')
					.setRequired(true))
			)
		.addSubcommand(subcommand =>
			subcommand
				.setName('update')
				.setDescription('Game Updates')
				.addStringOption(option => 
					option.setName('game')
					.setDescription('The name of game.')
					.setRequired(true))
			)
		.addSubcommand(subcommand =>
			subcommand
				.setName('count')
				.setDescription('Player count for a game.')
				.addStringOption(option => 
					option.setName('game')
					.setDescription('The name of game.')
					.setRequired(true))
			),
	async execute(interaction) {
		if(interaction.options.getSubcommand() === 'search'){
			const game = interaction.options.getString('game')
			try {
				let embed = await gameEmbed(game);
				await interaction.reply({embeds: [embed]});
			} catch (e) {
				if(e instanceof TypeError) {
					await interaction.reply(
						'Please double check the spelling of the game. Special characters will need to be added.')
				}
			}
		} else if(interaction.options.getSubcommand() === 'update'){
			const game = interaction.options.getString('game')
			let embed = await gameUpdate(game);
			await interaction.reply({embeds: [embed]});
		} else if(interaction.options.getSubcommand() === 'count'){
			const game = interaction.options.getString('game')
			let embed = await playerCount(game);
			await interaction.reply({embeds: [embed]});
		}
	},
};




// Steam Search Function to pull appID
async function steamSearch(game) {
    const resp = await axios.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/");
    let gdata = resp.data.applist.apps
	let glist=[];
	let app=[];
	for(var x in gdata){
		if(gdata[x].name) {
			glist.push(gdata[x].name)
		}
	}
	let matches = fuzzysort.go(game, glist, {
		limit: 1,
		threshold: 0,
	})
	
	for(var y in gdata) {
		if(matches[0].target.toLowerCase() == gdata[y].name.toLowerCase()) {
			app.push(gdata[y])
		}
	}
	
	let appID = app[0].appid.toString()
	let name = app[0].name

	return [appID, name]
};


// Creating an Embed object function
async function gameEmbed(game) {

	let results = await steamSearch(game);

	let appID = results[0]

	const resp = await axios.get(`https://store.steampowered.com/api/appdetails/?appids=${appID}&l=english`)

	const response = await axios.get(`https://store.steampowered.com/appreviews/${appID}?json=1`)

	let reviews = response.data

	const reg1 = /<.+>/ig

	let devs = [];

	var tokenizer = new Tokenizer('Test');

	function cleanHtml(raw_html) {
		let cleanText = raw_html.replace(reg1, ' ')
		return cleanText
	}

	let appdetails = resp.data[`${appID}`].data
	let description = appdetails.short_description
	
	const gameEmbed =  new MessageEmbed() 
		.setColor('RANDOM')
		.setTitle(appdetails.name)
		.setURL(`https://store.steampowered.com/app/${appID}/`)
		.setImage(appdetails.header_image)
		.setDescription(cleanHtml(description))


		// Checking if legal notice is present.
		if(appdetails.legal_notice === undefined || appdetails.legal_notice === null) {
			gameEmbed.setFooter({text:''})

		}
		else {
			let notice = appdetails.legal_notice
			tokenizer.setEntry(notice)
			let sentences = tokenizer.getSentences()
			sentences = sentences.slice(0,2).join(' ')
			notice = cleanHtml(sentences)
			gameEmbed.setFooter({text: notice})
		}
		
		// Adding multiple devs
		for(dev in appdetails.developers) {
			devs.push(appdetails.developers[dev])
		};
		let developer = devs.join(', ')
		gameEmbed.addFields('Developers: ', developer, true)

		// Price check for games

		let price = appdetails.price_overview

		if(appdetails.is_free === true) {
			gameEmbed.addFields('Price: ', 'Free', true)
		}
		else if(appdetails.release_date.coming_soon === true) {
			gameEmbed.addFields('Price: ', 'Coming Soon', true)
		}
		else if(price.initial_formatted != '') {
			gameEmbed.addFields('Price: ', `~~${price.initial_formatted}~~` + ' ' + `**${price.final_formatted}**`, true)
		}
		else {
			gameEmbed.addFields('Price: ', price.final_formatted, true)
		};

		// Adding Reviews
		gameEmbed.addFields('Review: ', reviews.query_summary.review_score_desc, true)
		

	return gameEmbed

};


// Game Update Logic
async function gameUpdate(game) {

	let results = await steamSearch(game);

	let appID = results[0]

	const resp = await axios.get(`https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=${appID}`)
	const response = await axios.get(`https://store.steampowered.com/api/appdetails/?appids=${appID}&l=english`)
	
	let appdetails = response.data[`${appID}`].data

	const reg = /<.*?>|\[.*?\]|\{.*?\}|\[img\].+\[img\]/ig

	var tokenizer = new Tokenizer('Test');

	function cleanHtml(raw_html) {
		let cleanText = raw_html.replace(reg, '')
		return cleanText
	}

	let items = resp.data.appnews.newsitems
	let item =[];

	for(x in items) {
		if(items[x].feedlabel === 'Community Announcements') {
			item.push(items[x])
		}
	};

	tokenizer.setEntry(item[0].contents)
	let sentences = tokenizer.getSentences()
	sentences = sentences.slice(0,3).join(' ')

	let contents = cleanHtml(sentences)
	
	let url = item[0].url
	url = url.replace(' ', '')

	const updateEmbed = new MessageEmbed()
		.setColor('RANDOM')
		.setTitle(item[0].title)
		.setURL(url)
		.setDescription(contents)
		.setThumbnail(appdetails.header_image)

		let date_time = item[0].date

		let date = new Date(date_time*1000).toLocaleDateString('en-US')

		updateEmbed.addFields('Date: ', date, true)

		if(item[0].author != ''){
			updateEmbed.addFields('Author: ', item[0].author, true)
		} else {
			
		}

		updateEmbed.setFooter({text:item[0].feedlabel})

	return updateEmbed

}

// Game player count logic
async function playerCount(game){

	let results = await steamSearch(game);

	let appID = results[0]
	let name = results[1]

	gsdata = await axios.get(`https://store.steampowered.com/api/appdetails/?appids=${appID}&l=english`)
	codata = await axios.get(`https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=${appID}`)

	let check = codata.data.response

	if(check.player_count === undefined){
		await interaction.reply('This game currently does not have players online.')

	} else {
		let player_count = check.player_count
		let appdetails = gsdata.data[`${appID}`].data

		const playerEmbed = new MessageEmbed()
			.setColor('RANDOM')
			.setTitle(name)
			.setDescription('There are currently ' + `**${player_count}**` + ' playing.')
			.setThumbnail(appdetails.header_image)
		
			return playerEmbed
	}

}