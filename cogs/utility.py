import discord
from discord.ext import commands
import sqlite3

class utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility Is Ready")        
        
    @commands.command(aliases=['prefix'], help="Changes the prefix of the bot", usage = "preifx <?>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def setprefix(self, ctx, prefix=None):
        cursor = self.con.cursor()
        cursor.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (ctx.guild.id,))
        p = cursor.fetchone()  
        if prefix is None:
            embed = discord.Embed(description=f"Please provide a prefix to update.",color=0x2b2d31)
            await ctx.reply(embed=jingle, mention_author=False)
            return     
        if len(prefix) > 2:
            embed2 = discord.Embed(description="Prefix cannot be greater than 2 characters.",color=0x2b2d31)
            await ctx.reply(embed=embed2, mention_author=False)
            return      
        cursor.execute(f"UPDATE Prefix SET prefix = ? WHERE guild_id = ?", (prefix, ctx.guild.id))
        embed3 = discord.Embed(description=f"Successfully set the prefix to `{prefix}`",color=0x2b2d31)
        await ctx.reply(embed=embed3, mention_author=False)
        self.con.commit()
        
    @commands.group(description="Ignore Commands", aliases=['ig'], invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def ignore(self, ctx):
        await ctx.send("")    
        
    @ignore.command(name="add")
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def embed_add(self, ctx, channel: discord.TextChannel):
        self.cur.execute('SELECT COUNT(*) FROM ignored_channels WHERE guild_id = ?', (ctx.guild.id,))
        ignored_count = self.cur.fetchone()[0]
        limit = 1
        
        if ignored_count >= limit:
            embed = discord.Embed(description=f"You cannot ignore more than `{limit}` channel.",color=0x2b2d31)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        
        self.cur.execute('SELECT * FROM ignored_channels WHERE guild_id = ? AND channel_id = ?', (ctx.guild.id, channel.id))
        ignored = self.cur.fetchone()
        
        if ignored:
            embed2 = discord.Embed(description=f"**{channel.name}** is already present in my ignore list.",color=0x2b2d31)
            embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed2.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed2, mention_author=False)
        else:
            self.cur.execute('INSERT INTO ignored_channels (guild_id, channel_id) VALUES (?, ?)', (ctx.guild.id, channel.id))
            self.con.commit()
            embed3 = discord.Embed(description=f"I will now ignore all messages in **{channel.name}**",color=0x2b2d31)
            embed3.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed3.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed3, mention_author=False)

    @ignore.command(name="remove")
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def embed_remove(self, ctx, channel: discord.TextChannel):
        self.cur.execute('SELECT * FROM ignored_channels WHERE guild_id = ? AND channel_id = ?', (ctx.guild.id, channel.id))
        ignored = self.cur.fetchone()
        
        if ignored:
            self.cur.execute('DELETE FROM ignored_channels WHERE guild_id = ? AND channel_id = ?', (ctx.guild.id, channel.id))
            self.con.commit()
            embed = discord.Embed(description=f"I will no longer ignore messages in **{channel.name}**", color=0x2b2d31)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
            
        else:
            embed2 = discord.Embed(description=f"**{channel.name}** is not present in my ignore list.", color=0x2b2d31)
            embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed2.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed2, mention_author=False)
            
    @ignore.command(name="reset")
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def embed_reset(self, ctx):
        self.cur.execute('SELECT * FROM ignored_channels WHERE guild_id = ?', (ctx.guild.id,))
        ignored = self.cur.fetchall()
        
        if ignored:
            self.cur.execute('DELETE FROM ignored_channels WHERE guild_id = ?', (ctx.guild.id,))
            self.con.commit()
            
            embed = discord.Embed(description="All channels have been removed from the ignore list for this guild.", color=0x2b2d31)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed2 = discord.Embed(description="There are no channels in the ignore list for this guild.", color=0x2b2d31)
            embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed2.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            await ctx.reply(embed=embed2, mention_author=False)

    @commands.command(aliases=['purge'], help="Purge the message of trick", usage = "Clean")
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check_any(commands.is_owner(), commands.has_permissions(manage_messages=True))
    async def clean(self, ctx):
            bot_messages = [message async for message in ctx.channel.history(limit=100) if message.author == self.client.user]
            await ctx.channel.delete_messages(bot_messages)
            embed = discord.Embed(description=f"Cleared {len(bot_messages)} bot messages.", color=0x2b2d31)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            response_message = await ctx.reply(embed=embed, mention_author=False, delete_after=3)
    
    @commands.command(help="You can send your issue to HQ server", usage="Report <Your Issue>")
    @commands.cooldown(1, 10 * 60, commands.BucketType.user) 
    async def report(self, ctx, *issue):
       if not issue: 
        report = discord.Embed(
            description="You are missing a required argument for the command report.",
            color=0x2b2d31)
        return await ctx.send(embed=report)
    
       issue_text = ' '.join(issue)

       embed = discord.Embed(title='New Issue Report', description=f'**Issue:** {issue_text}', color=0x2b2d31)
       embed.add_field(name='User', value=f'{ctx.author.name}#{ctx.author.discriminator} (ID: {ctx.author.id})', inline=False)
       embed.add_field(name='Server', value=f'{ctx.guild.name} (ID: {ctx.guild.id})', inline=False)
    
       try:
          invite = await ctx.channel.create_invite(max_age=86400)
          embed.add_field(name='Channel', value=f'{ctx.channel.name} (ID: {ctx.channel.id})', inline=False)
          embed.add_field(name='Server Invite', value=f'https://discord.gg/{invite.code}', inline=False)
       except discord.errors.Forbidden:
          embed.add_field(name='Channel', value=f'{ctx.channel.name} (ID: {ctx.channel.id})', inline=False)
          embed.add_field(name='Server Invite', value='None', inline=False)

       log_channel_id = 1202479503025373184
       log_channel = self.client.get_channel(log_channel_id)
       await log_channel.send(embed=embed)

       embed2 = discord.Embed(description="Your issue has been reported. You can join the support server for further assistance.", colour=0x2b2d31)
       embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
       embed2.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
       view = discord.ui.View()
       button = discord.ui.Button(label="Support", url="https://discord.gg/NH5qnRpbxh")
       view.add_item(button)
       await ctx.reply(embed=embed2, mention_author=False, view=view)

    

async def setup(client):
    await client.add_cog(utility(client))