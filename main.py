"""
Main Script
----------------------------

Copyright © 2023

Description:
    This is the main script for the BOT, a robust and adaptable Discord bot framework.
    It initializes the bot and runs the bot using a securely stored Discord token. 

Author:
    Ethan Smith

Usage:
    Run this script to start the bot. Ensure all dependencies are installed as per 'requirements.txt'.
    The bot's behavior and functionalities can be customized by modifying the modules in the 'BOT' folder.
    This script integrates these modules to create a cohesive and fully functional Discord bot.

Notes:


"""
from BOT import DiscordBot

def main():
    
    bot = DiscordBot()

    try:
        bot.run(bot.token)
    except Exception as e:
        bot.logger.error(f"Cannot run bot: {e}")

if __name__ == "__main__":
    main()