from os import path
import json
eee = path.dirname(__file__).split('/')[:-2]
guild_id_file = ''
for i in eee:
    guild_id_file += i + "/"
guild_id_file += 'GuildConfigs.json'


def createfile():
    if not path.exists(guild_id_file):
        file = open(guild_id_file, 'w+')
        file.write("{}")
        file.close()


def addNewGuild(gid: int):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        guild_ids[str(gid)] = {}
        json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)
    else:
        createfile()


def setGuildLogChannel(gid: int, channel: int):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        if str(gid) in guild_ids:
            guild_ids[str(gid)]["Log_Channel"] = str(channel)
            json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)
        else:
            guild_ids = json.load(open(guild_id_file, 'r'))
            guild_ids[str(gid)] = {}
            guild_ids[str(gid)]["Log_Channel"] = str(channel)
            json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)
    else:
        createfile()


def getGuildLogChannel(gid: int):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        if str(gid) in guild_ids:
            return int(guild_ids[str(gid)]["Log_Channel"])
        else:
            return None


def appendGuildSetting(gid: int, setting: str, value: str):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        if str(gid) in guild_ids:
            if setting not in guild_ids[str(gid)]:
                guild_ids[str(gid)][setting] = []
            guild_ids[str(gid)][setting].append(value)
            json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)
        else:
            guild_ids = json.load(open(guild_id_file, 'r'))
            guild_ids[str(gid)] = {}
            if setting not in guild_ids[str(gid)]:
                guild_ids[str(gid)][setting] = []
            guild_ids[str(gid)][setting].append(value)
            json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)
    else:
        createfile()


def removeGuildSetting(gid: int, setting: str, value: str):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        if str(gid) in guild_ids:
            guild_ids[str(gid)][setting].remove(value)
            json.dump(guild_ids, open(guild_id_file, 'w'), indent=4, sort_keys=True)


def getGuildSetting(gid: int, setting: str):
    if path.exists(guild_id_file):
        guild_ids = json.load(open(guild_id_file, 'r'))
        if str(gid) in guild_ids:
            if setting in guild_ids[str(gid)]:
                return guild_ids[str(gid)][setting]
            return []
        else:
            return []
