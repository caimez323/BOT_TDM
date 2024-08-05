import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio

TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': 'in_playlist'
}

ydl = yt_dlp.YoutubeDL(ydl_opts)

# File d'attente pour les morceaux
music_queue = []
next_music_file = None

@client.command(name='join', help='Commande pour faire rejoindre le bot dans un canal vocal.')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Tu dois être dans un canal vocal pour utiliser cette commande.")

@client.command(name='play', help='Commande pour ajouter de la musique à la file d\'attente.')
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.send("Je ne suis pas connecté à un canal vocal.")
        return

    async with ctx.typing():
        info = ydl.extract_info(f"ytsearch:{search}", download=False)
        if 'entries' in info and len(info['entries']) > 0:
            music_info = info['entries'][0]
            music_queue.append(music_info)  # Ajouter la musique à la file d'attente
            await ctx.send(f"Ajouté à la file d'attente: **{music_info['title']}**")
            
            if not ctx.voice_client.is_playing():
                await play_next(ctx)  # Jouer la prochaine musique dans la file si rien n'est en cours
            elif len(music_queue) == 1:
                # Précharger la prochaine musique si elle est la seule dans la file
                await predownload_next()
        else:
            await ctx.send("Aucun résultat trouvé pour la recherche.")

async def play_next(ctx):
    global next_music_file

    if next_music_file:
        downloaded_file = next_music_file
        next_music_file = None
    elif len(music_queue) > 0:
        info = music_queue.pop(0)  # Retirer et obtenir la première musique de la file d'attente
        url = info['url']

        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
            ydl_download.download([url])

        downloaded_file = "song.webm" if os.path.exists("song.webm") else "song.mp3"
    else:
        return  # Pas de musique à jouer

    source = discord.FFmpegPCMAudio(downloaded_file)
    ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(cleanup(ctx, downloaded_file), client.loop))
    await ctx.send(f"Lecture de: **{info['title']}**")

    # Précharger la musique suivante en arrière-plan
    if len(music_queue) > 0:
        await predownload_next()


async def predownload_next():
    global next_music_file

    if len(music_queue) > 0 and not next_music_file:
        info = music_queue[0]
        url = info['url']

        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': 'next_song.%(ext)s'
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl_download:
            ydl_download.download([url])

        next_music_file = "next_song.webm" if os.path.exists("next_song.webm") else "next_song.mp3"

async def cleanup(ctx, file):
    try:
        if os.path.exists(file):
            os.remove(file)
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier: {str(e)}")
    await play_next(ctx)  # Jouer la musique suivante dans la file d'attente

import logging
logging.basicConfig(level=logging.INFO)

@client.command(name='skip', help='Commande pour passer à la musique suivante.')
async def skip(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        logging.info("Musique arrêtée. Passage à la musique suivante...")
        await ctx.send("Musique suivante...")
        await play_next(ctx)
    else:
        await ctx.send("Aucune musique en cours de lecture.")

@client.command(name='leave', help='Commande pour faire quitter le bot du canal vocal.')
async def leave(ctx):
    global next_music_file

    if ctx.voice_client:
        music_queue.clear()  # Vider la file d'attente
        next_music_file = None
        await ctx.voice_client.disconnect()

        # Supprimer les fichiers audio restants
        if os.path.exists('song.webm'):
            os.remove('song.webm')
        elif os.path.exists('song.mp3'):
            os.remove('song.mp3')
            
        if os.path.exists('next_song.webm'):
            os.remove('next_song.webm')
        elif os.path.exists('next_song.mp3'):
            os.remove('next_song.mp3')

@client.event
async def on_ready():
    print(f'{client.user} est connecté et prêt à l\'utilisation!')

client.run(TOKEN)
