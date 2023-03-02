import discord
import configparser
import inspect
from datetime import datetime, timezone
from pprint import pprint
from pathlib import Path
import calendar
#from tinydb import TinyDB, Query
import os
from tools import config_creator
config = configparser.ConfigParser()


class MyClient(discord.Client):
    def __init__(self, set_intents):
        super().__init__(intents=set_intents)
        if not os.path.exists("data"):
            os.makedirs(os.path.dirname("data"), exist_ok=True)
        else:
            print("path exists")
        self.data_dir = "data"
        config_obj = configparser.ConfigParser()
        config_file = os.path.join(self.data_dir, "config2.ini")
        if not os.path.exists(config_file) or os.path.getsize(config_file) == 0:
            config_stat = False
            while not config_stat:
                config_stat = config_creator.create_config(config_file, config_obj)

        #self.message_db = TinyDB(self.data_dir, 'messageHistory.json'))
        #self.user_db = TinyDB(self.data_dir, 'userHistory.json'))
        #self.accept_db = TinyDB(self.data_dir, 'rulesAccept.json'))
        #self.name_backup_db = TinyDB(self.data_dir, "nameBackup.json"))
        #self.eo_af_db = TinyDB(self.data_dir, 'af.json'))
        #self.eo_af_global_db = TinyDB(self.data_dir, 'g_af.json'))
        #self.query = Query()

    async def on_ready(self):
        print(f"Started {self.application.owner.name}'s bot: {self.application.name}")
        print(f"{self.user.name}")
        # print(self.getattr())
        pprint(vars(self))

    async def on_message(self, message):
        print(self.application)
        if message.author.id is not self.application:
            print("It's not me")
        else:
            print("It is me")
        # Moving message params to their own dict, easier to iterate through, manage, and faster.
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

        if str(message.channel).startswith("Direct Message with "):
            print()
        elif message.channel.id == 826856868416323604:  # eo_next channel
            print()
        elif message.channel.id == 531636126927028224:  # deep_city channel
            print()
        elif message.channel.id == 750481250267037727:  # rules_accept channel
            print()
        elif message.channel.id == 1020340888347623444:  # mod_commands channel
            print()

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
    intents = discord.Intents.all()
    # intents = discord.Intents(members=True, messages=True, message_content=True)
    client = MyClient(intents)
    client.run("")
    # client.run("")  # Call test_environmental_setter, then retrieve key from environment variable
