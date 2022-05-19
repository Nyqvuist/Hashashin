require('dotenv').config();
const fs = require('node:fs');
const path = require('node:path');
// const fetch = require('cross-fetch');
// const mongoose = require('mongoose');
const { Client, Intents, Collection } = require('discord.js');
const token = process.env.DISCORD_TOKEN;
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

client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const filePath = path.join(commandsPath, file);
	const command = require(filePath);
	// Set a new item in the Collection
	// With the key as the command name and the value as the exported module
	client.commands.set(command.data.name, command);
}

client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;

	const command = client.commands.get(interaction.commandName);

	if (!command) return;

	try {
		await command.execute(interaction);
	} catch (error) {
		console.error(error);
		await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
	}
});

// Ready check for the client
client.once('ready', () => {
    console.log('Hashashin is online!');
});

// Login to Discord with the client token.
client.login(token);