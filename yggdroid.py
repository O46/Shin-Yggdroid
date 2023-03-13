"""
Creator: o46
Date: 02/28/2023
Updated: 03/06/2023
Summary: Heart of the Shin-Yggdroid Discord management bot.
    Features:
        Role assignment - Users can assign themselves a select number of roles from predefined ranges
        Moderation tools - Moderators can Warn, ban, and notify users, check user history (warn count, nickname history,
            etc.)
        Logging - Reactions, calls, content, and so on are logged to a MongoDB powered database
        Games - Hosts the april fools gacha game, "play on 3DS through discord" feature
        User admittance - Require users to sign a ToS before being admitted to server
"""

import os
import configparser
from pprint import pprint
import discord
from tools import config_creator
from tools import environmental_setter
from tools import uid_to_color

from channel_actions import *
from discord.ext import commands


# import inspect
# from datetime import datetime, timezone
# from pathlib import Path
# import calendar
# from tinydb import TinyDB, Query


def accept_log(message):
    print("stub for logging user acceptance, record user ID, time, message and message id.")


# Adds and formats user changes within a message
def user_change(action, description, color, name, user_id):
    formatted_message = discord.Embed(title=action, description=description, color=color)
    formatted_message.add_field(name="Member Name: ", value=str(name), inline=True)
    formatted_message.add_field(name="Member ID: ", value=str(user_id), inline=True)
    return formatted_message


def message_attribute_extraction(message: discord.message.Message) -> dict:
    """
    Takes in a discord message object, extracts values I want to record, returns them in a dictionary where all
    lookups are O(1) and simple."""
    message_dict = {"channel_id": message.channel.id,
                    "author_id": message.author.id,
                    "message_id": message.id,
                    "channel_name": message.channel.name,
                    "author_name": message.author.name,
                    "content": message.content,
                    "time": message.created_at,  # datetime.now(timezone.utc),
                    "attachments": message.attachments,
                    "mentions": message.mentions
                    }
    return message_dict


def items_to_ints(discord_client, item_obj, item_name):
    """"""
    setattr(discord_client, item_name, {key: int(value) for key, value in item_obj.items()})


def set_config_vars(discord_client):
    """"""
    config_file = os.path.join(discord_client.data_dir, "config.ini")
    if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
        config_stat = False
        while not config_stat:
            config_stat = config_creator.create_config(config_file, discord_client.config_obj)
    config_obj = configparser.ConfigParser()
    config_obj.read(config_file)
    discord_client.guild_id = int(config_obj["GUILD"]["guild_id"])
    discord_client.channel_ids = dict(config_obj["CHANNELS"])
    discord_client.roles = dict(config_obj["ROLES"])
    discord_client.files = config_obj["FILES"]
    discord_client.emoji = config_obj["EMOJI"]
    discord_client.gacha = config_obj["GACHA.VALUES"]


def refresh_guild(client):
    client.guild_obj = client.get_guild(client.guild_id)
    print(f"Discord guild object: {client.guild_obj}")


def refresh_roles(client):
    print(client.guild_obj.roles)
    #client.guild_roles = discord.utils.get(client.guild_obj.roles)
    #print(type(client.guild_obj.roles))
    print(f"Discord roles object: {dir(client.guild_roles)}")


class MyClient(discord.Client):
    def __init__(self, set_intents):
        super().__init__(intents=set_intents)
        self.config_obj = configparser.ConfigParser()
        if not os.path.exists("data"):
            os.makedirs(os.path.dirname("data"), exist_ok=True)
        else:
            print("path exists")
        self.data_dir = "data"
        set_config_vars(self)

        # Converting all values in self.channel_ids, self.roles to ints for more performant comparisons, usages.
        items_to_ints(self, self.channel_ids, "channel_ids")
        items_to_ints(self, self.roles, "roles")

        # print(config_obj["CHANNELS"]["announcement_channel_id"])
        # self.message_db = TinyDB(self.data_dir, 'messageHistory.json'))
        # self.user_db = TinyDB(self.data_dir, 'userHistory.json'))
        # self.accept_db = TinyDB(self.data_dir, 'rulesAccept.json'))
        # self.name_backup_db = TinyDB(self.data_dir, "nameBackup.json"))
        # self.eo_af_db = TinyDB(self.data_dir, 'af.json'))
        # self.eo_af_global_db = TinyDB(self.data_dir, 'g_af.json'))
        # self.query = Query()

    async def on_ready(self):
        """"""
        print(f"Connected\n------------\nOwner: {self.application.owner.name} ({self.application.owner.id})\n"
              f"Bot: {self.application.name} ({self.application_id})\n"
              f"Guild: {self.guilds[0]} ({self.guilds[0].id})\n------------\n")
        refresh_guild(self)
        refresh_roles(self)

    async def on_message(self, message):
        """"""
        if message.author.id == self.application_id:
            print("It's me")
        else:
            if message.guild:
                # Moving message params to their own dict, easier to iterate through, manage, and faster.
                msg_attrs = message_attribute_extraction(message)
            else:
                print("Privately messaged")

            if str(message.channel).startswith("Direct Message with "):
                print()
                direct(self, message)
            elif message.channel.id == self.channel_ids["eo_next_id"]:
                print()
                gacha(self, msg_attrs)
            elif message.channel.id == self.channel_ids["mod_commands_id"]:  # deep_city_id
                await rules_admittance.accept_handler(self, message)
                """acceptable_commands = ["set", "rem", "lis", "!"]
                split_message = str(message.content).lower().split(" ", 1)
                if not any(x in split_message[0] for x in acceptable_commands):
                    print("Couldn't find command...")
                    await message.channel.send(
                        'Please make sure your message is in the format \"[action(set/remove)] [role name]\"'.format(
                            message))
                else:
                    print(message.guild.roles)
                    mod_commands.command_handler(self, message_attributes=msg_attrs, split_message=split_message)
                    # role_assignment(self, split_message)"""
            elif message.channel.id == self.channel_ids["rules_accept_id"]:
                print()
                rules_admittance.accept_handler(self, msg_attrs)
                # Call rules_admittance

    async def on_raw_message_delete(self, message):
        """"""
        print(type(message))
        msg_attrs = message_attribute_extraction(message)
        pprint(msg_attrs)


if __name__ == "__main__":
    client_token = environmental_setter.env_var(["discord_token"])
    intents = discord.Intents.all()
    client = MyClient(intents)
    client.run(client_token['discord_token'])
