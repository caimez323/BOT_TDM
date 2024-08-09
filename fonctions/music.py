import discord
import asyncio
import yt_dlp

queues = {}
voice_clients = {}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}
lClient = ""


async def on_end():
    """Fonction appelée après la fin de la lecture d'une chanson."""
    print("syhfoyutftguityuifftyuig")

def on_end_callback(error):
    """Fonction de rappel synchrone pour gérer la fin de la musique."""
    if error:
        print(f"An error occurred: {error}")
    # Exécutez la coroutine `on_end` dans la boucle d'événements principale
    asyncio.run_coroutine_threadsafe(on_end(), lClient.loop)
    
async def play_next(message):
    guild_id = message.guild.id
    if guild_id in queues and queues[guild_id]:
        url, title = queues[guild_id].pop(0)
        voice_client = voice_clients.get(guild_id)

        try:

            # Préparer le lecteur audio
            player = discord.FFmpegOpusAudio(url, **ffmpeg_options)
            # Jouer la chanson et définir la fonction de rappel
            voice_client.play(player, after=lambda e: on_end_callback(e))

            await message.channel.send(f'Now playing: {title}')
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while trying to play the next song.')



async def music(message,client):
    global lClient
    lClient = client
    guild_id = message.guild.id
    if message.content.startswith("?play"):
        # Extract the search query from the message
        query = ' '.join(message.content.split()[1:])  # Join the rest of the message as the query
        try:
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
            else:
                await message.channel.send('No results found.')
                return

            # Add the song to the queue
            if guild_id not in queues:
                queues[guild_id] = []
            queues[guild_id].append((song, title))
            #Si on joue rien on dit, sinon ça part à la queue
            if not voice_client.is_playing():
                await play_next(message)

            # Prepare the audio player
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            # Play the audio
            if not voice_client.is_playing():
                #voice_client.stop()
                voice_client.play(player, after=on_end_callback)
            print(queues)
        except Exception as e:
            print(e)
            await message.channel.send('An error occurred while trying to play the song.')

    elif message.content.startswith("?pause"):
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
