import urllib.parse, urllib.request, re
from pytube import YouTube
import discord
from discord.ui import View, Button

#On peut également ajouter des boutons liens https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4


class PaginationView(View):
    def __init__(self, links):
        super().__init__()
        self.links = links
        self.current_link_index = 0

    @discord.ui.button(label="", style=discord.ButtonStyle.red, emoji="<cle1:1269619584688979978>")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_link_index = (self.current_link_index - 1) % len(self.links)
        await self.update_message(interaction)

    @discord.ui.button(label="", style=discord.ButtonStyle.green, emoji="<cle2:1269619569463394367>")
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