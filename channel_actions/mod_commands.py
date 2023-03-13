"""import discord


def notify_user(client, split_message):
    user_id = split_message.split(" ", 2)[0]
    try:
        user_object = await client.fetch_user(user_id)
    except discord.NotFound as find_error:
        user_object = False
        print(f"Could not find user: {find_error}")

    if not user_object:
        await message.channel.send(f"Unable to locate user by id {command[1]}")
    else:
        try:
            await user_object.send(command[1])
        except discord.errors.Forbidden as send_error:
            await message.channel.send(f"Unable to send message to {user_object}")
    if command[0] == "color":
        color = uid_to_color.id_to_color(provided_id=str(message.author.id))
        await message.channel.send(f"Your unique color is {color[2][0]}: "
                               f"https://convertingcolors.com/rgb-color-{color[2][0]}"
                               f"_{color[2][1]}_{color[2][2]}.html")
    else:
        await message.channel.send(f"Could not find suitable command in string \"{command[0]}\"")


def command_handler(self, message_attributes, split_message):
    print(split_message)
    if split_message[0] == "notifyuser":
        notify_user(self, split_message)

"""