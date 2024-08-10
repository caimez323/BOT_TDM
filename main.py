import os
import discord
from discord import app_commands
import random
import asyncio
from dotenv import load_dotenv
import fonctions as f

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

myGuildID = 468724624126115840
load_dotenv(".env")

@tree.command(
    name="commandname",
    description="My first application Command",
    guild=discord.Object(id=myGuildID)
)

async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
  print('Le bot {0.user} est prêt'.format(client))

  #Slash command
  await tree.sync(guild=discord.Object(id=myGuildID))


@client.event
async def on_message(message):

  if message.author == client.user:
    return

#==========> HELP <==========
  if message.content.startswith("!help"):
    await f.help(message)

#==========> CUSTOM MSG <==========  
  await f.customWords(message)

#==========> VX Twitter/Insta <==========
  await f.jvaisVX(message)
  
#==========> SNIFSNOUF <==========
  await f.snifsnouf(message)

#==========> MUSIQUE <==========
  await f.music(message,client)

#==========> ARAM <==========
  await f.mainAram(message)

#==========> CALCULS <==========
  await f.calculs(message,client)

#==========> COMPOS <==========
  await f.compos(message)

#==========> FIGHTS <==========
  await f.fights(message,client)

#==========> RECHERCHE <==========
  await f.recherche(message)

  #await f.jumbledWordsResolver(message)

#TODO 
  if message.content.startswith("!clash"): 
    await f.clash(message)

#================================= COMMANDES =================================

  if message.content.startswith("!purge") and message.author.id==172362870439411713: #Laiken
    await message.channel.purge(limit=int(message.content.split()[1]))
    
#================================= MUSIQUE ================================= 
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
#================================= COMPTEUR ================================

@client.event
async def on_member_join(member):
  for channel in member.guild.channels:
    if channel.name.startswith('Member'):
      await channel.edit(name=f'Members: {(member.guild.member_count)-4}')

@client.event
async def on_member_remove(member):
  channel_reunion = member.guild.get_channel(693866632690401280)
  for channel in member.guild.channels:
    if channel.name.startswith('Member'):
      await channel_reunion.send(f"{member.name} a quitté le Discord")
      await channel.edit(name=f'Members: {(member.guild.member_count)-4}')

#==========================================================================

TOKEN=os.getenv("TOKEN")
client.run(TOKEN)