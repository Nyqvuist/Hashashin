const { SlashCommandBuilder } = require('@discordjs/builders');
const fuzzysort = require('fuzzysort');
const axios = require('axios');
const { MessageEmbed, Message } = require('discord.js');
const Tokenizer = require('sentence-tokenizer');
var _ = require('lodash');

// Creating Slash commands
module.exports = {
    data: new SlashCommandBuilder()
        .setName('pokemon')
        .setDescription('Pokemon Commands')
        .addSubcommand(subcommand =>
            subcommand
                .setName('route')
                .setDescription('Search for pokemon in a game.')
                .addStringOption(option =>
                    option.setName('version')
                    .setDescription('The game version')
                    .setRequired(true)
                    )
                .addStringOption(option =>
                    option.setName('pokemon')
                    .setDescription('The specified pokemon.')
                    .setRequired(true)
                    ) 
            ),
    async execute(interaction) {
        if(interaction.options.getSubcommand() === 'route'){
            const version = interaction.options.getString('version')
            const pokemon = interaction.options.getString('pokemon')
            let embed = await pokemonRoute(pokemon, version);
            await interaction.reply({embeds: [embed]});
        }
    }
}


async function pokemonRoute(pokemon, version){

    const possibilities = ['red','blue','diamond','pearl','platinum','yellow','gold','silver','crystal','firered','leafgreen','heartgold','soulsilver','ruby','sapphire','emerald','x','y','omega-ruby','alpha-sapphire','black','white']

    let matches = fuzzysort.go(version.toLowerCase(), possibilities, {
		limit: 1,
	})

    let pokemondata = await axios.get(`https://pokeapi.co/api/v2/pokemon/${pokemon.toLowerCase()}/encounters`)

    if(pokemondata.data.length === 0){
        const routeEmbed = new MessageEmbed()
            .setColor('RANDOM')
            .setTitle('This pokemon cannot be found in wild grass.')
        return routeEmbed

    } else {
        let vlist = []
        let dlist = []
        pokemondata = pokemondata.data

        for(x in pokemondata) {
            let version_data = pokemondata[x].version_details[0]
            if(version_data.version.name === matches[0].target.toLowerCase()){
                vlist.push(pokemondata[x])
            }else {
                if(version_data.version.name){
                    dlist.push(version_data.version.name)
                }
            }
        };

        dlist = new Set(dlist)
        dlist = Array.from(dlist)
        
        if(vlist.length > 0){
            let pokemon_name = _.upperFirst(pokemon)
            let str = _.upperFirst(matches[0].target.toLowerCase())
            const routeEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(pokemon_name + ' Routes ' + '- Version: ' + str)

            for(y in vlist){
                let version_data = vlist[y]['version_details'][0]
                let name = vlist[y]['location_area']['name']
                name = name.replaceAll('-', ' ')
                routeEmbed.addField(name, 'Encounter Potential: ' + String(version_data.max_chance) + '%', false)
            }

            return routeEmbed

        } else if(vlist.length === 0 && dlist.length > 0){
            let pokemon_name = _.upperFirst(pokemon)
            const routeEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(pokemon_name + ' can be found in these versions!')

                for(x in dlist){
                    routeEmbed.addField(dlist[x], '\u200b', false)
                }
            return routeEmbed
        }
    }
};