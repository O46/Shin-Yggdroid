import discord
from tools import uid_to_color


async def notify_user(client, message_attributes,  split_message):
    user_id = split_message.split(" ", 2)[0]
    try:
        user_object = await client.fetch_user(user_id)
    except discord.NotFound as find_error:
        user_object = False
        print(f"Could not find user: {find_error}")

    if not user_object:
        await split_message.channel.send(f"Unable to locate user by id {split_message[1]}")
    else:
        try:
            await user_object.send(split_message[1])
        except discord.errors.Forbidden as send_error:
            await split_message.channel.send(f"Unable to send message to {user_object}")
    if split_message[0] == "color":
        color = uid_to_color(provided_id=str(message_attributes.author_id))
        await split_message.channel.send(f"Your unique color is {color[2][0]}: "
                               f"https://convertingcolors.com/rgb-color-{color[2][0]}"
                               f"_{color[2][1]}_{color[2][2]}.html")
    else:
        await split_message.channel.send(f"Could not find suitable command in string \"{split_message[0]}\"")


async def command_handler(self, message_attributes, split_message):
    print(split_message)
    if split_message[0] == "notifyuser":
        notify_user(self, split_message)
