import urllib.parse, urllib.request, re
from pytube import YouTube
import discord
from discord.ext import commands
from discord.ui import View, Button

#===============

#On peut également ajouter des boutons liens https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4

class PaginationView(View):
    def __init__(self, links):
        super().__init__()
        self.links = links
        self.current_link_index = 0

    @discord.ui.button(label="", style=discord.ButtonStyle.green,emoji="<:240_Amoa:1017107527961424014>")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_link_index = (self.current_link_index - 1) % len(self.links)
        await self.update_message(interaction)

    @discord.ui.button(label="", style=discord.ButtonStyle.green,emoji="<:238_Maraiste:1133163882999971991>")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_link_index = (self.current_link_index + 1) % len(self.links)
        await self.update_message(interaction)

    async def update_message(self, interaction: discord.Interaction):
        link = self.links[self.current_link_index]
        await interaction.response.edit_message(content=link, view=self)

async def youtube_search(message):

  liste = message.content.split()
  del liste[0]
  search = ""
  for mots in liste:
    search = search + mots + " "

  search = search[:-1]
  botMsg = await message.channel.send("Recherche en cours pour {}...".format(search))
  query_string = urllib.parse.urlencode({'search_query': search})
  htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)

  search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
  displayString = ""
  checkList = []
  index = 0
  while len(checkList) <3 and index <9999:
    theString = 'http://www.youtube.com/watch?v={}'.format(search_results[index])
    index+=1
    if theString in checkList:
      continue
    checkList.append(theString)
    displayString+=(theString+"\n")

  await message.channel.send(content=checkList[0], view=PaginationView(checkList))
  await botMsg.delete()

#===============

async def w2g(message):
    await message.channel.send("https://w2g.tv/rooms/yangoo-dnd4zxj3huxhxuj1uq?lang=fr")

#===============

async def pp(message):
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

#===============



async def cherche_kopain(message):
  BOTID = [850798626946809867,1269278012864594061]
  messageArgs = message.content.split()[1:]
  mention,deranger = False,False
  if("-m" in messageArgs):
     mention = True
  if("-d" in messageArgs):
     deranger = True
  if deranger:
    online_members = [member for member in message.guild.members if message.channel.permissions_for(member).read_messages and member.id not in BOTID and member.status in {discord.Status.online, discord.Status.idle, discord.Status.dnd}]
  else:
    online_members = [member for member in message.guild.members if message.channel.permissions_for(member).read_messages and member.id not in BOTID and member.status in {discord.Status.online, discord.Status.idle}]

  Ts = "Voici la liste des utilisateurs susceptibles d'être ligne :\n"
  for m in online_members:
    Ts+= ("<@{}>\n".format(str(m.id)) if mention else "{}\n".format(str(m.name)))
  await message.channel.send(Ts)
#===============

async def recherche(message):
    if message.content.lower() == "!w2g": await w2g(message)
    if message.content.startswith("!pp"): await pp(message)
    if message.content.startswith("!ytb"): await youtube_search(message)
    if message.content.startswith("!kop1"): await cherche_kopain(message)
    # if message.content.startswith("!clash"): await clash(message, client)