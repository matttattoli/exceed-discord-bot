import discord
from discord.ext import commands
from cogs.utils.checks import *
from cogs.utils.GlobalVars import *
from cogs.utils.debug import *
from cogs.utils.Database import Database
import datetime
import asyncio


class RemindParser:
    def parseReminderMsg(msg: str):
        timedelta = ''
        if msg.count(" to ") > 0 and msg.count("in ") > 0:
            data = msg.split(" to ")
            timedelta = data[0].split("in ")[1]
            remindmsg = data[1]
            print(f"{timedelta} ..... {remindmsg}")
        if timedelta == '':
            timedelta = msg.split(" ")[0]
            remindmsg = msg.replace(timedelta + " ", "")
            print(f"{timedelta} ..... {remindmsg}")
        if timedelta.endswith("s"):
            timedelta = datetime.datetime.now() + datetime.timedelta(seconds=int(timedelta[:-1]))
        elif timedelta.endswith("m"):
            timedelta = datetime.datetime.now() + datetime.timedelta(minutes=int(timedelta[:-1]))
        elif timedelta.endswith("h"):
            timedelta = datetime.datetime.now() + datetime.timedelta(hours=int(timedelta[:-1]))
        elif timedelta.endswith("d"):
            timedelta = datetime.datetime.now() + datetime.timedelta(days=int(timedelta[:-1]))
        elif timedelta.endswith("w"):
            timedelta = datetime.datetime.now() + datetime.timedelta(weeks=int(timedelta[:-1]))
        elif timedelta.endswith("mo") or timedelta.endswith("mon"):
            timedelta = datetime.datetime.now() + datetime.timedelta(weeks=4*int(timedelta[:-2]))
        elif timedelta.endswith("y"):
            timedelta = datetime.datetime.now() + datetime.timedelta(weeks=12*4*int(timedelta[:-1]))
        return timedelta, remindmsg


class Reminders:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remindme(self, ctx, *, msg: str):
        data = RemindParser.parseReminderMsg(msg)
        if data is None:
            return await ctx.send("Error parsing your reminder")
        Database.createReminder(ctx.author.id, ctx.message.channel.id, datetime.datetime.now(), data[0], data[1])
        return await ctx.send(f"OK {ctx.author.name}, I will remind you to {data[1]} at {data[0]}")

    @commands.command()
    async def getmyreminders(self, ctx):
        reminders = Database.getReminders(ctx.author.id)
        if len(reminders) > 1:
            embed = discord.Embed(title=f"{ctx.author.name} reminders")
            for reminder in reminders:
                embed.add_field(name=reminder[4], inline=False, value=f"expires at {reminder[3]}")
            return await ctx.send(embed=embed)
        elif len(reminders) == 1:
            return await ctx.send(f"{reminders[0][4]} at {reminders[0][3]}")
        else:
            return await ctx.send("You have no reminders set")

    async def checkExpiredReminders(self):
        await self.wait_until_ready()
        while not self.is_closed():
            expiredRems = Database.getExpired()
            if len(expiredRems) >= 1:
                for rem in expiredRems:
                    await self.get_channel(rem[1]).\
                        send(f"{self.get_user(rem[0]).mention}, you asked to be reminded to {rem[4]}")
                    Database.deleteReminder(rem[0], rem[2], rem[3], rem[4])
            await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(Reminders(bot))
    bot.loop.create_task(Reminders.checkExpiredReminders(bot))
