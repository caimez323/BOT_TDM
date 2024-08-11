import discord
import asyncio
import yt_dlp
import time
import random

#loop
#auteur
#Ajouter autres plateformes
#afk for too long = deco

#https://github.com/Rapptz/discord.py/issues/6057


queues = {}
voice_clients = {}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

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

def secToMin(secondes):
    minutes = int(secondes) // 60  # Division entière pour obtenir les minutes
    secondes_restantes = int(secondes) % 60  # Reste de la division pour obtenir les secondes restantes
    return f"{minutes}:{secondes_restantes:02d}"  # Formater avec deux chiffres pour les secondes

def createEmbed():
    newEmbed = discord.Embed(title="", description="", color=0xdb5578)
    file = discord.File("fonctions/resources/musicIcon.png", filename="musicIcon.png")
    #thisMBD.add_field(name='', value="\u200b", inline=False)
    newEmbed.set_footer(text=f"{keyInfo[3].author.name}", icon_url=keyInfo[3].author.avatar)
    return newEmbed, file

async def play_next(skipped=False):
    guild_id = keyInfo[1]
    if guild_id in queues and queues[guild_id]:
        url, title, duration, ytbUrl, channel, author = queues[guild_id].pop(0)
        #add datas current playing song
        current_song[guild_id] = [url, title, duration, ytbUrl, channel, author]
        voice_client = voice_clients.get(guild_id)
        play_start_time[guild_id] = time.time()
        volume = volume_levels.get(guild_id, 0.25)
        # Préparer le lecteur audio
        player = discord.FFmpegOpusAudio(url, **get_ffmep_options(volume))
        if timecode.get(guild_id) is not None: #cad on a un timecode
            actTimecode[guild_id] = timecode[guild_id]
            timecode[guild_id] = 0
        # Jouer la chanson et définir la fonction de rappel
        voice_client.play(player, after=lambda e: on_end_callback(e))        
        if skipped : 
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"⏩ **Skipped to**: `{title}` [``{secToMin(duration)}``]")
            await keyInfo[2].send(embed=thisEmbed)
        else: 
            thisEmbed, file = createEmbed()
            thisEmbed.set_author(name='Now Playing  ♪', icon_url=('attachment://musicIcon.png'))
            thisEmbed.add_field(name='', value=f"[{channel} - {title}]({ytbUrl}) [``{secToMin(duration)}``]")
            await keyInfo[2].send(embed=thisEmbed, file=file)

def on_end_callback(error):
    if error:
        print(f"An error occurred: {error}")
    asyncio.run_coroutine_threadsafe(play_next(), keyInfo[0].loop)

async def nowplaying(message):
    guild_id = keyInfo[1]
    #current_song_data 0 = url, 1 = title, 2 = duration
    current_song_data = current_song[guild_id]
    title = current_song_data[1]
    duration = current_song_data[2]
    ytbUrl = current_song_data[3]
    channel = current_song_data[4]
    author = current_song_data[5]
    current_position = time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))
    remaining_time = duration - current_position + 1
    theTrackString=list("`▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬`")
    musicPosition = (int(int(current_position)*22 / int(duration)))
    theTrackString[musicPosition+1] = "🔘"
    finalTrackString = "".join(theTrackString)

    # Embed
    thisEmbed, file = createEmbed()
    thisEmbed.set_author(name='Now Playing  ♪', icon_url=('attachment://musicIcon.png'))
    thisEmbed.add_field(name='', value=f"[{channel} - {title}]({ytbUrl})", inline=False)
    thisEmbed.add_field(name='', value=f"{finalTrackString}\n`{secToMin(current_position)}/{secToMin(duration)}`  `({secToMin(remaining_time)} left)`", inline=False)
    # thisEmbed.add_field(name='', value="\u200b", inline=False)
    thisEmbed.add_field(name='', value=f"requested by `{author}`", inline=False)
    await keyInfo[2].send(embed=thisEmbed, file=file)

