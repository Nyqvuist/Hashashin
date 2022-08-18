const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, Message } = require('discord.js');
const Discordmeme = require('../Schemas/destiny2-meme');


module.exports = {
    data: new SlashCommandBuilder()
        .setName('destiny2')
        .setDescription('Destiny 2 Commands')
        .addSubcommand(subcommand =>
            subcommand
                .setName('organize')
                .setDescription('Organize a raid.')
                .addRoleOption(option => 
                    option.setName('mention')
                    .setDescription('The role to mention.')
                    .setRequired(true)
                    )
                .addStringOption(option =>
                    option.setName('raid1')
                    .setDescription('The name of the raid')
                    .setRequired(true)
                    )
                .addStringOption(option =>
                    option.setName('raid2')
                    .setDescription('The name of the raid')
                    .setRequired(false)
                    )
                .addStringOption(option =>
                    option.setName('raid3')
                    .setDescription('The name of the raid')
                    .setRequired(false)
                    )
                .addStringOption(option =>
                    option.setName('raid4')
                    .setDescription('The name of the raid')
                    .setRequired(false)
                    )
                
                .addStringOption(option =>
                    option.setName('message')
                    .setDescription('Optional message to add to the tag.')
                    .setRequired(false))
            ),
    async execute(interaction) {
        if(interaction.options.getSubcommand() === 'organize'){
            const raid1 = interaction.options.getString('raid1')
            const raid2 = interaction.options.getString('raid2')
            const raid3 = interaction.options.getString('raid3')
            const raid4 = interaction.options.getString('raid4')
            const role = interaction.options.getRole('mention')
            const description = interaction.options.getString('message')
            const meme = await Discordmeme.aggregate([{$sample: {size:1}}])

            console.log(meme[0].pic)

            let args = [raid1, raid2, raid3, raid4];

            for(var x = 0; x < args.length; x++){
                if(args[x] === null || undefined){
                    args.splice(x,4)
                }
            }

            const raidEmbed = new MessageEmbed()
                .setColor('RANDOM')
                .setTitle(interaction.user.username + ' is calling for a raid!')
                .setImage(meme[0].pic)
                if(description != null){
                    raidEmbed.setDescription(description)
                }
                for(var x = 0; x < args.length; x++){
                    raidEmbed.addField(args[x],'\u200b', false)
                }
                raidEmbed.setTimestamp()
                raidEmbed.setFooter({text: 'Raid Organizer'})
            
            const message = await interaction.reply({content:`${role}`, embeds:[raidEmbed], fetchReply: true})
            if(args.length === 1){
                message.react('1️⃣')
            } else if(args.length === 2){
                message.react('1️⃣')
                    .then(() => message.react('2️⃣'))
            } else if(args.length === 3){
                message.react('1️⃣')
                    .then(() => message.react('2️⃣'))
                    .then(() => message.react('3️⃣'))
            } else if(args.length === 4){
                message.react('1️⃣')
                    .then(() => message.react('2️⃣'))
                    .then(() => message.react('3️⃣'))
                    .then(() => message.react('4️⃣'))
            };
        } else {
            await interaction.reply('omegalul')
        }
    }
                
};