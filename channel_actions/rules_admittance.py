import discord.ext

async def accept_handler(client, message):
    #guild = client.get_guild(self.guild_id)
    #print(message.guild)
    #client.guild_id
    #print(test)
    print(client.guild_obj)
    new_member = discord.utils.get(client.guild_obj.roles, name="new adventurer")
    print(f"Printing new_member: {new_member}")
    if message.content.strip().lower().startswith("accept"):
        print(f"user {message.author} has accepted")
        await message.author.remove_roles(new_member)
        formatted_message = user_change("User accepted", "", 587983, message.author.name, message.author.id)
        # ("User Removed", "", 0xFFF8E7, member.name, member.id)
        channel = client.get_channel(self.channel_ids["rules_accept_id"])
        await channel.send(embed=formatted_message)
        accept_log(message)

if __name__ == "__main__":
    print()