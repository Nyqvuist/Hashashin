const mongoose = require('mongoose')

const osrsSchema = new mongoose.Schema({
    id: Number,
    name: String
}, {collection: 'osrs'})

module.exports = mongoose.model('discord-osrs', osrsSchema, 'osrs');
