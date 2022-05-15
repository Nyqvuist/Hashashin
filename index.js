require('dotenv').config();
const fetch = require('cross-fetch');
const mongoose = require('mongoose');
const { Client, Intents } = require('discord.js');
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const DB = process.env.DB;
const STEAM = process.env.STEAM_KEY;
const Games = require('./Schemas/Games');


/* Future Implementation.
// Making a DB connection.
mongoose.connect(DB, () => {
    console.log('DB is connected.')
})

function db_update() {
    games = []
    fetch(`https://api.steampowered.com/IStoreService/GetAppList/v1/?key=${STEAM}&include_games=true&include_dlc=false&include_software=false&include_videos=false&include_hardware=false&max_results=50000`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
        });

};

db_update()
*/


// Create a new client instance
const client = new Client({intents: [Intents.FLAGS.GUILDS] });


// Ready check for the client
client.once('ready', () => {
    console.log('Ready!');
});

// Login to Discord with the client token.
client.login(DISCORD_TOKEN);