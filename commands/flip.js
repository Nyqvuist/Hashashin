const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("flip")
    .setDescription("Flip a Coin."),

  async execute(interaction) {
    if (interaction.commandName === "flip") {
      const number = Math.floor(Math.random() * 2);
      if (number === 0) {
        await interaction.reply(
          `**${interaction.user.username}**` + " gets head."
        );
      } else {
        await interaction.reply(
          `**${interaction.user.username}**` + " is a furry."
        );
      }
    }
  },
};
