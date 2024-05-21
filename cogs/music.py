import discord
import wavelink , asyncio
from collections import deque
import re
from discord.ext import commands
import Trick
from wavelink.ext import spotify

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queuee = deque()
        self.color = Trick.color
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Is Ready")
    
    @commands.command(aliases=['p'], help="Play Some Music!", usage = "play <query>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query):
        try:
          vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, reconnect=True, self_deaf=True)
        except:
          vc: wavelink.Player = ctx.voice_client
        if vc is None:
           embed1 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
           return await ctx.reply(embed=embed1, mention_author=False)
        if ctx.author.voice.channel != vc.channel: 
            embed2 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused please use `+resume`.",colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)          
        url_pattern = r'(https?://\S+)'
        urls = re.findall(url_pattern, query)
        if urls:
            return await ctx.send(embed=discord.Embed(description='Links are not supported', color=self.color), delete_after=3)
        else:
            tracks = await wavelink.YouTubeTrack.search(query)
            if tracks == []:
                embed5 = discord.Embed(description=f'No songs were found with that query.',colour=self.color)
                return await ctx.reply(embed=embed5, mention_author=False)
            track_ = [track for track in tracks if track.length/1000 > 10]
            track = track_[0] if track_ else None
            if not vc.is_playing():
                await vc.play(track)
                vc.autoplay = True
                vc.ctx = ctx
            else:
                if len(list(vc.queue)) >= 10:
                    embed6 = discord.Embed(description="More songs cannot be added to the queue.",colour=self.color)
                    return await ctx.reply(embed=embed6, mention_author=False) 
                await vc.queue.put_wait(track)
                embed7 = discord.Embed(description=f"Added **[{track.title}]({Trick.support_link})** to the queue.",colour=self.color)
                await ctx.reply(embed=embed7, mention_author=False)

    @commands.Cog.listener('on_wavelink_track_end')
    async def PlayerEnd(self, player_: wavelink.Player):
        player = player_.player
        try:
            await player.ctx.msg.delete()
        except: pass
        try:
            await player.msg.delete()
        except: pass

    @commands.Cog.listener('on_wavelink_track_start')
    async def PlayerStart(self, payload: wavelink.TrackEventPayload) -> None:
        player: wavelink.Player = payload.player
        track = payload.track
        length_seconds = round(track.length) / 1000
        hours, remainder = divmod(length_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        embed = discord.Embed(description=f"Started Playing [{track.title}]({Trick.support_link})・[{duration_str}]({Trick.support_link})", colour=self.color)
        msg = await player.ctx.send(embed=embed, mention_author=False)
        player.ctx.msg = msg

    @commands.command(aliases=['wait'], help="Pause The Playing Music!", usage = "pause")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)
        else:
            vc: wavelink.Player = ctx.voice_client
            if ctx.author.voice.channel != vc.channel:
                embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
                return await ctx.reply(embed=embed3, mention_author=False)         
            if not vc.is_playing():
                embed4 = discord.Embed(description="I am not playing anything.",colour=self.color)
                return await ctx.reply(embed=embed4, mention_author=False)  
            await vc.pause()
            embed5 = discord.Embed(description="Sucessfully Paused the player.",colour=self.color)
            await ctx.reply(embed=embed5, mention_author=False)

    @commands.command(aliases=['begin'], help="Resume the Current Music!", usage = "resume")
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def resume(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)        
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)       
        else:
            vc: wavelink.Player = ctx.voice_client
            if ctx.author.voice.channel != vc.channel:
                embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
                return await ctx.reply(embed=embed3, mention_author=False)            
            if  vc.is_paused():
                await vc.resume()
                embed4 = discord.Embed(description="Resuming the player now <3",colour=self.color)
                return await ctx.reply(embed=embed4, mention_author=False) 
            if not vc.is_playing():
                embed5 = discord.Embed(description="I am not playing anything.",colour=self.color)
                return await ctx.reply(embed=embed5, mention_author=False) 
            


    @commands.command(aliases=['dc'], help="Stop The Music", usage = "stop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)        
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)       
        else:
            vc: wavelink.Player = ctx.voice_client
            if ctx.author.voice.channel != vc.channel:
                embed3 = discord.Embed(description="You are in not the same voice channel.", colour=self.color)
                return await ctx.reply(embed=embed3, mention_author=False)            
            if self.queuee:
                self.queuee.clear()
            await vc.stop()
            await vc.disconnect()
            embed4 = discord.Embed(description="Stopped and Disconnected :/ ",colour=self.color)
            await ctx.reply(embed=embed4, mention_author=False)

    @commands.command(aliases=['q'], help="Look Into The Queue", usage = "queue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any vc.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)     
        if ctx.voice_client is None:
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)
        vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            embed3 = discord.Embed(description="I am not playing any song.",colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)       
        if ctx.author.voice.channel != vc.channel:
            embed4 = discord.Embed(description="You are in not the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)
        queue = enumerate(list(vc.queue), start=1)
        track_list = '\n'.join(f'[{num}] {track.title}' for num, track in queue)
        length_seconds = round(vc.current.length) / 1000
        hours, remainder = divmod(length_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        embed5 = discord.Embed(description=f'**__Now Playing__**\n  [{vc.current.title}]({Trick.support_link})・[{duration_str}]({Trick.support_link})\n\n```\n{track_list}```',color=self.color)
        await ctx.reply(embed=embed5, mention_author=False)

    @commands.command(aliases=['vol'], help="Change The Volume", usage = "Volume")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def volume(self, ctx: commands.Context, volume: int):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)      
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)     
        vc: wavelink.Player = ctx.voice_client
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)                
        if not vc.is_playing:
            embed4 = discord.Embed(description="I am not playing anything.",colour=self.color)
            await ctx.reply(embed=embed4, mention_author=False)
            return 
        if not 0 <= volume <= 2000:
            embed5 = discord.Embed(description="Please provide a volume to set in between 0 to 200.",colour=self.color)
            await ctx.reply(embed=embed5, mention_author=False)
            return        
        await vc.set_volume(volume)
        embed6 = discord.Embed(description=f"Volume set to {volume}%",colour=self.color)
        await ctx.reply(embed=embed6, mention_author=False) 
    @commands.command(aliases=['s'], help="Plays The Next Track", usage = "skip")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx: commands.Context):
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            embed = discord.Embed(description="I am not in any voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)      
        elif not ctx.author.voice:
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)        
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False) 
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing anything.",colour=self.color)
            await ctx.reply(embed=embed4, mention_author=False)
            return        
        await vc.stop()
        embed5 = discord.Embed(description="Skipped the current song.",colour=self.color)
        await ctx.reply(embed=embed5, mention_author=False)
        if vc.queue:
            track = vc.queue.popleft()
            await vc.play(track)
            embed6 = discord.Embed(description=f"Started playing: [{track.title}]({Trick.support_link})",colour=self.color)
            await ctx.reply(embed=embed6, mention_author=False)

    @commands.command(aliases=['cq'], help="Clears The Queue", usage = "clearqueue")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clearqueue(self, ctx: commands.Context): 
        vc: wavelink.Player = ctx.voice_client
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)        
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)        
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)     
        if not vc or not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing anything.",colour=self.color)
            await ctx.reply(embed=embed4, mention_author=False)
            return         
        vc.queue.clear()
        embed5 = discord.Embed(description="Successfully Cleared The Queue.",colour=self.color)
        await ctx.reply(embed=embed5, mention_author=False) 

    @commands.command(aliases=['dvol'], help="Shows The Default Volume", usage = "defaultvolume")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def defaultvolume(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = discord.Embed(description="I am not in any voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)        
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)      
        vc: wavelink.Player = ctx.voice_client
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)     
        if not vc or not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing anything.",colour=self.color)
            await ctx.reply(embed=embed4, mention_author=False)
            return      
        await vc.set_volume(100)
        embed5 = discord.Embed(description="Default volume set to 100%", colour=self.color)
        await ctx.reply(embed=embed5, mention_author=False)        

    @commands.command(aliases=['j'], help="Joins The VC", usage = "join")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)
        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                embed2 = discord.Embed(description=f"I am already in another voice channel", colour=self.color)
                return await ctx.reply(embed=embed2, mention_author=False)
            else:
                embed3 = discord.Embed(description=f"Sucessfully Joined voice channel", colour=self.color)
                await ctx.reply(embed=embed3, mention_author=False)  
        else:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
            embed4 = discord.Embed(description=f"Successfully Joined your voice channel" , colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)      
            
    @commands.command(aliases=['shift'], help="Moves The Player To Your Channel", usage = "move")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def move(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)       
        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                if ctx.voice_client.is_playing():
                    embed2 = discord.Embed(description="I am currently playing in another voice channel.", colour=self.color)
                    return await ctx.reply(embed=embed2, mention_author=False)
                else:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(1)           
                    vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)
                    embed3 = discord.Embed(description=f"Successfully moved to **{ctx.author.voice.channel.name}**", colour=self.color)
                    await ctx.reply(embed=embed3, mention_author=False)
            else:
                embed4 = discord.Embed(description=f"I am already in your voice channel: {ctx.voice_client.channel.name}", colour=self.color)
                await ctx.reply(embed=embed4, mention_author=False)
        else:
            embed5 = discord.Embed(description="I am not in a voice channel.", colour=self.color)
            await ctx.reply(embed=embed5, mention_author=False)

    @commands.command(aliases=['quit'], help="Leaves The VC", usage = "leave")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx: commands.Context):
        if not getattr(ctx.author.voice, "channel", None):
            embed = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False) 
        if not ctx.voice_client:
            embed2 = discord.Embed(description="I am not in any voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)      
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed3 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)       
        await ctx.voice_client.disconnect()
        embed4 = discord.Embed(description="Sucessfully Left voice channel.", colour=self.color)
        await ctx.reply(embed=embed4, mention_author=False)             

    @commands.command(aliases=['nowp'], help="Shows What's Playing", usage = "nowplaying")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nowplaying(self, ctx):
        if ctx.voice_client is None:
            embed = discord.Embed(description="I am not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)      
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)
        vc: wavelink.Player = ctx.voice_client                
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused please use `+resume`.",colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing any song.",colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)   
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed5 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed5, mention_author=False) 
        queue = enumerate(list(vc.queue), start=1)
        length_seconds = round(vc.current.length) / 1000
        hours, remainder = divmod(length_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        embed6 = discord.Embed(title= "Now Playing", color=self.color)
        embed6.description=f"[{vc.current.title}]({Trick.support_link})・[{duration_str}]({Trick.support_link})"
        await ctx.reply(embed=embed6, mention_author=False)
        
    @commands.command(aliases=['further'], help="Forward The Track ", usage = "forward")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def forward(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if ctx.voice_client is None:
            embed = discord.Embed(description="I am not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)       
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)              
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused please use `+resume`.",colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)        
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing any song.",colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed5 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed5, mention_author=False)       
        position = vc.position + 10000
        await vc.seek(position)
        embed6 = discord.Embed(description="Skipped the track by 10 seconds.", colour=self.color)
        await ctx.reply(embed=embed6, mention_author=False)
        
    @commands.command(aliases=['retreat'], help="Rewinds The Track", usage = "rewind")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rewind(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if ctx.voice_client is None:
            embed = discord.Embed(description="I am not in a voice channel.",colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)      
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)              
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused please use `+resume`.",colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)       
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing any song.",colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)       
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed5 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed5, mention_author=False)     
        position = max(vc.position - 10000, 0)
        await vc.seek(position)       
        embed6 = discord.Embed(description="Rewound by 10 seconds.", colour=self.color)
        await ctx.reply(embed=embed6, mention_author=False)
        
    @commands.command(aliases=['look'], help="Seek Into The Track", usage = "seek <time>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def seek(self, ctx, *, time_str):
        vc: wavelink.Player = ctx.voice_client      
        if ctx.voice_client is None:
            embed = discord.Embed(description="I am not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)       
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)         
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused, please use `+resume`.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)       
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing any song.", colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)        
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed5 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed5, mention_author=False)       
        time_pattern = re.compile(r"(\d+:\d+|\d+)")
        match = time_pattern.match(time_str)
        if not match:
            embed6 = discord.Embed(description="Invalid time format. Please use either `mm:ss` or `ss`.", colour=self.color)
            return await ctx.reply(embed=embed6, mention_author=False)      
        time_seconds = 0
        if match.group(1):
            time_components = list(map(int, match.group(1).split(":")))
            time_seconds = sum(c * 60 ** i for i, c in enumerate(reversed(time_components)))         
            await vc.seek(time_seconds * 1000)
            embed7 = discord.Embed(description=f"Successfully sought to {time_str}.", colour=self.color)
            await ctx.reply(embed=embed7, mention_author=False)
            
    @commands.command(aliases=['detach'], help="Remove a Track From The Queue", usage = "remove <index>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def remove(self, ctx, index: int):
        vc: wavelink.Player = ctx.voice_client
        if ctx.voice_client is None:
            embed = discord.Embed(description="I am not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed, mention_author=False)            
        elif not getattr(ctx.author.voice, "channel", None):
            embed2 = discord.Embed(description="You are not in a voice channel.", colour=self.color)
            return await ctx.reply(embed=embed2, mention_author=False)           
        if vc.is_paused():
            embed3 = discord.Embed(description="I am currently paused, please use `+resume`.", colour=self.color)
            return await ctx.reply(embed=embed3, mention_author=False)          
        if not vc.is_playing():
            embed4 = discord.Embed(description="I am not playing any song.", colour=self.color)
            return await ctx.reply(embed=embed4, mention_author=False)          
        if ctx.author.voice.channel != ctx.voice_client.channel:
            embed5 = discord.Embed(description="You are not in the same voice channel.", colour=self.color)
            return await ctx.reply(embed=embed5, mention_author=False)       
        if not vc.queue or index > len(vc.queue) or index < 1:
            embed6 = discord.Embed(description=f"Invalid index. Must be between 1 and {len(vc.queue)}", color=self.color)              
            return await ctx.reply(embed=embed6, mention_author=False)             
        removed = list(vc.queue).pop(index - 1)
        vc.queue = list(vc.queue)[:index - 1] + list(vc.queue)[index:]
        embed7 = discord.Embed(description=f"Successfully removed `[{removed.title}]({Trick.support_link})` from Queue.", color=self.color)    
        await ctx.reply(embed=embed7, mention_author=False)

async def setup(client):
    await client.add_cog(music(client))