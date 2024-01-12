"""
Intents Configuration
------------------------------------

Copyright © 2023

Description:
    This module defines and configures the Discord Intents.
    Discord Intents allow the bot to receive specific events based on user activities.
    This module provides a centralized location to manage and customize the bot's intents
    for various events, ensuring granular control over the bot's interaction with Discord servers.

Author:
    Ethan Smith

Usage:
    Modify the 'get_intents' function to enable or disable specific intents based on the bot's requirements.
    Discord provides both general and privileged intents, where privileged intents require additional
    permissions and approval on the Discord Developer Portal.

Available Intents:
    - bans
    - dm_messages
    - dm_reactions
    - dm_typing
    - emojis
    - emojis_and_stickers
    - guild_messages
    - guild_reactions
    - guild_scheduled_events
    - guild_typing
    - guilds
    - integrations
    - invites
    - messages
    - reactions
    - typing
    - voice_states
    - webhooks

Privileged Intents (Requires approval on Discord Developer Portal):
    - members
    - message_content
    - presences

Notes:
    Ensure that the intents configured here align with the bot's functionality and comply with Discord's
    intent policy. Refer to the Discord API documentation for more information on Discord Intents.

"""
import discord

def get_intents():
    # Define your intents
    my_intents = discord.Intents.default()
    
    # Available Intents
    my_intents.bans = False                    # Allows access to ban events
    my_intents.dm_messages = False             # Allows access to direct message events
    my_intents.dm_reactions = False            # Allows access to direct message reaction events
    my_intents.dm_typing = False               # Allows access to direct message typing events
    my_intents.emojis = False                  # Allows access to emoji events
    my_intents.emojis_and_stickers = False     # Allows access to emoji and sticker events
    my_intents.guild_messages = False          # Allows access to guild message events
    my_intents.guild_reactions = False         # Allows access to guild reaction events
    my_intents.guild_scheduled_events = False  # Allows access to guild scheduled events
    my_intents.guild_typing = False            # Allows access to guild typing events
    my_intents.guilds = True                   # Allows access to guild events
    my_intents.integrations = True             # Allows access to integration events
    my_intents.invites = False                 # Allows access to invite events
    my_intents.messages = True                 # Allows access to message events
    my_intents.reactions = False               # Allows access to reaction events
    my_intents.typing = False                  # Allows access to typing events
    my_intents.voice_states = False            # Allows access to voice state events
    my_intents.webhooks = False                # Allows access to webhook events
    
    # Privileged Intents (Needs to be enabled on the Discord Developer Portal)
    my_intents.members = True                 # Allows access to member events
    my_intents.message_content = True         # Allows access to message content
    my_intents.presences = True               # Allows access to presence events

    return my_intents