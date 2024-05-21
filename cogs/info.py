import discord
import datetime
import discord.ui
from discord.ext import commands
import psutil

class info(commands.Cog):
    def __init__(self, client):       
        self.client = client
        self.start_time = datetime.datetime.now()      

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info Is Ready")

    @commands.command(help="Shows the latency of the bot", usage = "Ping")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(description=f"My Latency is {round(self.client.latency*1000)} ms",colour=0x2b2d31)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['up'], help="Shows the uptime of the bot", usage = "Uptime")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uptime(self, ctx):    
        current_time = datetime.datetime.now()
        uptime = current_time - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
        embed = discord.Embed(description=f"Uptime: {uptime_str}",colour=0x2b2d31)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['inv'], help="Gives you the invite link of bot", usage = "Invite")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(description="Invite me to get the best quailty music.",colour=0x2b2d31)
        view = discord.ui.View()
        button = discord.ui.Button(label="Trick", url="https://discord.com/api/oauth2/authorize?client_id=1151088490583429142&permissions=554104613249&scope=bot%20applications.commands")
        view.add_item(button)
        await ctx.reply(embed=embed, mention_author=False, view=view)

    @commands.command(aliases=['sup'], help="Gives you the support server link", usage = "Support")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(self, ctx):
        embed = discord.Embed(description="Want help regarding the bot join our support.",colour=0x2b2d31)
        view = discord.ui.View()
        button = discord.ui.Button(label="Support", url="https://discord.gg/NH5qnRpbxh")
        view.add_item(button)
        await ctx.reply(embed=embed, mention_author=False, view=view)     

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vote(self, ctx):
        embed = discord.Embed(description="Thanks for your support! Our voting system is in the works.\nPlease hang tight, your patience means a lot!",colour=0x2b2d31)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
        await ctx.reply(embed=embed, mention_author=False)          

    @commands.command(aliases=['bi'], help="Shows the information of the bot", usage = "Stats")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stats(self, ctx):
        current_time = datetime.datetime.now() 
        uptime = current_time - self.start_time 
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        total_users = sum([i.member_count for i in self.client.guilds])
        uptime_str = f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"  
        embed = discord.Embed(color=0x2b2d31)
        embed.add_field(name='Client', value=f'Guilds: {len(self.client.guilds)}\nUsers: {total_users}\nLatency: {round(self.client.latency * 1000)} ms\nOnline Since: {uptime_str}\nShards: {self.client.shard_count}', inline=False)       
        embed.add_field(name='System', value=f'Ram Usage: {round(psutil.virtual_memory().used / 1e9, 2)} GB\nCPU Usage: {psutil.cpu_percent()}', inline=False)
        embed.set_footer(text="Trick Is Love", icon_url="https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.webp?size=80")
        await ctx.reply(embed=embed, mention_author=False)

async def setup(client):
    await client.add_cog(info(client))       