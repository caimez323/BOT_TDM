import discord
import asyncio
import yt_dlp
import time
import random
from discord.ui import View

#loop
#auteur => Fait
#Ajouter autres plateformes (deezer / spotify)
#afk for too long = deco
#pour les playlist, faire jouer la 1ère pendant que les autres chargent
#ajouter activité du bot quand il est en train de play
#ajouter sur son profil, la musique qu'il est en train de jouer (comme le fait spotify). Si c'est possible ?

#https://github.com/Rapptz/discord.py/issues/6057

class HelperView(View):
    def __init__(self,pages):
        super().__init__()
        self.current_page = 0
        self.pages = pages
    
    @discord.ui.button(label="", style=discord.ButtonStyle.gray,emoji="<:240_Amoa:1017107527961424014>")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await self.update_message(interaction)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.gray,emoji="<:238_Maraiste:1133163882999971991>")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.pages)
        await self.update_message(interaction)
    
    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)

queues = {}
voice_clients = {}
current_voice_channel = ""
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
goto = False

keyInfo = []
current_song = {}
play_start_time = {}
volume_levels = {}
timecode = {}
actTimecode = {}

def get_ffmep_options(volume):
    time = 0
    if timecode.get(keyInfo[1]) is not None: time = timecode.get(keyInfo[1])
    return {'before_options': f'-ss {time} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': f'-vn -filter:a "volume={volume}"'
}

def secToTime(secondes):
    heures = int(secondes) // 3600  # Calculer les heures
    secondes_restantes = secondes % 3600 # Reste après avoir enlevé les heures
    minutes = int(secondes_restantes) // 60  # Division entière pour obtenir les minutes
    secondes_restantes = int(secondes_restantes) % 60  # Reste de la division pour obtenir les secondes restantes
    if heures > 0: return f"{heures}:{minutes:02d}:{secondes_restantes:02d}"  # Afficher heures, minutes, secondes
    else: return f"{minutes}:{secondes_restantes:02d}"  # Afficher seulement minutes, secondes

def createEmbed(author = None):
    newEmbed = discord.Embed(title="", description="", color=0xdb5578)
    file = discord.File("fonctions/resources/musicIcon.png", filename="musicIcon.png")
    #thisMBD.add_field(name='', value="\u200b", inline=False)
    msgAuthor = keyInfo[3].author if author == None else author
    newEmbed.set_footer(text=f"{msgAuthor.name}", icon_url=msgAuthor.avatar)
    return newEmbed, file

def truncateTitle(title, channel):
    max_length = 25
    title_length = len(title)
    channel_length = len(channel) + 1
    if title_length >= max_length:
        musicTitle = title[:max_length] + ".."
    elif (title_length + channel_length) > max_length:
        available_channel_length = max_length - title_length
        truncated_channel = channel[:(available_channel_length)]
        musicTitle = f"{title} ({truncated_channel}"
        musicTitle = musicTitle[:-2] + ".."
    else:
        musicTitle = f"{title} ({channel})"
    return musicTitle

async def play_next(message, skipped=False):
    global goto
    guild_id = keyInfo[1]
    if guild_id in queues and queues[guild_id]:
        url, title, duration, ytbUrl, channel, thumbnail, author = queues[guild_id].pop(0)
        #add datas current playing song
        current_song[guild_id] = [url, title, duration, ytbUrl, channel, thumbnail, author]
        voice_client = voice_clients.get(guild_id)
        play_start_time[guild_id] = time.time()
        volume = volume_levels.get(guild_id, 0.25)
        # Préparer le lecteur audio
        player = discord.FFmpegOpusAudio(url, **get_ffmep_options(volume))
        if timecode.get(guild_id) is not None: #cad on a un timecode
            actTimecode[guild_id] = timecode[guild_id]
            timecode[guild_id] = 0
        # Jouer la chanson et définir la fonction de rappel
        voice_client.play(player, after=lambda e: on_end_callback(message, e))     
        if skipped:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Skipped to ⏩', icon_url=('attachment://musicIcon.png'))
            thisEmbed.description = f"[{title}]({ytbUrl})"
            thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
            thisEmbed.add_field(name='Song Duration', value=f"{secToTime(duration)}", inline = True)
            thisEmbed.set_thumbnail(url=thumbnail)
            await message.channel.send(embed=thisEmbed, file=file)  
        elif not goto :
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Playing ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.description = f"[{title}]({ytbUrl})"
            thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
            thisEmbed.add_field(name='Song Duration', value=f"{secToTime(duration)}", inline = True)
            thisEmbed.set_thumbnail(url=thumbnail)
            await message.channel.send(embed=thisEmbed, file=file)  
        goto = False

