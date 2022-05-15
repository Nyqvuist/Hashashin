const mongoose = require('mongoose')

const steamSchema = new mongoose.Schema({
    appid: Number,
    name: String,
    last_modified: Number,
    price_change_number: Number,
    have_more_results: Boolean,
    last_appid: Number
}, {collection: "steam-games"})

const Games = module.exports = mongoose.model("Games", steamSchema, "steam-games");