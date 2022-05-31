const mongoose = require('mongoose')

const discordlostarkSchema = new mongoose.Schema({
    question: String,
    answer: String,
    choices: [String],
}, {collection: 'quiz-lost ark'})

module.exports = mongoose.model('discord-lostark', discordlostarkSchema, 'quiz-lost ark');