def on_end_callback(message, error):
    if error:
        print(f"An error occurred: {error}")
    asyncio.run_coroutine_threadsafe(play_next(message), keyInfo[0].loop)

async def nowplaying(message):
    guild_id = keyInfo[1]
    #current_song_data 0 = url, 1 = title, 2 = duration
    current_song_data = current_song[guild_id]
    title = current_song_data[1]
    duration = current_song_data[2]
    ytbUrl = current_song_data[3]
    channel = current_song_data[4]
    thumbnail = current_song_data[5]
    author = current_song_data[6].name
    current_position = time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))
    remaining_time = duration - current_position + 1
    theTrackString=list("`▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬`")
    musicPosition = (int(int(current_position)*22 / int(duration)))
    theTrackString[musicPosition+1] = "🔘"
    finalTrackString = "".join(theTrackString)

    # Embed
    # thisEmbed.add_field(name='', value=f"{finalTrackString}\n`{secToTime(current_position)}/{secToTime(duration)}`  `({secToTime(remaining_time)} left)`", inline=False)
    # thisEmbed.add_field(name='', value=f"requested by `{author}`", inline=False)
    # thisEmbed.set_thumbnail(url=thumbnail)
    # await keyInfo[2].send(embed=thisEmbed, file=file)
    thisEmbed, file = createEmbed()
    thisEmbed.set_author(name='Now Playing ♪', icon_url=('attachment://musicIcon.png'))
    thisEmbed.description = f"[{title}]({ytbUrl})"
    thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
    thisEmbed.add_field(name='Time left', value=f"{secToTime(remaining_time)}", inline = True)
    thisEmbed.add_field(name='Position', value=f"{finalTrackString} `{secToTime(current_position)}/{secToTime(duration)}`", inline = False)
    thisEmbed.add_field(name='', value=f"**requested by** {author}", inline = False)
    thisEmbed.set_thumbnail(url=thumbnail)
    await message.channel.send(embed=thisEmbed, file=file)  

def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + int(seconds)
    elif len(parts) == 1:
        return int(parts[0])
    else:
        raise ValueError("Invalid time format. Use 'minutes:seconds' or 'seconds'.")

def queuePagesCreation(message): 
    guild_id = message.guild.id
    current_song_data = current_song[guild_id]   
    #page c'est une liste d'embed
    pages = []
    cReturn = 0  
    thisEmbed = None

    title = current_song_data[1]
    duration = current_song_data[2]
    ytbUrl = current_song_data[3]
    channel = current_song_data[4]
    thumbnail = current_song_data[5]
    author = current_song_data[6].name
    # Now Playing
    musicTitle = truncateTitle(title,channel)
    thisEmbed, file = createEmbed()
    thisEmbed.set_author(name='Queue ♪', icon_url=('attachment://musicIcon.png'))
    thisEmbed.add_field(name='', value=f"**Now Playing**\n[{musicTitle}]({ytbUrl}) [``{secToTime(duration)}``] (by `{author}`)", inline=False)
    thisEmbed.set_thumbnail(url=thumbnail)
    cReturn += 2
    # Next Songs
    ind = 0
    sumDuration = 0
    embedMaxLines = 7
    value = "**Next Songs**"    
    for tup in queues.get(guild_id):
        if cReturn>=embedMaxLines:
            cReturn = 0
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Queue ♪', icon_url=('attachment://musicIcon.png'))
        ind += 1
        title = tup[1]
        duration = tup[2]
        ytbUrl = tup[3]
        channel = tup[4]
        author = tup[6].name
        sumDuration += duration
        musicTitle = truncateTitle(title,channel)
        value += f"\n**{ind}.** [{musicTitle}]({ytbUrl}) [``{secToTime(duration)}``] (by `{author}`)"
        cReturn += 1
        if cReturn>=embedMaxLines:
            thisEmbed.add_field(name='', value=value, inline=False)
            pages.append(thisEmbed)
            value = ""
    if cReturn<embedMaxLines:
        thisEmbed.add_field(name='', value=value, inline=False)
        pages.append(thisEmbed)
    songNbr = "song" if ind == 1 else "songs"       
    for i, page in enumerate(pages):
        page.set_footer(text=f"{message.author.name} · Page {i + 1}/{len(pages)}  ·  {ind} {songNbr}  ·  {secToTime(sumDuration)} playing time", icon_url=message.author.avatar)
    return pages, file
    
