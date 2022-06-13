require('dotenv').config();
const fs = require('node:fs');
const path = require('node:path');
const mongoose = require('mongoose');
const { Client, Intents, Collection } = require('discord.js');
const token = process.env.DISCORD_TOKEN;
const DB = process.env.DB;
const STEAM = process.env.STEAM_KEY;


// Making a DB connection.
mongoose.connect(DB, () => {
    console.log('DB is connected.')
})

// Create a new client instance
const client = new Client({
	intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGE_REACTIONS, Intents.FLAGS.GUILD_MEMBERS],
	partials: ['MESSAGE', 'CHANNEL', 'REACTION'],
});

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

client.on('ready', async() => {
	const games = [
		'Among Us',
		'ELDEN RING',
		'Devil May Cry 5',
		'HuniePop',
		'Lost Ark',
		'Maplestory',
		'Assassins Creed 2',
		'Bioshock',
		'Apex Legends',
		'Call Of Duty: Black Ops',
	]

	setInterval(() => {
		const status = games[Math.floor(Math.random() * games.length)]
		client.user.setPresence({activities: [{name: `${status}`, type: 'PLAYING'}]})
	},  30 * 60 * 100)

})

// Login to Discord with the client token.
client.login(token);