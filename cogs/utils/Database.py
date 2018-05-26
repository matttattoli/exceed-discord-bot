import discord
from discord.ext import commands
import asyncpg
import datetime
from config import *


async def __init__():
    global db
    db = await asyncpg.connect(user=privateconfig["database"]["user"], password=privateconfig["database"]["password"],
                               database=privateconfig["database"]["database"], host=privateconfig["database"]["host"])
    await db.execute("""CREATE TABLE IF NOT EXISTS guilds (
            gid	INTEGER NOT NULL UNIQUE,
            log_mode	INTEGER DEFAULT 0,
            log_channel	INTEGER DEFAULT NULL,
            bot_volume    INTEGER DEFAULT 0.5,
            PRIMARY KEY(gid)
            )""")
    await db.execute("""CREATE TABLE IF NOT EXISTS reminders (
            userid INTEGER NOT NULL,
            channelid	INTEGER NOT NULL,
            created_at	TIMESTAMP NOT NULL,
            expires	TIMESTAMP NOT NULL,
            message TEXT DEFAULT NULL
            )""")
    await db.execute("""CREATE TABLE IF NOT EXISTS funroles (
            gid INTEGER NOT NULL,
            rolename TEXT NOT NULL,
            roleid INTEGER NOT NULL UNIQUE,
            PRIMARY KEY(roleid)
            )""")
    print("INITIALIZED DB")
# TODO: convert all sqlite3 to postgre/asyncpg
# TODO: convert all queries into f strings with proper format for postgre : DONE


class Database:
    async def initializeGuild(gid: int):
        data = await db.fetch(f"SELECT gid FROM guilds WHERE gid = {gid}")
        if data is None:
            db.execute(f"INSERT INTO guilds(gid) VALUES({gid})")

    async def setLogChannel(gid: int, logmode: int, logchan: int):
        data = await db.fetch(f"SELECT gid FROM guilds WHERE gid = {gid}")
        if data is None:
            await db.execute(f"""INSERT INTO guilds(gid, log_mode, log_channel) VALUES({gid},{logmode},{logchan})""")
        else:
            await db.execute(f"""UPDATE guilds SET log_mode={logmode}, log_channel={logchan} WHERE gid = {gid}""")

    async def getLogChannel(gid: int):
        data = await db.fetch(f"SELECT log_mode, log_channel from guilds WHERE gid = {gid}")
        if data is None or data[0] == 0:
            return None
        else:
            return data[1]

    async def addfunrole(gid: int, role: discord.Role):
        data = await db.fetch(f"SELECT gid FROM funroles WHERE roleid = {role.id}")
        if data is None:
            await db.execute(f"""INSERT INTO funroles(gid, rolename, roleid) VALUES({gid},'{role.name}',{role.id})""")
        else:
            return

    async def removefunrole(gid: int, role: discord.Role):
        await db.execute(f"DELETE FROM funroles WHERE roleid = {role.id}")

    async def isfunrole(gid: int, roleid: int):
        data = await db.fetch(f"SELECT roleid, rolename FROM funroles WHERE roleid = {roleid}")  # LIMIT 1 ??
        if data is not None:
            return True
        else:
            return False

    async def getFunRoles(gid: int):
        data = await db.fetch(f"SELECT rolename FROM funroles WHERE gid = {gid}")
        return data

    async def getReminders(userid: int):
        data = await db.fetch(f"SELECT * FROM reminders WHERE userid = {userid}")
        return data

    async def createReminder(userid: int, channelid: int, created_at: datetime.datetime,
                       expires: datetime.datetime, message: str=None):
        db.execute(f"""INSERT INTO reminders(userid, channelid, created_at, expires, message) 
        VALUES({userid},{channelid},TIMESTAMP '{created_at}',TIMESTAMP '{expires}','{message}')""")

    async def getExpired():
        data = db.fetch(f"SELECT * FROM reminders WHERE expires < {datetime.datetime.now()}")
        return data

    async def deleteReminder(userid: int, created_at: datetime.datetime, expires: datetime.datetime, message: str=None):
        await db.execute(f"""DELETE FROM reminders WHERE userid = {userid} AND created_at = {created_at}
                         AND expires = {expires} AND message = {message}""")
