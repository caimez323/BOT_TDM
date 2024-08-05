#====================================BOLOSSE====================================
import random
import asyncio

async def bolosse(message):
    await message.channel.send("Analyse TDM en cours pour savoir qui est le bolosse du channel...")
    await asyncio.sleep(3)
    connectés = []
    channel = message.author.voice.channel
    for user in channel.members:
      if (user.nick == None):
        connectés.append(user.name)
      else:
        connectés.append(user.nick)
      
    choisi = random.choice(connectés)
    emojis = random.choice(["<a:95_Pffft:873548369753165824>","<:23_ThisIsFine:873337713141624882>","<:06_SadQuokka:873337529775030302>","<:21_Pika:873337681982148628>"])

    await message.channel.send(f"Le bolosse est : {choisi} {emojis}")