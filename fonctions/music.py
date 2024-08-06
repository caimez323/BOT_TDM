import discord
import yt_dlp
import os
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': 'in_playlist',
    'continuedl': False,
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

# File d'attente pour les morceaux
music_queue = []
next_music_file = None

async def join_channel(message):
    if message.author.voice:
        channel = message.author.voice.channel
        await channel.connect()
        await message.channel.send(f"Connecté au canal vocal: {channel.name}")
    else:
        await message.channel.send("Tu dois être dans un canal vocal pour utiliser cette commande.")

async def play_music(message, search: str):
    global next_music_file

    if not message.guild.voice_client:
        await message.channel.send("Je ne suis pas connecté à un canal vocal.")
        return

    async with message.channel.typing():
        info = ydl.extract_info(f"ytsearch:{search}", download=False)
        if 'entries' in info and len(info['entries']) > 0:
            music_info = info['entries'][0]

            if not message.guild.voice_client.is_playing() and len(music_queue) == 0:
                music_queue.append(music_info)  # Ajouter la musique à la file d'attente
                await download_and_play(message, music_info)  # Télécharger et jouer la musique
            else:
                music_queue.append(music_info)  # Ajouter la musique à la file d'attente
                await message.channel.send(f"Ajouté à la file d'attente: **{music_info['title']}**")

            if len(music_queue) == 1:  # Si c'est la seule musique dans la file, précharger la suivante
                await predownload_next()
        else:
            await message.channel.send("Aucun résultat trouvé pour la recherche.")

async def download_and_play(message, music_info):
    url = music_info['url']
    downloaded_file = "song.mp3"
    
    ydl_opts_download = {
        'format': 'bestaudio/best',
        'outtmpl': downloaded_file
    }
    
    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
        ydl_download.download([url])
    
    source = discord.FFmpegPCMAudio(downloaded_file)
    message.guild.voice_client.play(source, after=lambda e: asyncio.create_task(cleanup(message, downloaded_file)))
    await message.channel.send(f"Lecture de: **{music_info['title']}**")

async def play_next(message):
    global next_music_file

    if next_music_file:
        downloaded_file = next_music_file
        next_music_file = None
    elif len(music_queue) > 0:
        info = music_queue.pop(0)  # Retirer et obtenir la première musique de la file d'attente
        url = info['url']

        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.mp3'
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
            ydl_download.download([url])

        downloaded_file = "song.mp3"
        await message.channel.send(f"Lecture de: **{info['title']}**")
    else:
        return  # Pas de musique à jouer

    source = discord.FFmpegPCMAudio(downloaded_file)
    message.guild.voice_client.play(source, after=lambda e: asyncio.create_task(cleanup(message, downloaded_file)))

    if len(music_queue) > 0:
        await predownload_next()  # Précharger la musique suivante en arrière-plan

async def predownload_next():
    global next_music_file

    if len(music_queue) > 0 and not next_music_file:
        info = music_queue[0]
        url = info['url']

        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': 'next_song.mp3'
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
            ydl_download.download([url])

        next_music_file = "next_song.mp3"

async def cleanup(message, file):
    try:
        if os.path.exists(file):
            os.remove(file)
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier: {str(e)}")
    await play_next(message)  # Jouer la musique suivante dans la file d'attente

async def skip_music(message):
    if message.guild.voice_client.is_playing():
        message.guild.voice_client.stop()
        await message.channel.send("Musique suivante...")
        await play_next(message)
    else:
        await message.channel.send("Aucune musique en cours de lecture.")

async def leave_channel(message):
    global next_music_file

    if message.guild.voice_client:
        music_queue.clear()  # Vider la file d'attente
        next_music_file = None
        await message.guild.voice_client.disconnect()

        # Supprimer les fichiers audio restants
        for file in ['song.mp3', 'next_song.mp3']:
            if os.path.exists(file):
                os.remove(file)

# Entry point
async def music(message):
    if message.content.startswith('!join'):
        await join_channel(message)
    elif message.content.startswith('!play'):
        await play_music(message, message.content[len('!play '):])
    elif message.content.startswith('!skip'):
        await skip_music(message)
    elif message.content.startswith('!leave'):
        await leave_channel(message)
