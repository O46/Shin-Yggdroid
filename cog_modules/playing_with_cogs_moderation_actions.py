from discord.ext import commands


@commands.Cog.listener()
async def on_message(self, message):
    """Actually adds the autoassign roles."""
    print("Cog activated")
    print(f"Message sent, {message}")
    print(self.data_dir)
    #autoassign_roles = []
    #autoassign_role_ids = await \
    #    self.bot.pg_utils.get_autoassign_roles(member.guild.id)
    #if not autoassign_role_ids:
    #    return
    #for role in member.guild.roles:
    #    if role.id in autoassign_role_ids:
    #        autoassign_roles.append(role)
    #await member.add_roles(*autoassign_roles)

