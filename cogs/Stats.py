import asyncio
import discord
import json
from urllib.request import urlopen, Request
from discord.ext import commands
jsontoenglish = {"wins": "Wins", "has_played": "Ever Played", "losses": "Losses", "kills": "Kills", "deaths": "Deaths",
                 "playtime": "Playtime", "kd": "Kill/Death Ratio", "wlr": "Win/Loss Ratio", "assists": "Assists",
                 "barricades_built": "Barricades Built", "bullets_fired": "Bullets Fired", "bullets_hit": "Bullets Hit",
                 "headshots": "Headshots", "melee_kills": "Melee Kills", "penetration_kills": "Penetration Kills",
                 "reinforcements_deployed": "Reinforcements Deployed", "revives": "Revives",
                 "steps_moved": "Steps Moved", "suicides": "Suicides", True: "Hell Yeah", False: "Never ever"}


class Stats:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def r6stats(self, ctx, player: str=None, platform: str='uplay'):
        if player is None:
            return await ctx.send("Error: Need a proper username")
        stats = json.loads(urlopen(Request('https://api.r6stats.com/api/v1/players/{}?platform={}'
                                           .format(player, platform), headers={'User-Agent': 'Mozilla/5.0'})).read()
                           .decode("utf-8"))
        if 'status' in stats:
            return await ctx.send(stats['errors'][0]['detail'])
        embed = discord.Embed(title="Stats for {} who also happens to be level {}"
                              .format(stats['player']["username"], stats['player']['stats']['progression']['level']))
        embed.add_field(name="Ranked Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['ranked']:
            if type(stats['player']['stats']['ranked'][x]) is not bool:
                embed.add_field(name=jsontoenglish[x], value=stats['player']['stats']['ranked'][x])
            else:
                embed.add_field(name=jsontoenglish[x], value=jsontoenglish[stats['player']['stats']['ranked'][x]])
        embed.add_field(name="Casual Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['casual']:
            if type(stats['player']['stats']['casual'][x]) is not bool:
                embed.add_field(name=jsontoenglish[x], value=stats['player']['stats']['casual'][x])
            else:
                embed.add_field(name=jsontoenglish[x], value=jsontoenglish[stats['player']['stats']['casual'][x]])
        embed.add_field(name="Overall Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['overall']:
            embed.add_field(name=jsontoenglish[x], value=stats['player']['stats']['overall'][x])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stats(bot))
