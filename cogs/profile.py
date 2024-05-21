import discord
from discord.ext import commands

class profile(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.predefined_badges = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_predefined_badges()
        print("Profile Is Ready") 
   
    async def load_predefined_badges(self):
        roles_badges = {
            1216607053334974594: "<a:Trick_rex:1216607136994557985> [ReXx Qt](https://discordapp.com/users/910881343884390400/)",
            1214106672482615376: "<a:Trick_Owner:1205098796082532412> Owner",
            1214106867073294336: "<:Trick_Promoter:1205100364328607754> Promoters Team",
            1216605094477434950: "<:Trick_Team:1205109544775319562> Support Team",
            1214107020765167616: "<a:Trick_Partner:1205099040312655903> Partner",
            1215296337688535181: "<a:Trick_premium:1216607375361052803> Premium User",
            1214105601034944522: "<:Trick_Staff:1205100593388064799> Staff",
            1214109831989039105: "<a:Trick_Supporter:1205098748687028255> Supporter",
            1216604334595248128: "<:Trick_Bughunt:1205101080514666516> Bug Hunters",
            1214107823269744680: "<:Trick_Frined:1205100761969852436> Friend",
            1214106597131948073: "<a:Trick_User:1205098822762504234> User"
        }
        
        for guild in self.client.guilds:
            for role_id, emoji in roles_badges.items():
                role = guild.get_role(role_id)
                if role:
                    self.predefined_badges[role_id] = emoji

    async def fetch_predefined_badges(self, member):
        user_roles_badges = {}
        
        for guild in self.client.guilds:
            guild_member = guild.get_member(member.id)
            if guild_member:
                roles_with_positions = [(role.id, role.position) for role in guild_member.roles]
                sorted_roles = sorted(roles_with_positions, key=lambda x: x[1], reverse=True)
                user_roles_badges.update({role_id: self.predefined_badges[role_id] for role_id, _ in sorted_roles if role_id in self.predefined_badges})

        return user_roles_badges

    @commands.command(aliases=['pr'])
   
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, user: discord.User = None):
        target_user = user or ctx.author
        role_badges = await self.fetch_predefined_badges(target_user)
        role_display = "\n".join([f"{role_badges[role_id]}" for role_id in role_badges])

        if role_display:
            embed = discord.Embed(color=0x2b2d31, description=f"**__Badges__:\n{role_display}**")
            embed.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            embed.set_author(name=target_user.name, icon_url=target_user.display_avatar.url)
            embed.set_thumbnail(url=target_user.display_avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed2 = discord.Embed(description="Sorry but you don't have any badges please join our support server for badges.",colour=0x2b2d31)
            embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
            embed2.set_footer(text="Trick Is Love", icon_url=self.client.user.avatar.url)
            view = discord.ui.View()
            button = discord.ui.Button(label="Support", url="https://discord.gg/NH5qnRpbxh")
            view.add_item(button)
            await ctx.reply(embed=embed2, mention_author=False, view=view)

async def setup(client):
    await client.add_cog(profile(client))
