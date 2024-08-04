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

import fonctions as f

from Commandes.duel import duel
from Commandes.justeprix import justeprix
from Commandes.price import price,priceu
from swinny.swinny import swinny_collection,swinny_drawings,swinny_musics
from swinny.hugo import hugo_destinations
from swinny.jeux import jeux1,jeux2



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

  if message.content.startswith("!clash"):
    await f.clash(message)

#====================

  if message.content.startswith("!ytb"):
    await f.youtube_search(message)

#====================

  if message.content.lower() == "!justeprix":
    await justeprix(message,client)

#====================    

  if message.content.startswith("!duel"):
    await duel(message,client)

#====================    

  if message.content.startswith("!price"):
    await price(message)

  if message.content.startswith("!lvlprice"):
    await priceu(message)

#=================================SWINNY=================================

  if message.content.lower() == "!swinny_collection":
    await swinny_collection(message)  

  if message.content.startswith("!dessin"):
    await swinny_drawings(message)  

  if message.content.lower() == "!swinny_musics":
    await swinny_musics(message) 
    
  if message.content.lower() == "!hugo_destinations":
    await hugo_destinations(message)

  if message.content.lower() == "!jeux1":
    await jeux1(message)

  if message.content.lower() == "!jeux2":
    await jeux2(message)

#=================================MUSIQUE=================================
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
  channel_réunion = member.guild.get_channel(693866632690401280)
  for channel in member.guild.channels:
    if channel.name.startswith('Member'):
      await channel_réunion.send(f"{member.name} a quitté le Discord")
      await channel.edit(name=f'Members: {(member.guild.member_count)-4}')

#==========================================================================

# @client.event
# async def on_message_edit(before,after):
#   channel_test = before.guild.get_channel(1039948872849555476)
#   if before.channel == channel_test or before.author.id == 850798626946809867 or before.content.startswith('http') or before.author.id == 432610292342587392:
#     return
#   try:
#     await channel_test.send(f"**Message modifié** dans {before.channel.mention} :\n{before.author.name} (*{before.created_at.day}/{before.created_at.month}/{before.created_at.year} | {before.created_at.hour+2}:{before.created_at.minute}*) : {before.attachments[0]} ➡️ {after.content}")
#   except IndexError:
#     pass
#   if not before.attachments:
#     await channel_test.send(f"**Message modifié** dans {before.channel.mention} :\n{before.author.name} (*{before.created_at.day}/{before.created_at.month}/{before.created_at.year} | {before.created_at.hour+2}:{before.created_at.minute}*) : {before.content} ➡️ {after.content}")

# #====================
# @client.event
# async def on_message_delete(message):
#   channel_test = message.guild.get_channel(1039948872849555476)
#   if message.channel == channel_test or message.author.id == 850798626946809867:
#     return
#   try:
#     await channel_test.send(f"**Message supprimé** dans {message.channel.mention} :\n{message.author.name} (*{message.created_at.day}/{message.created_at.month}/{message.created_at.year} | {message.created_at.hour+2}:{message.created_at.minute}*) : {message.attachments[0]}")
#   except IndexError:
#     pass
#   if not message.attachments:
#     await channel_test.send(f"**Message supprimé** dans {message.channel.mention} :\n{message.author.name} (*{message.created_at.day}/{message.created_at.month}/{message.created_at.year} | {message.created_at.hour+2}:{message.created_at.minute}*) : {message.content}")

#====================

@client.event
async def on_raw_reaction_add(payload):
  await tournoi_add(payload,client)
  print("========================================")
  print("Added :", payload.member.name, payload.emoji.name)
  print("========================================")

@client.event
async def on_raw_reaction_remove(payload):
  await tournoi_remove(payload,client)
  print("========================================")
  guild = client.get_guild(payload.guild_id) 
  member = get(guild.members, id=payload.user_id)
  print("Removed :", member.name, payload.emoji.name)
  print("========================================")

#====================
  
'''
@client.event
async def schedule_daily_message():
  now = datetime.datetime.now()
  print(now)
  then = now + datetime.timedelta(days=1)
  then = now.replace(hour=13, minute=1)
  wait_time = (then-now).total_seconds()
  await asyncio.sleep(wait_time)

  channel = client.get_channel(693866632690401280)
  user_id = "510537578961829890"
  await channel.send(f"<@{user_id}> cc c'l'heure mrc ")
'''
  
#==========================================================================



#==========================================================================
load_dotenv(".env")
TOKEN=os.getenv("TOKEN")
client.run(TOKEN)