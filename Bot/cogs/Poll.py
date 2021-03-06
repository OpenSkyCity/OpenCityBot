import json

import discord
from discord.ext import commands


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return True
        if await self.bot.is_owner(ctx.author):
            return True
        guild_data = json.load(open(self.bot.guilds_json))
        enabled = guild_data[str(ctx.guild.id)]["enabled"]
        if f"Bot.cogs.{self.qualified_name}" in enabled:
            return True
        return False

    @commands.command(help="Creates a polls with a question and answer.", usage="<question_and_answer_separated_by_commas_or_pipes>")
    async def polls(self, ctx: commands.Context, *, q_and_a):
        question = str(q_and_a).split(", " if ", " in q_and_a else "| ")[0]
        answers = str(q_and_a).split(", " if ", " in q_and_a else "| ")[1:]
        embed = discord.Embed()
        reply = ''
        for answer_index, answer in enumerate(answers):
            answer_index += 1
            reply += f"{answer_index}\N{variation selector-16}\N{combining enclosing keycap} : {answer} \n"
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.title = f"{ctx.author.name}#{ctx.author.discriminator} asks {question}"
        embed.description = reply
        embed.colour = discord.Colour.teal()
        message = await ctx.send(embed=embed)
        for answer_index in range(len(answers)):
            answer_index += 1
            await message.add_reaction(f"{answer_index}\N{variation selector-16}\N{combining enclosing keycap}")


def setup(bot):
    bot.add_cog(Poll(bot))
