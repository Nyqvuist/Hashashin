const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Message } = require('discord.js');
const Osrsschema = require('../Schemas/discord-osrs');
const axios = require('axios');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('osrs')
        .setDescription('osrs commands')
        .addSubcommand(subcommand =>
            subcommand
                .setName('item')
                .setDescription('Look up GE prices and relevant info for an item.')
                .addStringOption(option =>
                    option.setName('name')
                    .setDescription('Name of item')
                    .setRequired(false)
                    )
                .addIntegerOption(option =>
                    option.setName('id')
                    .setDescription('item id of an item.')
                    .setRequired(false)
                    )
                ),
    async execute(interaction) {
        if(interaction.options.getSubcommand() === 'item'){
            const name = interaction.options.getString('name')
            const id = interaction.options.getInteger('id')

            if(name != null || undefined){
                let embed = await nameEmbed(name)
                await interaction.reply({embeds: [embed]}); 
            } else if(id != null || undefined){
                let embed = await idEmbed(id)
                await interaction.reply({embeds: [embed]})
            } else {
                await interaction.reply('Please enter a name or item id.')
            }

        }

    }
};

async function nameEmbed(itemName){
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
      }

    function replaceSpace(string){
        return string.replace(/\s/g,'_')
    }
    
    itemName = capitalizeFirstLetter(itemName.toLowerCase())
    try {
        const db = await Osrsschema.findOne({name: `${itemName}`})
        const dbId = db.id

        const resp = await axios.get(`https://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=${dbId}`)
        const itemData = resp.data.item

        const osrsEmbed = new MessageEmbed()
            .setColor('RANDOM')
            .setURL(`https://oldschool.runescape.wiki/w/${replaceSpace(itemName)}`)
            .setTitle(itemName)
            .setDescription(itemData.description)
            .setThumbnail(itemData.icon)
            .setTimestamp()
                        
            .addFields({name:'Item ID: ',value: itemData.id.toString(), inline: true})
            .addFields({name:'Current Price: ', value: itemData.current.price.toString(), inline: true})
            .addFields({name: `Today's Price Trend: `, value: itemData.today.trend + ' by ' + itemData.today.price.toString(), inline: true})
            if(itemData.members == 'true'){
                osrsEmbed.addFields({name: 'Member Item? ', value:':white_check_mark:', inline: true})
            } else {
                osrsEmbed.addFields({name: 'Member Item? ', value:':x:',inline: true})
            }
        return osrsEmbed
    } catch (e){
        if(e instanceof TypeError){
            const failEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(`The item ${itemName} was not found, please make sure it is spelled correctly.`)

            return failEmbed
        }
    }
}
        

async function idEmbed(id){
    function replaceSpace(string){
        return string.replace(/\s/g,'_')
    }

    try {
        const resp = await axios.get(`https://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=${id}`)
        const itemData = resp.data.item
        const osrsEmbed = new MessageEmbed()
            .setColor('RANDOM')
            .setURL(`https://oldschool.runescape.wiki/w/${replaceSpace(itemData.name)}`)
            .setTitle(itemData.name)
            .setDescription(itemData.description)
            .setThumbnail(itemData.icon)
            .setTimestamp()
                        
            .addFields({name:'Item ID: ',value: itemData.id.toString(), inline: true})
            .addFields({name:'Current Price: ', value: itemData.current.price.toString(), inline: true})
            .addFields({name: `Today's Price Trend: `, value: itemData.today.trend + ' by ' + itemData.today.price.toString(), inline: true})
            if(itemData.members == 'true'){
                osrsEmbed.addFields({name: 'Member Item? ', value:':white_check_mark:', inline: true})
            } else {
                osrsEmbed.addFields({name: 'Member Item? ', value:':x:',inline: true})
            }
        return osrsEmbed
    } catch (err) {
        if(err.response) {
            const failEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(`The item id of ${id} was not found, please make sure you entered the proper item id.`)

            return failEmbed
        }
    }
}