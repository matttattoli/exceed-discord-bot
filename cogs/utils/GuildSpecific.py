from os import path
guild_id_file = path.join(path.dirname(__file__), 'GuildLogChannel.dict')


def getGuildLogChannel(ctx):
    guild_ids = dict(open(guild_id_file, 'r'))
    if ctx.guild in guild_ids.keys():
        return guild_ids[ctx.guild]


def setGuildLogChannel(ctx):
    if path.join(path.dirname(__file__), 'GuildLogChannel.dict'):
        guild_ids = open(guild_id_file, 'w+')
