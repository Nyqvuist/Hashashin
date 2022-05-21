const { SlashCommandBuilder } = require('@discordjs/builders');
const fuzzysort = require('fuzzysort');
const axios = require('axios');
const { MessageEmbed } = require('discord.js');
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
			),
	async execute(interaction) {
		if(interaction.options.getSubcommand() === 'search'){
			const game = interaction.options.getString('game')
			let embed = await gameEmbed(game);
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
	})
	for(var y in gdata) {
		if(matches[0].target.toLowerCase() == gdata[y].name.toLowerCase()) {
			app.push(gdata[y])
		}
	}
	
	let appID = app[0].appid.toString()
	let name = app[0].name

	return [appID, name]
}


// Creating an Embed object function
async function gameEmbed(game) {

	let results = await steamSearch(game);

	let appID = results[0]

	const resp = await axios.get(`https://store.steampowered.com/api/appdetails/?appids=${appID}&l=english`)

	const response = await axios.get(`https://store.steampowered.com/appreviews/${appID}?json=1`)

	let reviews = response.data

	const reg = /<.*?>/ig
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
			let sentences = tokenizer.getSentences().join(' ')
			notice = cleanHtml(sentences)
			gameEmbed.setFooter({text: notice})
		}
		
		// Adding multiple devs
		for(dev in appdetails.developers) {
			devs.push(appdetails.developers[dev])
		};
		let developer = devs.join(', ')
		gameEmbed.addField('Developers: ', developer, true)

		// Price check for games

		let price = appdetails.price_overview

		if(appdetails.is_free === true) {
			gameEmbed.addField('Price: ', 'Free', true)
		}
		else if(appdetails.release_date.coming_soon === true) {
			gameEmbed.addField('Price: ', 'Coming Soon', true)
		}
		else if(price.initial_formatted != '') {
			gameEmbed.addField('Price: ', `~~${price.initial_formatted}~~` + ' ' + `**${price.final_formatted}**`, true)
		}
		else {
			gameEmbed.addField('Price: ', price.final_formatted, true)
		};

		// Adding Reviews
		gameEmbed.addField('Review: ', reviews.query_summary.review_score_desc, true)
		

	return gameEmbed

}
