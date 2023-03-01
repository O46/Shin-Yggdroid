import discord
import configparser
from pathlib import Path

config = configparser.ConfigParser()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Started {self.application.owner.name}'s bot: {self.application.name}")

    async def on_message(self, payload):
        print()

    async def on_raw_message_delete(self, payload):
        print("")

if __name__ == "__main__":
    client = MyClient(intents=discord.Intents.default())
    client.run("")  # Call test_environmental_setter, then retrieve key from environment variable
