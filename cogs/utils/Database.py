import discord
from discord.ext import commands
import sqlite3


db = sqlite3.connect("exceeddatabase.db")
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS `guilds` (
        `gid`	INTEGER NOT NULL UNIQUE,
        `log_mode`	INTEGER DEFAULT 0,
        `log_channel`	INTEGER DEFAULT NULL,
        `bot_volume`    INTEGER REAL DEFAULT 0.5,
        PRIMARY KEY(`gid`)
        )""")
# cursor.execute("""CREATE TABLE IF NOT EXISTS `reminders` (
#         `channelid`	INTEGER NOT NULL,
#         `created_at`	INTEGER NOT NULL,
#         `expires`	INTEGER NOT NULL,
#         `message` TEXT DEFAULT NULL
#         )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS `funroles` (
        `gid` INTEGER NOT NULL,
        `rolename` TEXT NOT NULL UNIQUE,
        `roleid` INTEGER NOT NULL UNIQUE,
        PRIMARY KEY(`roleid`)
        )""")
db.commit()


class Database:
    def initializeGuild(gid: int):
        cursor.execute("SELECT gid FROM guilds WHERE gid = ?", (gid,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("INSERT INTO guilds(gid) VALUES(?)", (gid,))
        db.commit()

    def setLogChannel(gid: int, logmode: int, logchan: int):
        cursor.execute("SELECT gid FROM guilds WHERE gid = ?", (gid,))
        data = cursor.fetchone()
        if data is None:
            cursor.execute("""INSERT INTO guilds(gid, log_mode, log_channel) VALUES(?,?,?)
                            """, (gid, logmode, logchan))
        else:
            cursor.execute("""UPDATE guilds SET log_mode=?, log_channel=? WHERE gid = ?""",
                           (logmode, logchan, gid))
        db.commit()

    def getLogChannel(gid: int):
        cursor.execute("SELECT `log_mode`, `log_channel` from guilds WHERE gid = ?", (gid,))
        data = cursor.fetchone()
        if data is None or data[0] == 0:
            return None
        else:
            return data[1]

