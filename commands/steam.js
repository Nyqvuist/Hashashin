const { SlashCommandBuilder } = require('@discordjs/builders');
const fuzzysort = require('fuzzysort');
const axios = require('axios');
const { MessageEmbed } = require('discord.js');

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
			let results = await steamSearch(game);
			await gameEmbed(results[0]);
			await interaction.reply(`Is ${results[1]} the game you searched for?`);
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


// Creating an Embed object
async function gameEmbed(appID) {
	const resp = await axios.get(`https://store.steampowered.com/api/appdetails/?appids=${appID}&l=english`)
	
	const reg = '<.*?>'

	const response = await axios.get(`https://store.steampowered.com/appreviews/${appID}?json=1`)

	let appdata = resp.data[`${appID}`].data
	let description;


}
