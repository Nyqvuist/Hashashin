const { SlashCommandBuilder } = require('@discordjs/builders');
const axios = require('axios');
const { MessageEmbed, Message } = require('discord.js');
const mongoose = require('mongoose');
const Discordcsgo = require('../Schemas/discord-csgo');
const wait = require('node:timers/promises').setTimeout;
const Discordlostark = require('../Schemas/discord-lostark');


module.exports = {
    data: new SlashCommandBuilder()
        .setName('quiz')
        .setDescription('Create a quiz question')
        .addStringOption(option =>
            option.setName('category')
                .setDescription('The quiz category')
                .setRequired(true)
                .addChoices(
                    {name: 'csgo', value: 'csgo quiz'},
                    {name: 'lost ark', value: 'LA_quiz'},
                    {name: 'league of legends', value: 'LOL_quiz'},
                )),
    async execute(interaction) {
        if(interaction.options.getString('category') === 'csgo quiz'){
            const embed = await csgoQuiz()
            const message = await interaction.reply({embeds: [embed[0]], fetchReply: true})
            message.react('1️⃣')
                .then(() => message.react('2️⃣'))
                .then(() => message.react('3️⃣'))
                .then(() => message.react('4️⃣'))
            await wait(50000)
            const edit = await embedEdit(embed[1], embed[2], embed[3], embed[4])
            await interaction.editReply({embeds:[edit]})
        } else if(interaction.options.getString('category') === 'LA_quiz') {
            const embed = await lostarkQuiz()
            const message = await interaction.reply({embeds: [embed[0]], fetchReply: true})
            message.react('1️⃣')
                .then(() => message.react('2️⃣'))
                .then(() => message.react('3️⃣'))
                .then(() => message.react('4️⃣'))
            await wait(50000)
            const edit = await lostarkEdit(embed[1], embed[2], embed[3])
            await interaction.editReply({embeds:[edit]})
        }
    }
}

// CSGO Quiz Function
async function csgoQuiz() {
    const quiz = await Discordcsgo.aggregate([{$sample: {size:1}}])
    const shuffled = quiz[0].choices.sort(() => 0.5 - Math.random());
    let choices = shuffled.slice(0,3)
    let answer = quiz[0].answer
    let question = quiz[0].question
    let name = quiz[0].name
    choices.push(quiz[0].answer)
    const shuffle = choices.sort(() => 0.5 - Math.random());
    
    const quizEmbed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(question)
        .setDescription(name)
        .addFields({name:shuffle[0] + '\n' + shuffle[1] + '\n' + shuffle[2] + '\n' + shuffle[3],value: '\u200B',inline: false})
        .setTimestamp()
        .setFooter({text: 'CSGO Quiz'})

    return [quizEmbed,question,name,answer,shuffle]
    }
   
// Lost Ark Quiz Function
async function lostarkQuiz() {
    const quiz = await Discordlostark.aggregate([{$sample: {size:1}}])
    const shuffled = quiz[0].choices.sort(() => 0.5 - Math.random());
    let choices = shuffled.slice(0,3)
    let answer = quiz[0].answer
    let question = quiz[0].question
    choices.push(quiz[0].answer)
    const shuffle = choices.sort(() => 0.5 - Math.random());
    
    const quizEmbed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(question)
        .addFields({name:shuffle[0] + '\n' + shuffle[1] + '\n' + shuffle[2] + '\n' + shuffle[3],value: '\u200B',inline: false})
        .setTimestamp()
        .setFooter({text: 'Lost Ark Quiz'})

    return [quizEmbed,question,answer,shuffle]
}

async function embedEdit(question,name,answer,shuffle) {
    
    for(x in shuffle){
        if(shuffle[x] ===  answer){
            const concat = shuffle[x].concat(' ', ':white_check_mark:')
            shuffle.splice(x,1,concat)
        }  
    }
    const editedEmbed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(question)
        .setDescription(name)
        .addFields({name:shuffle[0] + '\n' + shuffle[1] + '\n' + shuffle[2] + '\n' + shuffle[3],value:'\u200B',inline: false})
        .setTimestamp()
        .setFooter({text: 'CSGO Quiz'})

    return editedEmbed

}


async function lostarkEdit(question,answer,shuffle) {
    for(x in shuffle){
        if(shuffle[x] ===  answer){
            const concat = shuffle[x].concat(' ', ':white_check_mark:')
            shuffle.splice(x,1,concat)
        }  
    }
    
    const editedEmbed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(question)
        .addFields({name:shuffle[0] + '\n' + shuffle[1] + '\n' + shuffle[2] + '\n' + shuffle[3],value: '\u200B',inline: false})
        .setTimestamp()
        .setFooter({text: 'Lost Ark Quiz'})

    return editedEmbed

}

