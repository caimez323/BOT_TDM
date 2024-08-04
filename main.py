import os
import discord

import random
import asyncio

import io
#import pytesseract
#import requests
#from PIL import Image
#from PIL import ImageFilter
import datetime
#pytesseract.pytesseract.tesseract_cmd = "tesseract"
#os.environ["TESSDATA_PREFIX"] = "/home/runner/.apt/usr/share/tesseract-ocr/4.00/tessdata/"

from dotenv import load_dotenv
from discord.utils import get
from discord.ui import Button,View

import fonctions as f


intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('Le bot {0.user} est prêt'.format(client))
  #await schedule_daily_message()


@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content == "!bouton":
      # Créer un bouton
      bouton = Button(label="Cliquez-moi!", style=discord.ButtonStyle.green)

      # Définir ce qui se passe lorsque le bouton est cliqué
      async def on_bouton_click(interaction: discord.Interaction):
          await interaction.response.send_message("Bouton cliqué!")

      # Assigner le callback au bouton
      bouton.callback = on_bouton_click

      # Créer une vue et y ajouter le bouton
      view = View()
      view.add_item(bouton)

      # Envoyer le message avec le bouton
      await message.channel.send("Voici un bouton :", view=view)
#=================================MESSAGES Divers=================================
  
  await f.customWords.customW(message)

#============================MESSAGES pour la VX twitter/insta (Clement)==============================

  await f.jvaisVX.main.VXBot(message)

#===================================ARAM===================================

  if message.content.startswith("!aram_"):
    await message.channel.send(f.ARAM.mainAram.aram_maker(message))


  if message.content.startswith("!reroll"):
    await message.channel.send(f.ARAM.mainAram.reroll(message))

  if message.content.startswith("!random_pick"):
    await message.channel.send(f.ARAM.mainAram.random_pick())   


#===================================COMPOS===================================

  if message.content.lower() == "!challenges":
    await f.COMPO.compos.challenges(message)

  if message.content.startswith("!chall") or message.content.startswith("!comp") or message.content.startswith("!region") or message.content.startswith("!région"):
    await f.COMPO.compos.challenges_images(message)

  if message.content.startswith("!champ"):
    await f.COMPO.compos.challenges_champ(message)
    
#=================================COMMANDES=================================

  if message.content.startswith("!purge") and message.author.id==172362870439411713: #Laiken
    await message.channel.purge(limit=int(message.content.split()[1]))

#====================

  if message.content.lower() == "!w2g":
    await message.channel.send("https://w2g.tv/rooms/yangoo-dnd4zxj3huxhxuj1uq?lang=fr")

#====================
  if message.content.lower() == "!bolosse":
    await f.bolosse(message)

#====================

  if message.content.startswith("!combat"):
    await f.combat(message)
    
#====================

  if message.content.startswith("!piece"):
    await message.channel.send("Lancement de la pièce...")
    await asyncio.sleep(1)
    await message.channel.send(random.choice(["Pile","Face"]))

#====================

  if message.content.startswith("!random_number"):
    await f.random_number(message)

#====================

  if message.content.startswith("!pp"):
    userDesignation = message.content.split()[-1]
    if len(message.mentions)>0:
       await message.channel.send(message.mentions[0].avatar)
       return
    memberList = message.guild.members
    for member in memberList:
      if userDesignation in [member.name,member.nick,member.global_name]:
        await message.channel.send(member.avatar)
        return
    await message.channel.send("Merci d'indiquer un utilisateur correct")

#====================
#TODO 
  if message.content.startswith("!clash"): 
    await f.clash(message)

#====================

  if message.content.startswith("!ytb"):
    await f.youtube_search(message)
    
#====================

  if message.content.lower() == "!justeprix":
    await f.justeprix(message,client)

#====================    

  if message.content.startswith("!duel"):
    await f.duel(message,client)

#=================================MUSIQUE================================= 
#!TODO ?
'''
  if message.content.lower() == "!join":
    await join(message)  

  #====================
  if message.content.lower() == "!leave":
    await leave(message) 

  #====================
  if message.content.lower() == "!stop":
    await stop(message)
'''
#=================================COMPTEUR================================

@client.event
async def on_member_join(member):
  print("commandes")
  for channel in member.guild.channels:
    if channel.name.startswith('Member'):
      await channel.edit(name=f'Members: {(member.guild.member_count)-4}')

@client.event
async def on_member_remove(member):
  print("commandes")
  channel_reunion = member.guild.get_channel(693866632690401280)
  for channel in member.guild.channels:
    if channel.name.startswith('Member'):
      await channel_reunion.send(f"{member.name} a quitté le Discord")
      await channel.edit(name=f'Members: {(member.guild.member_count)-4}')

#==========================================================================
load_dotenv(".env")
TOKEN=os.getenv("TOKEN")
client.run(TOKEN)