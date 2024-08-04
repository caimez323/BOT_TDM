import urllib.parse, urllib.request, re
from pytube import YouTube
import discord
from discord.ui import View

#On peut également ajouter des boutons liens https://gist.github.com/lykn/bac99b06d45ff8eed34c2220d86b6bf4
class PaginationView(View):
    def __init__(self,pages):
        super().__init__()
        self.current_page = 0
        self.pages = pages
    
    @discord.ui.button(label="", style=discord.ButtonStyle.red,emoji="🎁")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await self.update_message(interaction)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.green,emoji="▶️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.pages)
        await self.update_message(interaction)
    
    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)
        
def get_video_title(url):
    try:
        # Créez un objet YouTube en utilisant l'URL de la vidéo
        yt = YouTube(url)
        # Retournez le titre de la vidéo
        return yt.title
    except Exception as e:
        return f"Une erreur est survenue : {e}"

def get_video_info(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    return {
        "title": get_video_title(url),  # Titre de la vidéo
        "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",  # Miniature de la vidéo
        "video_url": url
    }

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
  # Créez les pages d'embed
  idList = [link.replace("http://www.youtube.com/watch?v=","") for link in checkList]
  pages = []
  SideColorList=[discord.Color.red(),discord.Color.blue(),discord.Color.green()]
  for index,id in enumerate(idList):
    payload = discord.Embed(
        title=get_video_info(id)["title"],
        description=f"[Regardez ici]({get_video_info(id)['video_url']})",
        color=SideColorList[index]
    ).set_image(url=get_video_info(id)["thumbnail_url"])
    pages.append(payload)
  await message.channel.send(embed=pages[0], view=PaginationView(pages))
  await botMsg.delete()