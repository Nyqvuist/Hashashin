const { SlashCommandBuilder } = require('@discordjs/builders');
const axios = require('axios');
const { MessageEmbed, Message } = require('discord.js');
const mongoose = require('mongoose');
const Discordcsgo = require('../Schemas/discord-csgo')


module.exports = {
    data: new SlashCommandBuilder()
        .setName('quiz')
        .setDescription('Create a quiz question')
        .addStringOption(option =>
            option.setName('category')
                .setDescription('The quiz category')
                .setRequired(true)
                .addChoices(
                    {name: 'csgo', value: 'csgo_quiz'},
                    {name: 'lost ark', value: 'LA_quiz'},
                    {name: 'league of legends', value: 'LOL_quiz'},
                )),
    async execute(interaction) {
        if(interaction.options.getString('category') === 'csgo_quiz'){
            await csgoQuiz()
            await interaction.reply('Luhmao')
        } else {
            await interaction.reply('uh oh')
        }
    }
}




async function csgoQuiz() {
    const quiz = await Discordcsgo.aggregate([{$sample: {size:1}}])
    const shuffled = quiz[0].choices.sort(() => 0.5 - Math.random());
    let choices = shuffled.slice(0,3)
    choices.push(quiz[0].answer)
    
    const quizEmbed = new MessageEmbed()
        .setColor('RANDOM')
        .setTitle(quiz[0].question)
        .setDescription(quiz[0].name)
        .addField
}


// Create another function that passes embed object and answer to cross check answer.