"""
Creator: o46
Date: 02/28/2023
Updated: 03/06/2023
Summary: Heart of the Shin-Yggdroid Discord management bot.
    Features:
        Role assignment - Users can assign themselves a select number of roles from predefined
            ranges
        Moderation tools - Moderators can Warn, ban, and notify users, check
            user history (warn count, nickname history, etc.)
        Logging - Reactions, calls, content, and so on are logged to a MongoDB powered database
        Games - Hosts the april fools gacha game, "play on 3DS through discord" feature
        User admittance - Require users to sign a ToS before being admitted to server
"""

import configparser
import importlib.util
import os
from pprint import pprint

import discord

from channel_actions import gacha
from channel_actions import mod_commands
# from channel_actions import * This is considered bad practice by PEP standards?
from channel_actions import private_message
from channel_actions import rules_admittance
# from tools import config_creator
from tools import environmental_setter


# import inspect
# from datetime import datetime, timezone
# from pathlib import Path
# import calendar
# from tinydb import TinyDB, Query


class MyClient(discord.Client):
    """Meat and potatoes of the operation. This class is the body of the bot and houses its
    logic."""

    def __init__(self, set_intents):
        super().__init__(intents=set_intents)
        self.config_obj = configparser.ConfigParser()
        if not os.path.exists("data"):
            os.makedirs(os.path.dirname("data"), exist_ok=True)
        else:
            print("path exists")
        self.data_dir = "data"

        # get the path of the "tools" directory relative to the current file
        self.tools_dir = os.path.join(os.path.dirname(__file__), 'tools')

        # loop through all files in the tools directory
        for filename in os.listdir(self.tools_dir):
            if filename.endswith('.py'):
                # import the module using the full path to the file
                module_name = os.path.splitext(filename)[0]  # remove the file extension
                module_path = os.path.join(self.tools_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # attach the module to a self attribute with the module name
                setattr(self, module_name, module)


        # await self.load_extension()

        self.set_config.set_config_vars(self)
        # self.accept_log = accept_log()
        # Converting all values in self.channel_ids, self.roles to ints for more performant
        # comparisons, usages.
        self.items_to_ints.items_to_ints(self, self.channel_ids, "channel_ids")
        self.items_to_ints.items_to_ints(self, self.roles, "roles")

        # print(config_obj["CHANNELS"]["announcement_channel_id"])
        # self.message_db = TinyDB(self.data_dir, 'messageHistory.json'))
        # self.user_db = TinyDB(self.data_dir, 'userHistory.json'))
        # self.accept_db = TinyDB(self.data_dir, 'rulesAccept.json'))
        # self.name_backup_db = TinyDB(self.data_dir, "nameBackup.json"))
        # self.eo_af_db = TinyDB(self.data_dir, 'af.json'))
        # self.eo_af_global_db = TinyDB(self.data_dir, 'g_af.json'))
        # self.query = Query()

    async def on_ready(self):
        """Gets triggered whenever the bot has connected to the discord api endpoint,
        ensures certain things are set up such as the guild and role objects"""
        print(f"Connected\n------------\nOwner: {self.application.owner.name} ("
              f"{self.application.owner.id})\nBot: {self.application.name} ({self.application_id})"
              f"\nGuild: {self.guilds[0]} ({self.guilds[0].id})\n------------\n")
        self.refresh_guild()
        self.refresh_roles()

    async def on_message(self, message):
        """This hijacks the on_message event to determine how to handle messages based on what
        channel it's sent in. Some actions are preformed regardless of channel location, and
        those will be after the if-else block so as not to impede user experience."""
        if message.author.id == self.application_id:
            print("It's me")
        else:
            if message.guild:
                # Moving message params to their own dict, easier to iterate through, manage,
                # and faster.
                msg_attrs = self.message_attribute_extraction(message)
            else:
                print("Privately messaged")

            if str(message.channel).startswith("Direct Message with "):
                private_message.print_me(self, message)
            elif message.channel.id == self.channel_ids["eo_next_id"]:
                gacha.place_holder(self, msg_attrs)
            elif message.channel.id == self.channel_ids["mod_commands_id"]:  # deep_city_id
                await rules_admittance.accept_handler(self, message)
                acceptable_commands = ["set", "rem", "lis", "!"]
                split_message = str(message.content).lower().split(" ", 1)
                if not any(x in split_message[0] for x in acceptable_commands):
                    await message.channel.send("Please make sure your message is in the format"
                                               "[action(set/remove)] [role name]")

                else:
                    print(message.guild.roles)
                    mod_commands.command_handler(self, message_attributes=msg_attrs,
                                                 split_message=split_message)
                    # role_assignment(self, split_message)"""
            elif message.channel.id == self.channel_ids["rules_accept_id"]:
                print()
                await rules_admittance.accept_handler(self, msg_attrs)
                # Call rules_admittance

    async def on_raw_message_delete(self, message):
        """Whenever a message is deleted trigger this handler, will extract known variables and
         commit them to log"""
        print(type(message))
        msg_attrs = self.message_attribute_extraction(message)
        pprint(msg_attrs)

    # Adds and formats user changes within a message
    def user_change(self, action, description, color, name, user_id):
        """Used to format messages sent when a user updates his or her profile"""
        formatted_message = discord.Embed(title=action, description=description, color=color)
        formatted_message.add_field(name="Member Name: ", value=str(name), inline=True)
        formatted_message.add_field(name="Member ID: ", value=str(user_id), inline=True)
        return formatted_message

    def message_attribute_extraction(self, message: discord.message.Message) -> dict:
        """Takes in a discord message object, extracts values I want to record, returns them in a
        dictionary where all lookups are O(1) and simple."""
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

    def refresh_guild(self):
        """Refreshes the guild object"""
        self.guild_obj = self.get_guild(self.guild_id)
        print(f"Discord guild object: {self.guild_obj}")

    def refresh_roles(self):
        """Refreshes all roles assigned to the guild object"""
        self.guild_roles = discord.utils.get(self.guild_obj.roles)
        print(f"Discord roles object: {dir(self.guild_roles)}")


if __name__ == "__main__":
    client_token = environmental_setter.env_var(["discord_token"])
    intents = discord.Intents.all()
    client = MyClient(intents)
    client.run(client_token['discord_token'])
