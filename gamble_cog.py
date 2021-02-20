from discord.ext import commands
import discord
from random import randint
import json


class GambleBot(commands.Cog):
    """GambleBot is a discord Cog that handle a points gambling system
       A member can gamble his guild points in order to gain ranks
    """
    def __init__(self):
        self.db = "./data/data.json"
        self.default_points = 2000

    @commands.is_owner()
    @commands.command()
    async def init(self, ctx):
        """Initialize gambling database [OWNER ONLY]"""
        data = {}
        data['members'] = []
        for member in ctx.guild.members:
            if member.nick:
                data['members'].append({
                    'name': member.nick,
                    'id': member.id,
                    'points': self.default_points
                })
            else:
                data['members'].append({
                    'name': member.name,
                    'id': member.id,
                    'points': self.default_points
                })
        with open(self.db, 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send("Gambling database have been initialized !")

    @commands.command()
    async def refresh(self, ctx):
        """Refresh the database with updated members information
           If a new member have joined the server it will add it
           If a member have left the server it will remove him
        """
        removed = 0
        added = 0
        with open(self.db, 'r') as f:
            data = json.load(f)
        for member in data['members']:
            if member['id'] not in [i.id for i in ctx.guild.members]:
                data['members'].remove(member)
                print("[INFO] An old member {0} have been removed from the database".format(member['name']))
                removed += 1

        for member in ctx.guild.members:
            if member.id not in [i['id'] for i in data['members']]:
                name = ""
                if member.nick:
                    data['members'].append({
                        'name': member.nick,
                        'id': member.id,
                        'points': self.default_points,
                    })
                    name = member.nick
                else:
                    data['members'].append({
                        'name': member.name,
                        'id': member.id,
                        'points': self.default_points,
                    })
                    name = member.name
                print("[INFO] New member {0} have been added to the database".format(name))
                added += 1

        with open(self.db, 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send("Database have been refresh :\n```- {0} old members removed\n- {1} new members added```".format(removed, added))

    @commands.command()
    async def gamble(self, ctx, *, points: int):
        """Gamble a defined amount of points"""
        data = []
        if points <= 0:
            return await ctx.send("{0} You can only gamble `< 0` values...".format(ctx.message.author.mention))
        with open(self.db, 'r') as f:
            data = json.load(f)
            result = next(filter(lambda res: res[1]['id'] == ctx.message.author.id, enumerate(data['members'])))
        total_points = result[1]['points']
        if total_points == 0:
            return await ctx.send("{0} You cannot gamble with {1} points...".format(ctx.message.author.mention, total_points))
        if total_points < points:
            return await ctx.send("{0} You cannot gamble {1} points with {2} points left...".format(ctx.message.author.mention, points, total_points))
        rand = randint(1, 10)
        if rand < 5:
            total_points -= points
            if total_points < 0:
                total_points = 0
            await ctx.send("{0} Oh crap, you lost {1} points...".format(ctx.message.author.mention, points))
        elif rand > 5:
            total_points += points
            await ctx.send("{0} Great, you won {1} points !".format(ctx.message.author.mention, points))
        else:
            total_points = total_points
            await ctx.send("{0} You've kind of won, you keep your {1} points !".format(ctx.message.author.mention, points))
        result[1]['points'] = total_points
        data['members'][result[0]].update(result[1])

        with open(self.db, 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send("{0} You have currently {1} points".format(ctx.message.author.mention, result[1]['points']))

    @commands.command()
    async def points(self, ctx):
        """Get member's points"""
        data = []
        with open(self.db, 'r') as f:
            data = json.load(f)
            result = next(filter(lambda res: res[1]['id'] == ctx.message.author.id, enumerate(data['members'])))
        await ctx.send("{0} You have currently {1} points".format(ctx.message.author.mention, result[1]['points']))

    @commands.is_owner()
    @commands.command()
    async def give(self, ctx, points: int, *, username: str):
        """Give points to a specific member [OWNER ONLY]"""
        data = []
        if points <= 0:
            return await ctx.send("{0} You can only give `< 0` values...".format(ctx.message.author.mention))
        member = discord.utils.get(ctx.guild.members, nick=username)
        if not member:
            member = discord.utils.get(ctx.guild.members, name=username)
            if not member:
                return await ctx.send("Could not find member's user or nickname '{0}'".format(username))
        with open(self.db, 'r') as f:
            data = json.load(f)
            result = next(filter(lambda res: res[1]['id'] == member.id, enumerate(data['members'])))
        result[1]['points'] += points
        data['members'][result[0]].update(result[1])
        with open(self.db, 'w') as f:
            json.dump(data, f, indent=2)
        await ctx.send("{0} gave {1} {2} points !".format(ctx.message.author.mention, username, points))

    @commands.command()
    async def top(self, ctx):
        """Get top ranked member"""
        data = []
        with open(self.db, 'r') as f:
            data = json.load(f)
            list_points = [x['points'] for x in data['members']]
            max_index = list_points.index(max(list_points))
            max_member = data['members'][max_index]
        await ctx.send("Top member is {0} with {1} points !".format(max_member['name'], max_member['points']))

    @commands.command()
    async def rank(self, ctx):
        """Get member's rank"""
        data = []
        with open(self.db, 'r') as f:
            data = json.load(f)
            sort = sorted(data['members'], key=lambda member: member['points'], reverse=True)
            member = next(filter(lambda res: res[1]['id'] == ctx.message.author.id, enumerate(sort)))
            rank = member[0] + 1
        await ctx.send("Your rank is {0} over {1} members !".format(rank, len(sort)))
