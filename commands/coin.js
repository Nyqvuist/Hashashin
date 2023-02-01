const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
  data: new SlashCommandBuilder()
    .setName("roll")
    .setDescription("Flip a Coin or Dice Roll.")
    .addSubcommand((subcommand) =>
      subcommand.setName("flip").setDescription("Flip a coin.")
    )
    .addSubcommand((subcommand) =>
      subcommand.setName("roll").setDescription("Roll a Number Between 0 - 100")
    ),

  async execute(interaction) {
    if (interaction.options.getSubcommand() === "flip") {
      const number = Math.floor(Math.random() * 2);
      if (number === 0) {
        await interaction.reply(interaction.user.username + " gets Head.");
      } else {
        await interaction.reply(interaction.user.username + " is a furry.");
      }
    } else if (interaction.options.getSubcommand() === "roll") {
      const number = Math.floor(Math.random() * 100);
      await interaction.reply(
        interaction.user.username + " rolled a " + number + "."
      );
    }
  },
};
