import random
import asyncio
import discord

async def duel(message,client):
      if not message.mentions:
        await message.channel.send("Erreur, veuillez entrer un adversaire valide en le mentionnant.")
        return

      if len(message.mentions) > 1:
        await message.channel.send("Erreur, tu ne peux défier qu'un seul adversaire à la fois !")
        return

      adversaire = message.mentions[0]

      await message.channel.send(f"{message.author.mention} souhaite défier {adversaire.mention}, accepte-t-il le défi ? *(!oui pour accepter.)*")
      
      def check_adversaire(reponse):
            return reponse.author == adversaire and reponse.content ==  "!oui"

      try:
        reponse = await client.wait_for("message", timeout = 20, check = check_adversaire)
      except: 
        await message.channel.send("L'adversaire n'a pas accepté le duel.")
        return

      await message.channel.send("Très bien, le duel va pouvoir commencer.\nSoyez prêt à faire !feu dès que j'en donnerai l'ordre.")

      voicetrue1 = message.author.voice
      voicetrue2 = adversaire.voice
      voice = message.guild.voice_client

      if not voicetrue1 is None: #Si celui qui lance le défi est connecté à un vocal
        channel_vocal = message.author.voice.channel
        if not voice: #Si le bot n'est pas dans un vocal
          await channel_vocal.connect()
        voice = message.guild.voice_client
        audio = discord.FFmpegPCMAudio("fonctions/duelMusics/Le_bbt.mp3")
        message.guild.voice_client.stop()
        #voice.play(audio)
      elif not voicetrue2 is None: #Si l'adversaire est connecté à un vocal
        channel_vocal = adversaire.voice.channel
        if not voice: #Si le bot n'est pas dans un vocal
          await channel_vocal.connect()
        voice = message.guild.voice_client
        audio = discord.FFmpegPCMAudio("fonctions/duelMusics/Le_bbt.mp3")(executable="C:/path/ffmpeg.exe", source="mp3.mp3")
        message.guild.voice_client.stop()
        #voice.play(audio)
      
      timer = random.randint(10,25)
      await asyncio.sleep(timer)
      fire = discord.FFmpegPCMAudio("fonctions/duelMusics/Pan.mp3")
      message.guild.voice_client.stop()
      await message.channel.send("FEU !!")
      voice.play(fire)

      def check_feu(feu):
            return (feu.author == adversaire or feu.author == message.author) and feu.content ==  "!feu"

      feu = await client.wait_for("message", timeout = 30, check = check_feu)
      try: 
        if feu.author == message.author:
          await message.channel.send(f"L'as de la gachette {message.author.mention} a remporté ce duel !")
          await asyncio.sleep(3)
          message.guild.voice_client.stop()
          await adversaire.move_to(None)
          await message.guild.voice_client.disconnect()
          return
        if feu.author == adversaire:
          await message.channel.send(f"L'as de la gachette {adversaire.mention} a remporté ce duel !")
          await asyncio.sleep(3)
          message.guild.voice_client.stop()
          await message.author.move_to(None)
          await message.guild.voice_client.disconnect()
          return
      except :
        await message.channel.send("Les deux tireurs se sont endormis...")
        return
        
      