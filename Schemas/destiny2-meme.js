const mongoose = require('mongoose')

const discordmemeSchema = new mongoose.Schema({
    pic: String,
}, {collection: 'destiny2meme'})

module.exports = mongoose.model('destiny2-meme', discordmemeSchema, 'destiny2meme');
