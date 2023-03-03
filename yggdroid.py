import discord
import configparser
import inspect
from datetime import datetime, timezone
from pprint import pprint
from pathlib import Path
import calendar
# from tinydb import TinyDB, Query
import os
from tools import config_creator
from tools import environmental_setter
from tools import uid_to_color

config = configparser.ConfigParser()


class MyClient(discord.Client):
    def __init__(self, set_intents):
        super().__init__(intents=set_intents)
        if not os.path.exists("data"):
            os.makedirs(os.path.dirname("data"), exist_ok=True)
        else:
            print("path exists")
        self.data_dir = "data"
        config_file = os.path.join(self.data_dir, "config.ini")
        if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
            config_stat = False
            while not config_stat:
                config_stat = config_creator.create_config(config_file, config_obj)
        config_obj = configparser.ConfigParser()
        config_obj.read(config_file)
        self.guild_id = int(config_obj["GUILD"]["guild_id"])
        self.channel_ids = dict(config_obj["CHANNELS"])
        self.roles = dict(config_obj["ROLES"])
        self.files = config_obj["FILES"]
        self.emoji = config_obj["EMOJI"]
        self.gacha = config_obj["GACHA.VALUES"]

        # Converting all values in self.channel_ids, self.roles to ints for more performant comparisons, usages.
        self.channel_ids = {key: int(value) for key, value in self.channel_ids.items()}
        self.roles = {key: int(value) for key, value in self.roles.items()}

        # print(config_obj["CHANNELS"]["announcement_channel_id"])
        # self.message_db = TinyDB(self.data_dir, 'messageHistory.json'))
        # self.user_db = TinyDB(self.data_dir, 'userHistory.json'))
        # self.accept_db = TinyDB(self.data_dir, 'rulesAccept.json'))
        # self.name_backup_db = TinyDB(self.data_dir, "nameBackup.json"))
        # self.eo_af_db = TinyDB(self.data_dir, 'af.json'))
        # self.eo_af_global_db = TinyDB(self.data_dir, 'g_af.json'))
        # self.query = Query()

    async def on_ready(self):
        print(f"Connected\n------------\nOwner: {self.application.owner.name} ({self.application.owner.id})\n"
              f"Bot: {self.application.name} ({self.application_id})\n"
              f"Guild: {self.guilds[0]} ({self.guilds[0].id})\n------------\n")

    async def on_message(self, message):
        print(self.application)
        if message.author.id == self.application_id:
            print("It's me")
        else:
            # Moving message params to their own dict, easier to iterate through, manage, and faster.
            if message.guild:
                msg_attrs = {"channel_id": message.channel.id,
                             "author_id": message.author.id,
                             "message_id": message.id,
                             "channel_name": message.channel.name,
                             "author_name": message.author.name,
                             "content": message.content,
                             "time": message.created_at,  # datetime.now(timezone.utc),
                             "attachments": message.attachments,
                             "mentions": message.mentions
                             }
            else:
                print("Privately messaged")

            if str(message.channel).startswith("Direct Message with "):
                print()
            elif message.channel.id == self.channel_ids["eo_next_id"]:
                print()
            elif message.channel.id == self.channel_ids["deep_city_id"]:
                print()
            elif message.channel.id == self.channel_ids["rules_accept_id"]:
                print()
            elif message.channel.id == self.channel_ids["mod_commands_id"]:
                command = message.content.split(maxsplit=2)
                command[0] = command[0].lower()
                if command[0] == "notifyuser":
                    try:
                        user_object = await client.fetch_user(command[1])
                    except:
                        user_object = False
                    if not user_object:
                        await message.channel.send(f"Unable to locate user by id {command[1]}")
                    else:
                        try:
                            await user_object.send(command[1])
                        except discord.errors.Forbidden as send_error:
                            await message.channel.send(f"Unable to send message to {user_object}")
                elif command[0] == "color":
                    color = uid_to_color.id_to_color(provided_id=str(message.author.id))
                    await message.channel.send(f"Your unique color is {color[2][0]}: "
                                               f"https://convertingcolors.com/rgb-color-{color[2][0]}"
                                               f"_{color[2][1]}_{color[2][2]}.html")
                else:
                    await message.channel.send(f"Could not find suitable command in string \"{command[0]}\"")


    async def on_raw_message_delete(self, message):
        msg_attrs = {"channel_id": message.channel.id,
                     "author_id": str(message.author.id),
                     "message_id": str(message.id),
                     "channel_name": message.channel.name,
                     "author_name": message.author.name,
                     "content": message.content,
                     "time": message.created_at,  # datetime.now(timezone.utc),
                     "attachments": message.attachments,
                     "mentions": message.mentions
                     }
        pprint(msg_attrs)


if __name__ == "__main__":

    client_token = environmental_setter.env_var(["discord_token"])
    intents = discord.Intents.all()
    client = MyClient(intents)
    client.run(client_token['discord_token'])
