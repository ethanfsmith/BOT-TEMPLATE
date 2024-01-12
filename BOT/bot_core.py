"""
Core Bot Implementation
--------------------------------------

Copyright © 2023

Description:
    This module defines the core implementation of the BOT TEMPLATE Discord bot using the Discord.py library.
    The `DiscordBot` class extends the `commands.Bot` class, providing a customizable framework for
    handling various Discord events, commands, and interactions. The core bot includes an integrated logger,
    configuration for Discord Intents, and a modularized structure for bot functionalities.

Author:
    Ethan Smith

Usage:
    Import this module in your main script to initialize the Discord bot. 

Notes:
    The 'BOT' folder contains additional modules for configuring Discord Intents ('intents.py') and the logger ('logger.py').

"""
import os
import discord
from discord.ext import commands
import platform

from .version import __version__
from .intents import get_intents
from .config import get_token, get_owners
from .logger import setup_logging

from DATABASE.database import Database

class DiscordBot(commands.Bot):
    
    def __init__(self) -> None:
        # Initialize the bot with necessary configurations
        super().__init__(command_prefix= '!',
                         intents=get_intents(),
                         help_command=None,
                         owner_ids=set(get_owners()))
        self.synced = False

        # Initialize and assign the bot's components
        self.version = __version__
        self.token = get_token()
        self.owners = set(get_owners())
        self.logger = setup_logging()

        self.database = Database(self.logger)

    async def setup_hook(self):

        #INIT DATABASE
        await self.database.init_db()

        #LOGIN MESSAGES
        self.logger.info('-----------------------------------------------------')
        self.logger.info('LOGIN SUCCESSFUL')
        self.logger.info('')
        self.logger.info(f'BOT: {self.user.name}')
        self.logger.info(f'USER ID: {self.user.id}')
        self.logger.info(f'VERSION: {self.version}')
        self.logger.info('')
        self.logger.info(f'API VERSION: {discord.__version__}')
        self.logger.info(f'PYTHON VERSION: {platform.python_version()}')
        self.logger.info(f'ENVIRONMENT: {platform.system()} {platform.release()} ({os.name})')
        self.logger.info('-----------------------------------------------------')

        #LOAD COGS
        cogs_directory = os.path.join(os.path.dirname(__file__), '..', 'COGS')
        for filename in os.listdir(cogs_directory):
            if filename.endswith('.py') and not filename.startswith('_'):
                cog_name = filename[:-3]  
                cog_path = f"COGS.{cog_name}"
                try:
                    await self.load_extension(cog_path)
                    self.logger.info(f"LOADED COG: {cog_name}")
                except Exception as e:
                    self.logger.error(f"FAILED TO LOAD COG: {cog_name}: {e}")
        self.logger.info('-----------------------------------------------------')

        #DEFINED OWNERS
        if not self.owners:
            self.logger.warning("No owners defined in owners.env. Proceeding with default owner settings.")

    async def close(self):
        await self.database.close_connection()
        await super().close()

    async def on_ready(self):
        if not self.synced:
            await self.tree.sync()  
            self.synced = True

    async def on_message(self, message):
    # Ignore messages from any bot (including itself)
        if message.author.bot:
            return
        await self.process_commands(message)