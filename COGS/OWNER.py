import discord
from discord.ext import commands
from discord import app_commands

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #owner test for communication between Discord and the bot
    @commands.command(name='ping')
    async def ping(self, ctx):
        if await self.bot.is_owner(ctx.author):
            self.bot.logger.info(f"OWNER COMMAND: ping, {ctx.author}")
            await ctx.send("Pong!")
        else:
            self.bot.logger.warning(f"OWNER COMMAND: ping, {ctx.author} - NONOWNER")

    @app_commands.command(name='sync', description="Synchronize slash commands")
    @app_commands.describe(scope="The scope of the sync. Can be 'global' or 'guild'")
    @app_commands.default_permissions(administrator=True)
    @commands.is_owner()
    async def sync(self, interaction: discord.Interaction, scope: str):
        if scope == "global":
            await self.bot.tree.sync()
            level = 'global'
        elif scope == "guild":
            await self.bot.tree.sync(guild=interaction.guild)
            level = 'guild'
        else:
            await interaction.response.send_message("The scope must be 'global' or 'guild'.", ephemeral=True)
            return

        self.bot.logger.info(f"SLASH COMMAND: sync, {interaction.user}, Level: {level}")
        await interaction.response.send_message(f"Commands synced, level: {level}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))