def time_to_seconds(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + int(seconds)
    elif len(parts) == 1:
        return int(parts[0])
    else:
        raise ValueError("Invalid time format. Use 'minutes:seconds' or 'seconds'.")
    
#==============================================
#=============      START             =========
#==============================================

async def music(message,client):
    global queues
    guild_id = message.guild.id
    if len(keyInfo) != 3: #not setup yet:
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
    if message.content.startswith("!play"):
        waitMessage = None
        # Extract the search query from the message
        query = ' '.join(message.content.split()[1:])  # Join the rest of the message as the query
        #On va d'abord regarder si c'est pas une playlist
        if "&list=" in query:
            isPlaylist = True
            waitMessage = await message.channel.send("Chargement d'une playlist en cours... cela peut prendre du temps..")
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
            if 'entries' in data: #playlist
                for elem in data["entries"]:
                    song = elem['url']
                    title = elem['title']
                    duration = elem["duration"]
                    ytbUrl = elem['original_url']
                    channel = elem['channel']
                    if guild_id not in queues:
                        queues[guild_id] = []
                    queues[guild_id].append((song, title, duration, ytbUrl, channel, message.author.name))
                await message.channel.send(f"Added playlist to the queue !")           
                await waitMessage.delete()
            else:#one
                song = data['entries'][0]['url']
                title = data['entries'][0]['title']
                duration = data["entries"][0]["duration"]
                ytbUrl = data["entries"][0]['original_url']
                channel = data["entries"][0]['channel']
                if guild_id not in queues:
                    queues[guild_id] = []
                queues[guild_id].append((song, title, duration, ytbUrl, channel, message.author.name))
                await waitMessage.delete()
                if voice_client.is_playing() : await message.channel.send(f"Added `{title}` to the queue !")                
        else:
            await message.channel.send('No results found.')
            return
        
        #Si on joue rien on dit, sinon ça part à la queue
        if not voice_client.is_playing():
            await play_next()


    elif message.content.startswith("!pause"): # SI on est en pause on est pas considéré comme entrain de jouer donc ça skip si on play
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                voice_clients[guild_id].pause()
                await message.channel.send('Playback paused.')
            else:
                await message.channel.send('No music is playing.')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while pausing the music.')

    elif message.content.startswith("!resume"):
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_paused():
                voice_clients[guild_id].resume()
                await message.channel.send('Playback resumed.')
            else:
                await message.channel.send('Music is not paused.')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while resuming the music.')

    elif message.content.strip() in ["!stop","!leave"]:
        queues = {}
        try:
            if guild_id in voice_clients:
                voice_clients[guild_id].stop()
                await voice_clients[guild_id].disconnect()
                del voice_clients[guild_id]
                await message.channel.send('Playback stopped and disconnected.')
            else:
                await message.channel.send('No music is playing.')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while stopping the music.')

    
    elif message.content.strip() == "!skip":
        if len(queues[guild_id])>0 and voice_clients[guild_id].is_playing():
            voice_clients[guild_id].stop()
            await play_next(skipped=True)

    elif message.content.strip() == "!queue":
        theString = ""
        if queues.get(guild_id) is None:
            await message.channel.send(f"Queue vide pour l'instant")
            return

        current_song_data = current_song[guild_id]
        title = current_song_data[1]
        duration = current_song_data[2]
        ytbUrl = current_song_data[3]
        channel = current_song_data[4]
        thisEmbed, file = createEmbed()
        thisEmbed.set_author(name='Queue ♪', icon_url=('attachment://musicIcon.png'))
        thisEmbed.add_field(name='', value=f"**Now Playing:**\n[{channel} - {title}]({ytbUrl}) [``{secToMin(duration)}``]", inline=False)
        ind = 0
        value = "**Next Songs:**"    
        for tup in queues.get(guild_id):
            ind += 1
            title = tup[1]
            duration = tup[2]
            ytbUrl = tup[3]
            channel = tup[4]
            author = tup[5]
            value += f"\n**{ind}.** [{channel} - {title}]({ytbUrl}) [``{secToMin(duration)}``] (by `{author}`)"
        thisEmbed.add_field(name='', value=value, inline=False)
        songNbr = "song" if ind == 1 else "songs"
        thisEmbed.set_footer(text=f"{keyInfo[3].author.name} - Page x/x | {ind} {songNbr} | xx:xx playing time", icon_url=keyInfo[3].author.avatar)
        await message.channel.send(embed=thisEmbed, file=file)
    
    elif message.content.strip() in ["!np","!nowplaying"]:
        await nowplaying(message)
    
    elif message.content.strip() == "!shuffle":
        random.shuffle(queues[guild_id])
        await message.channel.send("Queue mélangée !")

    elif message.content.startswith("!remove"):
        if len(message.content.split())!=2:
            await message.channel.send("Merci d'envoyer un numéro à supprimer")
            return
        id = int(message.content.split()[1])-1
        if len(queues[guild_id])<= id:
            await message.channel.send("Merci d'indiquer un nombre correct")
            return
        await message.channel.send(f"`{queues[guild_id][id][1]}` supprimé")
        del queues[guild_id][id]

    elif message.content.startswith("!volume"):
            if len(message.content.split())<=1:
                await message.channel.send("Merci de mettre un volume entre 0.0 et 2.0")
                return
            volume = float(message.content.split()[1])
            if (0.0 <= volume <= 2.0) or message.author.id in [172362870439411713,257167325558472705]:  # Limiter le volume entre 0.0 et 2.0
                volume_levels[guild_id] = volume
                await message.channel.send(f'Volume réglé à {volume:.2f}')
                if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                    #Stop, re-add in first, replay
                    voice_clients[guild_id].stop()
                    song,title,duration = current_song[guild_id]
                    if guild_id not in queues:
                        queues[guild_id] = []
                    queues[guild_id].insert(0,(song, title ,duration))
                    timecode[guild_id] = time.time() - play_start_time.get(guild_id, 0) + (0 if actTimecode.get(guild_id) is None else actTimecode.get(guild_id))
                    await play_next()
            else:
                await message.channel.send("Merci de mettre un volume entre 0.0 et 2.0")
    
    elif message.content.startswith("!goto"):
        if len(message.content.split())<=1:
            return
        #Stop, re-add in first, replay
        if guild_id in voice_clients and voice_clients[guild_id].is_playing():
            #Stop, re-add in first, replay
            voice_clients[guild_id].stop()
            song,title,duration = current_song[guild_id]
            if guild_id not in queues:
                queues[guild_id] = []
            queues[guild_id].insert(0,(song, title ,duration))
        else: # si on joue pas c'est inutile
            await message.channel.send("Aucune musique ne cours")
            return
        timecode[guild_id] = time_to_seconds(message.content.split()[1])
        if type(timecode[guild_id]) is not int:
            await message.channel.send("Merci de mettre un temps en secondes")
            return
        if timecode[guild_id] >= duration:
            await message.channel.send(f"Merci de mettre un temps compris dans la musique (`{duration}`)")
            return
        await message.channel.send(f"Musique mise à `{timecode[guild_id]}`")
        await play_next()