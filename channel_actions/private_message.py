"""This will be where direct personal are handled."""
from pprint import pprint


def print_me(discord_client, message):
    """This will hold all the personal message stuff..."""
    print(f"We're in direct and we got {discord_client} and {message}")
    pprint(message)


if __name__ == "__main__":
    print_me()
