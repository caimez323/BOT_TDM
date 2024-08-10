import discord
import asyncio
import yt_dlp
import time

#loop
#queue random
#auteur
#np avec barre
#delete queue

#Ajouter autres plateformes & playlist

#https://github.com/Rapptz/discord.py/issues/6057
queues = {}
voice_clients = {}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}
lClient = ""
keyInfo = []
current_song = {}
play_start_time = {}


async def play_next(skipped=False):
    guild_id = keyInfo[1]
    if guild_id in queues and queues[guild_id]:
        url, title, duration = queues[guild_id].pop(0)
        #add datas current playing song
        current_song[guild_id] = [url,title,duration]
        voice_client = voice_clients.get(guild_id)
        play_start_time[guild_id] = time.time()
        try:
            # Préparer le lecteur audio
            player = discord.FFmpegOpusAudio(url, **ffmpeg_options)
            # Jouer la chanson et définir la fonction de rappel
            voice_client.play(player, after=lambda e: on_end_callback(e))
            if skipped : await keyInfo[2].send(f'Skipped to: `{title}`')
            else: await keyInfo[2].send(f'Now playing: `{title}`')
            
        except Exception as e:
            print(e)
            await keyInfo[2].send('An error occurred while trying to play the next song.')

def on_end_callback(error):
    if error:
        print(f"An error occurred: {error}")
    asyncio.run_coroutine_threadsafe(play_next(), keyInfo[0].loop)

async def nowplaying(message):
    guild_id = keyInfo[1]
    #current_song_data 0 = url, 1 = title, 2 = duration
    current_song_data = current_song[guild_id]
    duration = current_song_data[2]
    current_position = time.time() - play_start_time.get(guild_id, 0)
    remaining_time = duration - current_position
    await message.channel.send(
            f"Now playing: {current_song_data[1]}\n"
            f"Duration: {duration} seconds\n"
            f"Current Position: {current_position:.0f} seconds\n"
            f"Remaining Time: {remaining_time:.0f} seconds"
        )
    theTrackString=list("`────────────────────`")
    musicPosition = (int(int(current_position)*20 / int(duration)))
    theTrackString[musicPosition+1] = "|"
    await message.channel.send("".join(theTrackString))

async def music(message,client):
    global queues
    guild_id = message.guild.id
    keyInfo.append(client)#0
    keyInfo.append(guild_id)#1
    keyInfo.append(message.channel)#2
    if message.content.startswith("?play"):
        # Extract the search query from the message
        query = ' '.join(message.content.split()[1:])  # Join the rest of the message as the query
        # If not connected to a channel, connect to the user's channel
        if guild_id not in voice_clients or not voice_clients[guild_id].is_connected():
            voice_client = await message.author.voice.channel.connect()
            voice_clients[guild_id] = voice_client
        else:
            voice_client = voice_clients[guild_id]

            
        # On fait la recherche et on prend le premier lien
        # Si à l'avenir on chercher à ajouter plus de résultat, il faudra toucher ici
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{query}", download=False))
        if 'entries' in data:
            song = data['entries'][0]['url']
            title = data['entries'][0]['title']
            duration = data["entries"][0]["duration"]
        else:
            await message.channel.send('No results found.')
            return
        await message.channel.send(f"Added `{title}` to the queue !")
        # Add the song to the queue
        if guild_id not in queues:
            queues[guild_id] = []
        queues[guild_id].append((song, title,duration))
        #Si on joue rien on dit, sinon ça part à la queue
        if not voice_client.is_playing():
            await play_next()

    elif message.content.startswith("?pause"): # SI on est en pause on est pas considéré comme entrain de jouer donc ça skip si on play
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_playing():
                voice_clients[guild_id].pause()
                await message.channel.send('Playback paused.')
            else:
                await message.channel.send('No music is playing.')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while pausing the music.')

    elif message.content.startswith("?resume"):
        try:
            if guild_id in voice_clients and voice_clients[guild_id].is_paused():
                voice_clients[guild_id].resume()
                await message.channel.send('Playback resumed.')
            else:
                await message.channel.send('Music is not paused.')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while resuming the music.')

    elif message.content.startswith("?stop"):
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
    elif message.content == "?skip":
        if len(queues[guild_id])>0 and voice_clients[guild_id].is_playing():
            voice_clients[guild_id].stop()
            await play_next(skipped=True)

    elif message.content == "?queue":
        await message.channel.send(f"A suivre : {queues[guild_id]}")
    
    elif message.content == "?np" or message.content == "?nowplaying":
        await nowplaying(message)
