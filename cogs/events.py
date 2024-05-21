import discord
from discord.ext import commands
import aiohttp
import sqlite3
import datetime
import time
import asyncio

class events(commands.Cog):
    def __init__(self, client):
        self.client = client  
        self.value = None  
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()  
        self.start_time = datetime.datetime.now()  
        self.cooldowns = {}      

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Is Ready")
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if len(guild.members) < 30:
            # Send a message to the guild explaining the condition
            embed = discord.Embed(
                title="Important Message",
                description="You cannot add me if your server has less than 30 members.\nSince this server has less than 30 members, I have to leave this server.\n\nFor any queries related to the bot please join our [Support Server](https://discord.gg/NH5qnRpbxh)",
                color=0xFF5733
            )
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(embed=embed)
                    break  # Stop after sending the message to one channel
            # Leave the guild
            await guild.leave()
            
        else:
            invite = await guild.text_channels[0].create_invite(max_age=604800, max_uses=0)
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159374625275945/rs42YiWBHa590Dw553aOSUjKL1pDVFh4sTvq_GKuF1tTAb-Cd9qsWd5TrYFScssdqGXK",session=session)
                embed = discord.Embed(title="Joined A Guild", description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Invite Link:** {invite.url}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>", color=0x2b2d31)    
                await webhook.send(embed=embed)     
            
    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214159429751017512/3NfkaefZIs9CnjA_pnP1eHb_rf83KyypYb5EvbfQcqo408fDU5M4CoiXzIfpuWHTi6iy",session=session)
                embed = discord.Embed(title="Left A Guild", description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>", color=0x2b2d31)
                await webhook.send(embed=embed)    


    @commands.Cog.listener()
    async def on_command(self, ctx):
        server_name = ctx.guild.name if ctx.guild else "DMs"
        server_id = ctx.guild.id if ctx.guild else None
        channel_id = ctx.channel.id
        user = ctx.author
        command_content = ctx.message.content  # Get the content of the message that triggered the command
        command_time = datetime.datetime.now()  # Capture the time when the command is run
        uptime = command_time - self.start_time  # Calculate the uptime
        total_seconds = int(uptime.total_seconds())
        uptime_timestamp = int(command_time.timestamp())
        uptime_str = f"<t:{uptime_timestamp}:R>"

        async with aiohttp.ClientSession() as session:
         webhook = discord.Webhook.from_url(url="https://discord.com/api/webhooks/1214497172536426556/H4d_cMlze9bfVAfjsPgiU5-4cCf8IW82Aw43ZnxNVoyU2UENDAm3HL9cYyYixuPSfVZY", session=session)
         embed = discord.Embed(
            title="Command",
            description=f"```{command_content}```\n**Server Name:** {server_name}\n\n **Server ID:** `{server_id}`\n\n**Channel ID:** `{channel_id}`\n<#{channel_id}>\n\n**User:** {user.mention}\n\n**Time:** {uptime_str}",
            color=0x2b2d31
         )
         await webhook.send(embed=embed)
                 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore messages from bots

        # Check if user is on cooldown
        if message.author.id in self.cooldowns:
            remaining_time = self.cooldowns[message.author.id] - time.time()
            if remaining_time > 3:
                return

        if message.content == self.client.user.mention:
            cur = self.con.cursor()
            cur.execute("SELECT prefix FROM Prefix WHERE guild_id = ?", (message.guild.id,))
            server_prefix = cur.fetchone()
            prefix = server_prefix[0] if server_prefix else "&"

            embed = discord.Embed(
                description=f"**Hey {message.author.mention}\n My prefix here is `{prefix}` \n Server ID: `{message.guild.id}` \n \n Type `{prefix}help` To Get The Command List**",
                color=0x2b2d31
            )
            embed.set_thumbnail(url=message.author.avatar)
            embed.set_footer(
                text="Trick is Love",
                icon_url="https://images-ext-2.discordapp.net/external/rG0vSVueMS2yUkfj0XColYR2AkuaoQSEgveBXHZlaoY/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/1151088490583429142/1ab05dfc8fc187202acc6e37184734dc.webp?format=webp&width=440&height=440"
            )
            embed.set_author(name=message.author.name,
                             icon_url=message.author.display_avatar.url)

            
            support_button = discord.ui.Button(label="Support", url="https://discord.gg/NH5qnRpbxh")

           
            invite_link = discord.utils.oauth_url(self.client.user.id, permissions=discord.Permissions(permissions=554104613249))
            invite_button = discord.ui.Button(label="Invite", url=invite_link)

            # Set the color of the embed
            embed.color = 0x2b2d31

            # Create a view and add the buttons to it
            view = discord.ui.View().add_item(invite_button).add_item(support_button)

            # Send the message with the embed and the buttons
            await message.reply(embed=embed, view=view, mention_author=False)

            # Add user to cooldown
            self.cooldowns[message.author.id] = time.time() + 5  # Cooldown duration
            await asyncio.sleep(5)  # Cooldown duration
            del self.cooldowns[message.author.id]  # Remove user from cooldown after cooldown duration


            # Set the color of the embed
            #embed.color = 0x2b2d31

            # Create a view and add the buttons to it
            #view = discord.ui.View().add_item(invite_button).add_item(support_button)

            # Send the message with the embed and the buttons
            #await message.reply(embed=embed, view=view, mention_author=False)
            
                       
async def setup(client):
    await client.add_cog(events(client))        