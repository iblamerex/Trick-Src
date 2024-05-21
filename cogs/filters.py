import discord
from discord.ext import commands
import wavelink
class Filters(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.filters = {}
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Filters Is Ready") 

    async def get_filter(self, filter_: str, guild_id):
        flt = self.filters.get(guild_id)
        if flt is None:
            return False
        return filter_.lower() in flt
    async def _filter(self, filter_name: str, guild_id):
        flt = self.filters.get(guild_id)
        if flt is None:
            self.filters[guild_id] = []
            self.filters[guild_id].append(filter_name.lower())
            return
        if str(filter_name).lower() in flt:
            self.filters[guild_id].remove(filter_name.lower())
        else:
            self.filters[guild_id].append(filter_name.lower())
    async def apply_filter(self, ctx, filter_name, filter_settings):
        vc: wavelink.Player = ctx.voice_client
        if not ctx.voice_client:
            embed1 = discord.Embed(description="I am not in any voice channel.", colour=0x2b2d31)
            return await ctx.reply(embed=embed1, mention_author=False)     
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=0x2b2d31)
            return await ctx.reply(embed=embed2, mention_author=False)      
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=0x2b2d31)
            return await ctx.reply(embed=embed3, mention_author=False)
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing anything.",colour=0x2b2d31)
            return await ctx.reply(embed=embed4, mention_author=False) 
        if vc.is_paused():
            embed6 = discord.Embed(description="I am currently paused please use `&resume`.",colour=0x2b2d31)
            return await ctx.reply(embed=embed6, mention_author=False)  
        flt = await self.get_filter(filter_name, ctx.guild.id)
        if not flt:
            await vc.set_filter(filter_settings)
            await self._filter(filter_name, ctx.guild.id)
            embed7 = discord.Embed(description=f"Set **{filter_name.capitalize()}** filter to the player.", color=0x2b2d31)
            await ctx.reply(embed=embed7, mention_author=False)
        else:
            await vc.set_filter(wavelink.Filter())
            await self._filter(filter_name, ctx.guild.id)
            embed8 = discord.Embed(description=f"Removed **{filter_name.capitalize()}** filter from the player.", color=0x2b2d31)
            await ctx.reply(embed=embed8, mention_author=False)  
    async def reset_filters(self, ctx, filter_names):
        vc: wavelink.Player = ctx.voice_client
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any voice channel.", colour=0x2b2d31)
            return await ctx.reply(embed=embed, mention_author=False)      
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=0x2b2d31)
            return await ctx.reply(embed=embed2, mention_author=False)      
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=0x2b2d31)
            return await ctx.reply(embed=embed3, mention_author=False)
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing anything.",colour=0x2b2d31)
            return await ctx.reply(embed=embed4, mention_author=False)     
        if vc.is_paused():
            embed5 = discord.Embed(description="I am currently paused please use `&resume`.",colour=0x2b2d31)
            return await ctx.reply(embed=embed5, mention_author=False)
        for filter_name in filter_names:
            flt = await self.get_filter(filter_name, ctx.guild.id)
            if flt:
                if filter_name in ['8d', 'tremolo']:
                    await vc.set_filter(wavelink.Filter(vc._filter, rotation=wavelink.Rotation(speed=0)))
                elif filter_name in ['bassboost', 'china', 'pop', 'soft', 'treblebass']:
                    await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer()))
                elif filter_name in ['karaoke']:
                    await vc.set_filter(wavelink.Filter(timescale=wavelink.Timescale()))
                else:
                    await vc.set_filter(wavelink.Filter())      
                await self._filter(filter_name, ctx.guild.id)
        embed6 = discord.Embed(description=f"All the filters have been reset.", color=0x2b2d31)
        await ctx.reply(embed=embed6, mention_author=False)

    @commands.command(aliases=['retro'], help="Music Like Retro", usage = "vaporwave")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vaporwave(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'vaporwave', wavelink.Filter(timescale=wavelink.Timescale(speed=0.7400040238419479, pitch=0.800000011920929, rate=1)))

    @commands.command(aliases=['classic'], help="Classic Music", usage = "lofi")  
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lofi(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'lofi', wavelink.Filter(timescale=wavelink.Timescale(speed=0.7300040238419479, pitch=0.860050011920929, rate=1), equalizer=wavelink.Equalizer(bands=[(0, -0.25), (1, -0.25)])))

    @commands.command(name="8d", aliases=['Rotation'], help="Surrounder Effect", usage = "8d") 
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8d(self, ctx: commands.Context):
        await self.apply_filter(ctx, '8d', wavelink.Filter(rotation=wavelink.Rotation(speed=0.0859884000491)))

    @commands.command(aliases=['slow'], help="Slowed Music", usage = "slowmo")   
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slowmo(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'slowmo', wavelink.Filter(timescale=wavelink.Timescale(speed=0.6800040238419479)))

    @commands.command(aliases=['bass'], help="Hear The Boosted Music", usage = "bassboost")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bassboost(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'bassboost', wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(5.0, 1.0), (10.0, 0.5)])))
    
    @commands.command(aliases=['chin'], help="Music Like Retro", usage = "china")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def china(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'china', wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(15.0, 0.0)])))

    @commands.command(aliases=['chips'], help="Hear The Chip's Sound", usage = "chipmunk")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chipmunk(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'chipmunk', wavelink.Filter(timescale=wavelink.Timescale(speed=1.5)))

    @commands.command(aliases=['breather'], help="Hear To Breather", usage = "darthvader")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def darthvader(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'darthvader', wavelink.Filter(timescale=wavelink.Timescale(speed=1.2, pitch=0.5)))

    @commands.command(aliases=['lucifer'], help="Hear To Demon", usage = "demon")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def demon(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'demon', wavelink.Filter(timescale=wavelink.Timescale(speed=0.8, pitch=0.5), equalizer=wavelink.Equalizer(bands=[(15.0, 0.0)])))

    @commands.command(aliases=['comd'], help="Unique Sounds", usage = "funny")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def funny(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'funny', wavelink.Filter(timescale=wavelink.Timescale(speed=1.2, pitch=0.7)))

    @commands.command(aliases=['singsong'], help="Music Along A Recorded One", usage = "karaoke")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def karaoke(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'karaoke', wavelink.Filter(timescale=wavelink.Timescale(speed=1.0, pitch=0.0)))

    @commands.command(aliases=['sped'], help="Hear The Sped-Up Music", usage = "nightcore")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nightcore(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'nightcore', wavelink.Filter(timescale=wavelink.Timescale(speed=1.5, pitch=1.5)))

    @commands.command(aliases=['bang'], help="Hip-Hop Music ", usage = "pop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pop(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'pop', wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(10.0, 0.5)])))

    @commands.command(aliases=['rfilters'], help="Removes All The Filters", usage = "reset")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reset(self, ctx: commands.Context):
        await self.reset_filters(ctx, ['slowmo', 'lofi', 'vaporwave', '8d', 'bassboost', 'china', 'chipmunk', 'darthvader', 'demon', 'funny', 'karaoke', 'nightcore', 'pop', 'soft', 'treblebass', 'tremolo'])

    @commands.command(aliases=['mushy'], help="Hear The Soft Music", usage = "soft")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def soft(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'soft', wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(0.0, 0.0), (15.0, 1.0)])))

    @commands.command(aliases=['deep'], help="Hear The High-Pitched Music", usage = "treblebass")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def treblebass(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'treblebass', wavelink.Filter(equalizer=wavelink.Equalizer(bands=[(0.0, 1.0), (15.0, -0.25)])))
    
    @commands.command(aliases=['tremble'], help="Hear The Trembling Music", usage = "tremolo")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tremolo(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'tremolo', wavelink.Filter(tremolo=wavelink.Tremolo(depth=0.5, frequency=4.0))) 

    @commands.command(aliases=['celestial'], help="Hear The Marshian Music", usage = "alien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def alien(self, ctx: commands.Context):
        await self.apply_filter(ctx, 'alien', wavelink.Filter(vibrato=wavelink.Vibrato(frequency=10.0 ,depth=0.9)))    

async def setup(client):
    await client.add_cog(Filters(client))          