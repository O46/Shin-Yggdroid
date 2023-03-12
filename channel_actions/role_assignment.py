"""def role_assignment(discord_client, split_message):
    """"""
    try:
        print(discord_client)
        print(vars(discord_client))
        pprint(discord_client)
        guild = discord_client.get_guild(discord_client.guild_id)
        print(f"GOT GUILD: {guild}")
        color_anchor = guild.get_role(discord_client.roles["color"])
        category_anchor = guild.get_role(discord_client.roles["category"])
        class_anchor = guild.get_role(discord_client.roles["class"])
        everyone_anchor = guild.get_role(discord_client.roles["everyone"])
        color_roles = [r for r in guild.roles if color_anchor > r > category_anchor]
        category_roles = [r for r in guild.roles if category_anchor > r > class_anchor]
        class_roles = [r for r in guild.roles if class_anchor > r > everyone_anchor]
    except Exception as e:
        print(e)"""