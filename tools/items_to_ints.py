def items_to_ints(discord_client, item_obj, item_name):
    """Converts all of a dictionary's key-values to integers"""
    setattr(discord_client, item_name, {key: int(value) for key, value in item_obj.items()})
