const mongoose = require('mongoose')

const discordcsgoSchema = new mongoose.Schema({
    question: String,
    name: String,
    answer: String,
    choices: [String],
}, {collection: 'quiz-csgo'})

module.exports = mongoose.model('discord-csgo', discordcsgoSchema, 'quiz-csgo');

