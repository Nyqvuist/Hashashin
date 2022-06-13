const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Message } = require('discord.js');



// Expand this command to fit all cases.
module.exports = {
    data: new SlashCommandBuilder()
        .setName('reactionroles')
        .setDescription('Set up a message for users to obtain a role based off of reaction. (Need to be guild owner.)')
        .addStringOption(option =>
            option.setName('title')
                .setDescription('The title for the embed.')
                .setRequired(true))
        .addStringOption(option =>
            option.setName('description')
                .setDescription('Description for embed.')
                .setRequired(true))
        .addChannelOption(option =>
            option.setName('channel')
                .setDescription('Chosen channel for the message.')
                .setRequired(true)),

    async execute(interaction) {
        if(interaction.commandName === 'reactionroles') {
            const title = interaction.options.getString('title')
            const desc = interaction.options.getString('description')
            const channel = interaction.options.getChannel('channel')
            const warriorRole = interaction.guild.roles.cache.find(role => role.name === 'Warriors')
            const assassinRole = interaction.guild.roles.cache.find(role => role.name === 'Assassins')
            const mageRole = interaction.guild.roles.cache.find(role => role.name === 'Mages')
            const martialRole = interaction.guild.roles.cache.find(role => role.name === 'Martial Artists')
            const gunnerRole = interaction.guild.roles.cache.find(role => role.name === 'Gunners')
            
            const roleEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(title)
                .setDescription(desc)
                .setFooter({text: 'Role Acquisition'})
            
            
            await interaction.reply('The reaction role message has been created.')
            const message = await channel.send({ embeds: [roleEmbed], fetchReply: true });
            const client = interaction.client
            const warriorEmoji = message.guild.emojis.cache.find(emoji => emoji.name === 'warrior')
            const assassinEmoji = message.guild.emojis.cache.find(emoji => emoji.name === 'assassin')
            const mageEmoji = message.guild.emojis.cache.find(emoji => emoji.name === 'mage')
            const martialEmoji = message.guild.emojis.cache.find(emoji => emoji.name === 'martialartist')
            const gunnerEmoji = message.guild.emojis.cache.find(emoji => emoji.name === 'gunner')
            message.react(warriorEmoji);
            message.react(assassinEmoji);
            message.react(mageEmoji);
            message.react(martialEmoji);
            message.react(gunnerEmoji);

            client.on('messageReactionAdd', async (reaction, user) => {
                if(reaction.message.partial) await reaction.message.fetch();
                if(reaction.partial) await reaction.fetch();
                if(user.bot) return;
                if(!reaction.message.guild) return;
            
                if(reaction.message.channel.id === channel.id) {
                    if(reaction.emoji.name === warriorEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.add(warriorRole)
                    }
                    if(reaction.emoji.name === assassinEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.add(assassinRole)
                    } 
                    if(reaction.emoji.name === mageEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.add(mageRole)
                    } 
                    if(reaction.emoji.name === martialEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.add(martialRole)
                    } 
                    if(reaction.emoji.name === gunnerEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.add(gunnerRole)
                    }   
                }  else {
                    return;
                }
            });
            
            client.on('messageReactionRemove', async (reaction, user) => {
                if(reaction.message.partial) await reaction.message.fetch();
                if(reaction.partial) await reaction.fetch();
                if(user.bot) return;
                if(!reaction.message.guild) return;
            
                if(reaction.message.channel.id === channel.id) {
                    if(reaction.emoji.name === warriorEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.remove(warriorRole)
                    }
                    if(reaction.emoji.name === assassinEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.remove(assassinRole)
                    } 
                    if(reaction.emoji.name === mageEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.remove(mageRole)
                    } 
                    if(reaction.emoji.name === martialEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.remove(martialRole)
                    } 
                    if(reaction.emoji.name === gunnerEmoji.name) {
                        await reaction.message.guild.members.cache.get(user.id).roles.remove(gunnerRole)
                    }   
                }  else {
                    return;
                }
            });
        }
    }
}
