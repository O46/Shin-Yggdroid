"""guild = client.get_guild(self.guild_id)
new_member = discord.utils.get(guild.roles, name="new adventurer")
if message.content.strip().lower().startswith("accept"):
    print(f"user {message.author} has accepted")
    await message.author.remove_roles(new_member)
    formatted_message = user_change("User accepted", "", 587983, message.author.name, message.author.id)
    # ("User Removed", "", 0xFFF8E7, member.name, member.id)
    channel = client.get_channel(self.channel_ids["rules_accept_id"])
    await channel.send(embed=formatted_message)
    accept_log(message)"""