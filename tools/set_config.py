import os
from tools import config_creator
import configparser


def set_config_vars(discord_client):
    """Sets all configuration variables"""
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


if __name__ == "__main__":
    print("Please run from within a Discord bot object")
