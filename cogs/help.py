import discord
import asyncio
import sqlite3
from discord.ext import commands

class MenuView(discord.ui.View):
    def __init__(self, author, timeout=30):
        super().__init__(timeout=timeout)
        self.author = author
        self.value = None  
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()        

    @discord.ui.select(placeholder="Make a selection", options=[
        discord.SelectOption(label="Music", value="music"),
        discord.SelectOption(label="Filter", value="filter"),
        discord.SelectOption(label="Info", value="info"),
        discord.SelectOption(label="Utility", value="utility"),
    ])
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("Sorry Bro, This is not your interaction.", ephemeral=True)
                return
            selected_values = select.values
            if selected_values and "music" in selected_values:
                embed = discord.Embed(colour=0x2b2d31, description="`Play`, `Pause`, `Resume`, `Stop`, `Queue`, `Volume`, `Skip`, `ClearQueue`, `DefaultVolume`, `Move`, `Join`, `Leave`, `NowPlaying`, `Forward`, `Rewind`, `Seek`, `Remove`")
                embed.set_author(name="Music Commands", icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text="Trick Is Love", icon_url='https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048')
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "filter" in selected_values:
                embed2 = discord.Embed(colour=0x2b2d31, description="`Vaporwave`, `Lofi`, `8d`, `Slowmo`, `BassBoost`, `China`, `Chipmunk`, `DarthVader`, `Demon`, `Funny`, `Karoke`, `NightCore`, `Pop`, `Soft`, `TrebleBass`, `Tremolo`, `Alien`, `Reset`")
                embed2.set_author(name="Filter Commands", icon_url=interaction.user.display_avatar.url)
                embed2.set_footer(text="Trick Is Love", icon_url='https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048')
                await interaction.response.edit_message(embed=embed2, view=self)
            elif selected_values and "info" in selected_values:
                embed3 = discord.Embed(colour=0x2b2d31, description="`Ping`, `Uptime`, `Invite`, `Support`, `Vote`, `Stats`, `Help`")
                embed3.set_author(name="Info Commands", icon_url=interaction.user.display_avatar.url)
                embed3.set_footer(text="Trick Is Love", icon_url='https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048')
                await interaction.response.edit_message(embed=embed3, view=self)
            elif selected_values and "utility" in selected_values:
                embed4 = discord.Embed(colour=0x2b2d31, description="`SetPrefix`, `Clean`, `Report`, `Ignore add`, `Ignore remove`, `Ignore Reset`")
                embed4.set_author(name="Utility Commands", icon_url=interaction.user.display_avatar.url)
                embed4.set_footer(text="Trick Is Love", icon_url='https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048')
                await interaction.response.edit_message(embed=embed4, view=self)
            select.placeholder = None 
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
            
    @discord.ui.button(label="Home", style=discord.ButtonStyle.secondary)
    async def home_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("Sorry Bro, This is not your interaction.", ephemeral=True)
                return
            cur = self.con.cursor()
            cur.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (interaction.guild.id,))
            server_prefix = cur.fetchone()
            prefix = server_prefix[0] if server_prefix else "+" 
            embed = discord.Embed(colour=0x2b2d31, description=f"• My prefix for this server is `{prefix}`\n• Total Commands `46`\n• [Trick](https://discord.com/api/oauth2/authorize?client_id=1151088490583429142&permissions=554104613249&scope=bot%20applications.commands) | [Support](https://discord.gg/NH5qnRpbxh)\n• Thanks for using Trick")
            embed.add_field(name="__Commands__", value=f"**Music\nFilters\nInfo\nUtility**")
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            embed.set_footer(text="Trick Is Love", icon_url="https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048")
            await interaction.response.edit_message(embed=embed, view=self)
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
           
            
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("Sorry Bro, This is not your interaction.", ephemeral=True)
                return
            await interaction.message.delete()
        except Exception as e:
            print(f"An error occurred: {e}")
            raise            
            
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()          

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Is Ready")    

    @commands.command(aliases=['h'], help="Shows the help command of the bot", usage = "Help")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, query=None):
        if query:
            command = self.client.get_command(query)
            if command:
                aliases = ", ".join(command.aliases)
                embed = discord.Embed(
                    colour=0x2b2d31, description=f"**{command.help}**"
                )
                embed.add_field(name="Aliases", value=f"`{aliases}`", inline=False)
                embed.add_field(name="Usage", value=f"`{command.usage}`", inline=False)
                embed.set_author(
                    name=ctx.author.name, icon_url=ctx.author.display_avatar.url
                )
                embed.set_thumbnail(url=ctx.author.display_avatar.url)
                embed.set_footer(text="Trick Is Love", icon_url="https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048")
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("Command not found.")
                return

        view = MenuView(ctx.author)
        cur = self.con.cursor()
        cur.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (ctx.guild.id,))
        server_prefix = cur.fetchone()
        prefix = server_prefix[0] if server_prefix else "+"
        embed = discord.Embed(colour=0x2b2d31, description=f"• My prefix for this server is `{prefix}`\n• Total Commands `46`\n• [Trick](https://discord.com/api/oauth2/authorize?client_id=1151088490583429142&permissions=554104613249&scope=bot%20applications.commands) | [Support](https://discord.gg/NH5qnRpbxh)\n• Thanks for using Trick")
        embed.add_field(name="__Commands__", value=f"**Music\nFilters\nInfo\nUtility**")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="Trick Is Love", icon_url="https://cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.png?size=2048")
        
        message = await ctx.reply(embed=embed, view=view, mention_author=False)

        try:
            await asyncio.sleep(view.timeout)
        except asyncio.CancelledError:
            pass
        else:
            for child in view.children:
                child.disabled = True
            await message.edit(embed=embed, view=view)

async def setup(client):
    await client.add_cog(Help(client))
