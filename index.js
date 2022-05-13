require('dotenv').config()
const { Client, Intents } = require('discord.js');
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;

// Create a new client instance
const client = new Client({intents: [Intents.FLAGS.GUILDS] });


// Ready check for the client
client.once('ready', () => {
    console.log('Ready!');
});

// Login to Discord with the client token.
client.login(DISCORD_TOKEN);