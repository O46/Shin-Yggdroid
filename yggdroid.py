import discord
import configparser
import inspect
from datetime import datetime, timezone
from pprint import pprint
from pathlib import Path
import calendar

config = configparser.ConfigParser()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Started {self.application.owner.name}'s bot: {self.application.name}")
        print(f"{self.user.name}")
        #print(self.getattr())

    async def on_message(self, message):
        print(f"Message: {message}")
        attrs = {"channel_id" : message.channel.id,
                 "author_id": str(message.author.id),
                 "message_id": message.id,
                 "channel_name": message.channel.name,
                 "author_name": message.author.name,
                 "content": message.content,
                 "time": datetime.now(timezone.utc)
                 }


        #pprint(attrs)

        #print(f"Message.channel: {message.channel}\nMessage.channel.id: {message.channel.id}")

        #print(datetime.now('US/Central'))
        #print(calendar.timegm(dt.utctimetuple()))
        #print(message.__dict__)
        #pprint(inspect.getmembers(message))

    async def on_raw_message_delete(self, payload):
        print("")


if __name__ == "__main__":
    intents = discord.Intents.all()
    #intents = discord.Intents(members=True, messages=True, message_content=True)
    client = MyClient(intents=intents)
    client.run("")
    #client.run("")  # Call test_environmental_setter, then retrieve key from environment variable




