const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("roll")
    .setDescription("Roll a Number Between 1 - 100"),

  async execute(interaction) {
    if (interaction.commandName === "roll") {
      const number = Math.floor(Math.random() * 100) + 1;
      await interaction.reply(
        `**${interaction.user.username}**` + " rolled a " + number + "."
      );
    }
  },
};