#==============================================
#=============      START             =========
#==============================================

async def music(message,client):
    global queues
    global current_voice_channel
    global goto
    guild_id = message.guild.id
    if len(keyInfo) != 4: #not setup yet:
        keyInfo.append(client)#0
        keyInfo.append(guild_id)#1
        keyInfo.append(message.channel)#2
        keyInfo.append(message)#3
    else:
        keyInfo[0] = client
        keyInfo[1] = guild_id
        keyInfo[2] = message.channel
        keyInfo[3] = message
    isPlaylist = False
    if message.content.startswith(("!play", "!p")):
        waitMessage = None
        # Extract the search query from the message
        query = ' '.join(message.content.split()[1:])  # Join the rest of the message as the query
        #On va d'abord regarder si c'est pas une playlist
        if "&list=" in query:
            isPlaylist = True
            waitMessage = await message.channel.send("Chargement d'une playlist en cours.. cela peut prendre du temps..")
        else:
            waitMessage = await message.channel.send("Chargement...")
        # If not connected to a channel, connect to the user's channel
        if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
            voice_client = await message.author.voice.channel.connect()
            voice_clients[guild_id] = voice_client
        else:
            voice_client = voice_clients[guild_id]
            
        # On fait la recherche et on prend le premier lien
        # Si à l'avenir on chercher à ajouter plus de résultat, il faudra toucher ici
        loop = asyncio.get_event_loop()
        if isPlaylist: #playlist
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        else: #classic
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=False))
        if 'entries' in data:
            if isPlaylist: #playlist
                for elem in data["entries"]:
                    song = elem['url']
                    title = elem['title']
                    duration = elem["duration"]
                    ytbUrl = elem['original_url']
                    channel = elem['channel']
                    thumbnail = elem['thumbnail']
                    if guild_id not in queues:
                        queues[guild_id] = []
                    queues[guild_id].append((song, title, duration, ytbUrl, channel, thumbnail, message.author))
                await waitMessage.delete()
                await message.channel.send('Playlist added to queue')
                # à enlever
                if voice_client.is_playing():
                    currentSongLeft = current_song[guild_id][2] - (time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))) + 1
                    totalDuration = currentSongLeft
                    for tup in queues.get(guild_id)[:-1]:
                        totalDuration += tup[2]
                    thisEmbed, file = createEmbed()
                    thisEmbed.set_author(name='Added to queue ♪', icon_url=('attachment://musicIcon.png'))
                    thisEmbed.description = f"[{title}]({ytbUrl})"
                    thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
                    thisEmbed.add_field(name='Song Duration', value=f"{secToTime(duration)}", inline = True)
                    thisEmbed.add_field(name='Time until playing', value=f"{secToTime(totalDuration)}", inline = True)
                    thisEmbed.add_field(name='Position in queue', value=f"{len(queues[guild_id])}", inline = False)
                    thisEmbed.set_thumbnail(url=thumbnail)
                    await message.channel.send(embed=thisEmbed, file=file)     
            else:#one
                song = data['entries'][0]['url']
                title = data['entries'][0]['title']
                duration = data["entries"][0]["duration"]
                ytbUrl = data["entries"][0]['original_url']
                channel = data["entries"][0]['channel']
                thumbnail = data["entries"][0]['thumbnail']
                if guild_id not in queues:
                    queues[guild_id] = []
                queues[guild_id].append((song, title, duration, ytbUrl, channel, thumbnail, message.author))
                await waitMessage.delete()
                if voice_client.is_playing():
                    currentSongLeft = current_song[guild_id][2] - (time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))) + 1
                    totalDuration = currentSongLeft
                    for tup in queues.get(guild_id)[:-1]:
                        totalDuration += tup[2]
                    thisEmbed, file = createEmbed()
                    thisEmbed.set_author(name='Added to queue ♪', icon_url=('attachment://musicIcon.png'))
                    thisEmbed.description = f"[{title}]({ytbUrl})"
                    thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
                    thisEmbed.add_field(name='Song Duration', value=f"{secToTime(duration)}", inline = True)
                    thisEmbed.add_field(name='Time until playing', value=f"{secToTime(totalDuration)}", inline = True)
                    thisEmbed.add_field(name='Position in queue', value=f"{len(queues[guild_id])}", inline = False)
                    thisEmbed.set_thumbnail(url=thumbnail)
                    await message.channel.send(embed=thisEmbed, file=file)             
        else:
            await message.channel.send('No results found.')
            return
        
        #Si on joue rien on dit, sinon ça part à la queue
        if not voice_client.is_playing():
            await play_next(message, False)

    elif message.content.lower() == "!join":
        guild_id = message.guild.id
        channel = message.author.voice.channel
        # If not connected to a channel, connect to the user's channel
        if (guild_id not in voice_clients or not voice_clients[guild_id].is_connected()):
            current_voice_channel = message.author.voice.channel
            voice_client = await message.author.voice.channel.connect()
            voice_clients[guild_id] = voice_client
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Joined** `{channel}`")
            await message.channel.send(embed=thisEmbed, file=file)
        elif channel == current_voice_channel:
            voice_client = voice_clients[guild_id]
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Already joined** `{channel}`")
            await message.channel.send(embed=thisEmbed, file=file)
        else:
            # leave
            voice_clients[guild_id].stop()
            await voice_clients[guild_id].disconnect()
            del voice_clients[guild_id]
            # reconnect
            current_voice_channel = message.author.voice.channel
            voice_client = await message.author.voice.channel.connect()
            voice_clients[guild_id] = voice_client
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Joined** `{channel}`")
            await message.channel.send(embed=thisEmbed, file=file)

    elif message.content.startswith("!pause"):
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                voice_clients[guild_id].pause()
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Music paused** ▶️")
                await message.channel.send(embed=thisEmbed, file=file)
            elif guild_id in voice_clients:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Not currently playing**")
                await message.channel.send(embed=thisEmbed, file=file)
            else:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Not in a voice channel**")
                await message.channel.send(embed=thisEmbed, file=file)
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while pausing the music.')

    elif message.content.startswith("!resume"):
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_paused():
                voice_clients[guild_id].resume()
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Music resumed** ⏸")
                await message.channel.send(embed=thisEmbed, file=file)
            elif guild_id in voice_clients:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Music not in pause")
                await message.channel.send(embed=thisEmbed, file=file)
            else:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Not in a voice channel**")
                await message.channel.send(embed=thisEmbed, file=file)
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while resuming the music.')

    elif message.content.strip() in ["!stop","!leave"]:
        queues = {}
        channel = message.author.voice.channel
        try:
            if guild_id in voice_clients:
                voice_clients[guild_id].stop()
                await voice_clients[guild_id].disconnect()
                del voice_clients[guild_id]
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Disconnected from** `{channel}`")
                await message.channel.send(embed=thisEmbed, file=file)
            else:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"**Not in a voice channel**")
                await message.channel.send(embed=thisEmbed, file=file)
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while stopping the music.')
    
    elif message.content.strip() == "!skip":
        if len(queues[guild_id])>0 and voice_clients[guild_id].is_playing():
            voice_clients[guild_id].stop()
            await play_next(message, skipped=True)

    elif message.content.strip() == "!queue":
        getQueues = queues.get(guild_id)
        if getQueues is None or getQueues == []:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Queue is empty**")
            await message.channel.send(embed=thisEmbed, file=file)
            return

        pages,file = queuePagesCreation(message)
        await message.channel.send(embed=pages[0],view = HelperView(pages), file=file)     
         
    elif message.content.strip() in ["!np","!nowplaying"]:
        if guild_id in voice_clients and voice_clients[guild_id].is_playing():
            await nowplaying(message)
        else : 
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Not currently playing**")
            await message.channel.send(embed=thisEmbed, file=file)

    elif message.content.strip() == "!shuffle":
        random.shuffle(queues[guild_id])
        thisEmbed, file = createEmbed()
        thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
        thisEmbed.add_field(name='', value=f"**Queue shuffled 🔀**")
        await message.channel.send(embed=thisEmbed, file=file)

    elif message.content.startswith("!remove"):
        if len(message.content.split())!=2:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"Merci de préciser le **numéro** de la musique à supprimer de la **queue**")
            await message.channel.send(embed=thisEmbed, file=file)
            return
        id = int(message.content.split()[1])-1
        if len(queues[guild_id])<= id:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"Merci d'indiquer un numéro correct de la **queue**")
            await message.channel.send(embed=thisEmbed, file=file)
            return
        ytbUrl = current_song[guild_id][3]   
        channel = current_song[guild_id][4]   
        thumbnail = current_song[guild_id][5]   
        thisEmbed, file = createEmbed()
        thisEmbed.set_author(name='Removed from queue ❌', icon_url=('attachment://musicIcon.png'))
        thisEmbed.description = f"[{queues[guild_id][id][1]}]({ytbUrl})"
        thisEmbed.add_field(name='Channel', value=f"{channel}", inline = True)
        thisEmbed.add_field(name='Position in queue', value=f"{id+1}", inline = True)
        thisEmbed.set_thumbnail(url=thumbnail)
        await message.channel.send(embed=thisEmbed, file=file)  
        del queues[guild_id][id]

    elif message.content.startswith("!volume"):
        if len(message.content.split())<=1:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"Merci d'indiquer un volume entre **0.0** et **2.0**")
            await message.channel.send(embed=thisEmbed, file=file)
            return
        song,title,duration,ytbUrl,channel,thumbnail,author = current_song[guild_id]   
        volume = float(message.content.split()[1])
        if (0.0 <= volume <= 2.0) or message.author.id in [172362870439411713,257167325558472705]:  # Limiter le volume entre 0.0 et 2.0
            volume_levels[guild_id] = volume
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Volume set to** `{volume:.2f}`")
            await message.channel.send(embed=thisEmbed, file=file)
            if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                #Stop, re-add in first, replay
                goto = True
                voice_clients[guild_id].stop()
                if guild_id not in queues:
                    queues[guild_id] = []
                queues[guild_id].insert(0,(song, title ,duration,ytbUrl,channel,thumbnail,author))
                timecode[guild_id] = time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))
                await play_next(message)
        else:
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"Merci d'indiquer un volume entre **0.0** et **2.0**")
            await message.channel.send(embed=thisEmbed, file=file)
    
    elif message.content.startswith("!goto"):
        if len(message.content.split())<=1:
            return
        #Stop, re-add in first, replay
        if guild_id in voice_clients and voice_clients[guild_id].is_playing():
            song,title,duration,ytbUrl,channel,thumbnail,author = current_song[guild_id]   
            timecode[guild_id] = time_to_seconds(message.content.split()[1])
            if type(timecode[guild_id]) is not int:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"Merci d'indiquer un temps en secondes ou de la forme xx:xx")
                await message.channel.send(embed=thisEmbed, file=file)
                return
            if timecode[guild_id] >= duration:
                thisEmbed, file = createEmbed()
                thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
                thisEmbed.add_field(name='', value=f"Merci d'indiquer un temps **inférieur** à la durée de la musique **(`{secToTime(duration)}`)**")
                await message.channel.send(embed=thisEmbed, file=file)
                return
            #Stop, re-add in first, replay
            goto = True
            voice_clients[guild_id].stop()
            if guild_id not in queues:
                queues[guild_id] = []
            queues[guild_id].insert(0,(song, title ,duration,ytbUrl,channel,thumbnail,author))
        else: # si on joue pas c'est inutile
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"**Not currently playing**")
            await message.channel.send(embed=thisEmbed, file=file)
            return
        thisEmbed, file = createEmbed()
        thisEmbed.set_author(name='Music  ♪', icon_url=('attachment://musicIcon.png'))
        thisEmbed.add_field(name='', value=f"**Music set to `{secToTime(timecode[guild_id])}`**")
        await message.channel.send(embed=thisEmbed, file=file)