import discord
import configparser
import inspect
from datetime import datetime, timezone
from pprint import pprint
from pathlib import Path
import calendar
#from tinydb import TinyDB, Query
import os

config = configparser.ConfigParser()


class MyClient(discord.Client):
    def __init__(self, intents):
        print(intents)
        super().__init__(intents=intents)
        if not os.path.exists("data"):
            os.makedirs(os.path.dirname("data"), exist_ok=True)
        else:
            print("path exists")
        self.data_dir = ""
        #self.message_db = TinyDB(os.path.join(os.getcwd(), 'messageHistory.json'))
        #self.user_db = TinyDB(os.path.join(os.getcwd(), 'userHistory.json'))
        #self.accept_db = TinyDB(os.path.join(os.getcwd(), 'rulesAccept.json'))
        #self.name_backup_db = TinyDB(os.path.join(os.getcwd(), "nameBackup.json"))
        #self.eo_af_db = TinyDB(os.path.join(os.getcwd(), 'af.json'))
        #self.eo_af_global_db = TinyDB(os.path.join(os.getcwd(), 'g_af.json'))
        #self.query = Query()

    async def on_ready(self):
        print(f"Started {self.application.owner.name}'s bot: {self.application.name}")
        print(f"{self.user.name}")
        # print(self.getattr())

    async def on_message(self, message):
        # print(f"Message: {message}")
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

        # print(f"Message.channel: {message.channel}\nMessage.channel.id: {message.channel.id}")

        # print(datetime.now('US/Central'))
        # print(calendar.timegm(dt.utctimetuple()))
        # print(message.__dict__)
        # pprint(inspect.getmembers(message))

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
    client = MyClient(intents=intents)
    client.run("")
    # client.run("")  # Call test_environmental_setter, then retrieve key from environment variable
