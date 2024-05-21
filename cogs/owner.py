import discord
from discord.ext import commands
import sqlite3
import aiohttp

def extraowner():
    async def predicate(ctx: commands.Context):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()  
            cur.execute("SELECT user_id FROM Owner")
            ids_ = cur.fetchall()
            if ctx.author.id in [i[0] for i in ids_]:
                return True
            else:
                return False
    return commands.check(predicate)  

class owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Owner Is Ready")  
        
    @commands.group(hidden=True, invoke_without_command=True)
    @commands.is_owner()
    async def owner(self, ctx):
        await ctx.reply("") 

    @owner.command(name="add")
    @commands.is_owner()
    async def ownerkrdu(self, ctx, user: discord.User):
        c = self.con.cursor()
        c.execute("SELECT user_id FROM Owner")
        re = c.fetchall()
        if re != []:
            ids = [int(i[0]) for i in re]
            if user.id in ids:
                embed = discord.Embed(description=f"That user is already in owner list.", color=0x2b2d31)
                await ctx.reply(embed=embed, mention_author=False)
                return
        c.execute("INSERT INTO Owner(user_id) VALUES(?)", (user.id,))
        embed2 = discord.Embed(description=f"Successfully added **{user}** in owner list..", color=0x2b2d31)
        await ctx.reply(embed=embed2, mention_author=False)
        self.con.commit()

    @owner.command(name="remove")
    @commands.is_owner()
    async def ownerhatadu(self, ctx, user: discord.User):
        c = self.con.cursor()
        c.execute("SELECT user_id FROM Owner")
        re = c.fetchall()
        if re == []:
            embed = discord.Embed(description=f"That user is not in owner list.", color=0x2b2d31)
            await ctx.reply(embed=embed, mention_author=False)
            return
        ids = [int(i[0]) for i in re]
        if user.id not in ids:
            embed2 = discord.Embed(description=f"That user is not in owner list.", color=0x2b2d31)
            await ctx.reply(embed=embed2, mention_author=False)
            return
        c.execute("DELETE FROM Owner WHERE user_id = ?", (user.id,))
        embed3 = discord.Embed(description=f"Successfully removed **{user}** from owner list.", color=0x2b2d31)
        await ctx.reply(embed=embed3, mention_author=False)
        self.con.commit() 

    @commands.group(description="Noprefix Commands", aliases=['np'], invoke_without_command=True, hidden=True)
    @commands.check_any(commands.is_owner(), extraowner())    
    async def noprefix(self, ctx):
        await ctx.reply("") 

    @noprefix.command(name="add", description="Adds a user to noprefix.")
    @commands.check_any(commands.is_owner(), extraowner())
    async def noprefix_add(self, ctx, user: discord.User):
        cursor = self.con.cursor()
        cursor.execute("SELECT users FROM Np")
        result = cursor.fetchall()
        if user.id not in [int(i[0]) for i in result]:
            cursor.execute(f"INSERT INTO Np(users) VALUES(?)", (user.id,))
            embed1 = discord.Embed(description=f"Successfully added **{user}** to no prefix.", color=0x2b2d31)
            await ctx.reply(embed=embed1, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159474349314108/QQ5DLOussLaxBfZiRzvjnIn4s5FCKKWgoU8BNCMTSEFQhd4_rlkxcfuHDy2mvUmJXKpL", session=session)
                embed2 = discord.Embed(title="No Prefix Added", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=0x2b2d31)
                await webhook.send(embed=embed2)
        else:
            embed3 = discord.Embed(description=f"That user is already in no prefix.", color=0x2b2d31)
            await ctx.reply(embed=embed3, mention_author=False)
        self.con.commit()

    @noprefix.command(name="remove",description="Removes a user from noprefix.")
    @commands.check_any(commands.is_owner(),extraowner())
    async def noprefix_remove(self, ctx, user: discord.User):
        cursor = self.con.cursor()
        cursor.execute("SELECT users FROM Np")
        result = cursor.fetchall()
        if user.id in [int(i[0]) for i in result]:
            cursor.execute(f"DELETE FROM Np WHERE users = ?", (user.id,))
            embed1 = discord.Embed(description=f"Successfully removed **{user}** from no prefix.", color=0x2b2d31)
            await ctx.reply(embed=embed1, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159474349314108/QQ5DLOussLaxBfZiRzvjnIn4s5FCKKWgoU8BNCMTSEFQhd4_rlkxcfuHDy2mvUmJXKpL",session=session)
                embed2 = discord.Embed(title="Noprefix Removed", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=0x2b2d31)
                await webhook.send(embed=embed2)  
        else:
            embed3 = discord.Embed(description=f"That user isn't in no prefix.", color=0x2b2d31)
            await ctx.reply(embed=embed3, mention_author=False)
        self.con.commit()

    @commands.group(description="Blacklist Commands", invoke_without_command=True)
    @commands.check_any(commands.is_owner())
    async def bl(self, ctx):
        await ctx.send("") 

    @bl.command(name="add")
    @commands.check_any(commands.is_owner())
    async def bl_add(self, ctx, user: discord.User):
      excluded_users = [760143551920078861, 910881343884390400]
      if user.id in excluded_users:
        await ctx.send("You cannot blacklist your dady.")
        return

      self.cur.execute('SELECT * FROM blacklist WHERE user_id = ?', (user.id,))
      blacklisted = self.cur.fetchone()    
      if blacklisted:
        embed1 = discord.Embed(description=f"**{user.name}** is already in the blacklist.", color=0x2b2d31)
        await ctx.reply(embed=embed1, mention_author=False)
      else:
        self.cur.execute('INSERT INTO blacklist (user_id) VALUES (?)', (user.id,))
        self.con.commit()
        embed2 = discord.Embed(description=f"I will now ignore messages from **{user.name}**", color=0x2b2d31)
        await ctx.reply(embed=embed2, mention_author=False)
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159535799803924/Boh_RzybkA6vFgF7SQDbmS6wsnvSpReMkgBrqeFQ_7dNGLR0oWMvEsKCf1aH0YoekDt4", session=session)
            embed3 = discord.Embed(title="Blacklist Added", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})", color=0x2b2d31)
            await webhook.send(embed=embed3)
  

    @bl.command(name="remove")
    @commands.check_any(commands.is_owner())
    async def bl_remove(self, ctx, user: discord.User):
        self.cur.execute('SELECT * FROM blacklist WHERE user_id = ?', (user.id,))
        blacklisted = self.cur.fetchone()
        if blacklisted:
            self.cur.execute('DELETE FROM blacklist WHERE user_id = ?', (user.id,))
            self.con.commit()        
            embed1 = discord.Embed(description=f"I will no longer ignore messages from **{user.name}**", color=0x2b2d31)
            await ctx.reply(embed=embed1, mention_author=False)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159535799803924/Boh_RzybkA6vFgF7SQDbmS6wsnvSpReMkgBrqeFQ_7dNGLR0oWMvEsKCf1aH0YoekDt4",session=session)
                embed3 = discord.Embed(title="Blacklist Removed", description=f"**Action By:** {ctx.author} ({ctx.author.id})\n**User:** {user} ({user.id})",color=0x2b2d31)
                await webhook.send(embed=embed3)          
        else:
            embed2 = discord.Embed(description=f"**{user.name}** is not in the blacklist.", color=0x2b2d31)
            await ctx.reply(embed=embed2, mention_author=False)

    @commands.command()
    @commands.is_owner()
    async def gleave(self, ctx, guild: discord.Guild):
        await guild.leave()  
        await ctx.send("Done !") 
        
    @commands.command(name="guildinvite", aliases=["ginv"])
    @commands.is_owner()
    async def invite_to_guild(self, ctx, guild_id: int):
        guild = self.client.get_guild(guild_id)
        if guild:
            invite_link = await guild.text_channels[0].create_invite(max_age=604800, max_uses=0)
            await ctx.send(f"Here's the invite link to the server: {invite_link}")
        else:
            await ctx.send("Could not find a server with the provided ID.")        
        
async def setup(client):
    await client.add_cog(owner(client))