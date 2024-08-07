import discord
import asyncio

#===============

async def challenges(message):
  embed = discord.Embed(title = "", 
  description = " ", 
  colour = discord.Colour.green())

  embed.set_author(name='Challenges', icon_url=("https://cdn.discordapp.com/attachments/888765508042768445/991727218176839710/lol.jpg"))

  embed.add_field(name='**\n• Champions Compos**', value="\n**1.** [Ultimes ultimes](https://bit.ly/3a39J6M)\n**2.** [Mais tu vas mourir oui ?!](https://bit.ly/3OLoARS)\n**3.** [Nulle part où se cacher](https://bit.ly/3y3HrRI)\n**4.** [Gardons nos distances](https://bit.ly/3udGjcT)\n**5.** [Viens par ici !](https://bit.ly/3y3Ne9Q)\n**6.** [On ne bouge plus](https://bit.ly/3y4PqOj)\n**7.** [Protection rapprochée](https://bit.ly/3nnPNi9)\n**8.** [C'est un piège !](https://bit.ly/3OR1SrL)\n**9.** [Où ils sont passés ?](https://bit.ly/3QXqQYj)\n**10.** [Les invocateurs de la Faille](https://bit.ly/3y19am1)\n**11.** [Et le terrain fut](https://bit.ly/3u9yJ3e)\n**12.** [Équipe homogène](https://bit.ly/3I9mQzV)",  inline=False)

  embed.add_field(name='**\n• Champions Régions**', value='\n**1.** [Bandle](https://bit.ly/3OQU4pX)\n**2.** [Bilgewater](https://bit.ly/bilgewater01)\n**3.** [Demacia](https://bit.ly/3npguTs)\n**4.** [Freljord](https://bit.ly/3ytZYYA)\n**5.** [Ionia](https://bit.ly/3ubJrGr)\n**6.** [Ixtal](https://bit.ly/ixtal01)\n**7.** [Noxus](https://bit.ly/3y4ZXsL)\n**8.** [Piltover](https://bit.ly/3OvfxVy)\n**9.** [îles Obscures](https://bit.ly/3nq2d8W)\n**10.** [Shurima](https://bit.ly/shurima01)\n**11.** [Targon](https://bit.ly/3OyQxg6)\n**12.** [Néant](https://bit.ly/3QXJZti)\n**13.** [Zaun](https://bit.ly/3OPJXlk)', 
  inline=False)

  embed.set_footer(text=message.author.name, icon_url=message.author.avatar)

  await message.channel.send(embed=embed)

#===============

async def challenges_images(message):
  
  if len(message.content.split())<2:
    await message.channel.send("Merci d'ajouter un chall")
    return
  chall = message.content.split()[1]

  embed = discord.Embed(title = "", 
  description = "", 
  colour = discord.Colour.dark_teal())

  embed.set_author(name='Challenges', icon_url=("https://cdn.discordapp.com/attachments/888765508042768445/991727218176839710/lol.jpg"))

  if chall == "1a" or chall == "ultimes" or chall == "Ultimes":
    embed.add_field(name='Ultimes ultimes', value="Gagnez avec un groupe de 5, avec 3+ __ultimes à large zone d'effet__", inline=False)
    embed.set_image(url='https://bit.ly/3a39J6M')
  elif chall == "2a" or chall == "réanimations" or chall == "Réanimations":
    embed.add_field(name='Mais tu vas mourir oui ?!', value="Gagnez avec un groupe de 5, avec 3+ __réanimations__", inline=False)
    embed.set_image(url='https://bit.ly/3OLoARS')
  elif chall == "3a" or chall == "compétences" or chall == "Compétences" or chall == "globales" or chall == "Globales":
    embed.add_field(name='Nulle part où se cacher', value="Gagnez avec un groupe de 5, avec 3+ __compétences globales__", inline=False)
    embed.set_image(url='https://bit.ly/3y3HrRI')
  elif chall == "4a" or chall == "poke" or chall == "Poke":
    embed.add_field(name='Gardons nos distances', value="Gagnez avec un groupe de 5, avec 3+ __champions qui \"pokent\"__", inline=False)
    embed.set_image(url='https://bit.ly/3udGjcT')
  elif chall == "5a" or chall == "cc" or chall == "CC":
    embed.add_field(name='Viens par ici !', value="Gagnez avec un groupe de 5, avec 3+ __effets de déplacement des ennemis__", inline=False)
    embed.set_image(url='https://bit.ly/3y3Ne9Q')
  elif chall == "6a" or chall == "immobilisations" or chall == "Immobilisations" or chall == "stun" or chall == "Stun":
    embed.add_field(name='On ne bouge plus', value="Gagnez avec un groupe de 5, avec 3+ __champions qui ont 2+ immobilisations__", inline=False)
    embed.set_image(url='https://bit.ly/3y4PqOj')
  elif chall == "7a" or chall == "boucliers" or chall == "Boucliers" or chall == "soins" or chall == "Soins":
    embed.add_field(name='Protection rapprochée', value="Gagnez avec un groupe de 5, avec 3+ __champions à boucliers ou soins__", inline=False)
    embed.set_image(url='https://bit.ly/3nnPNi9')
  elif chall == "8a" or chall == "pièges" or chall == "Pièges":
    embed.add_field(name="C'est un piège !", value="Gagnez avec un groupe de 5, avec 3+ __pièges__", inline=False)
    embed.set_image(url='https://bit.ly/3OR1SrL')
  elif chall == "9a" or chall == "furtifs" or chall == "Furtifs" or chall == "invisibles" or chall == "Invisibles":
    embed.add_field(name='Où ils sont passés ?', value="Gagnez avec un groupe de 5, avec 3+ __champions furtifs__", inline=False)
    embed.set_image(url='https://bit.ly/3QXqQYj')
  elif chall == "10a" or chall == "invocations" or chall == "Invocations" or chall == "familiers" or chall == "Familiers":
    embed.add_field(name='Les invocateurs de la Faille', value="Gagnez avec un groupe de 5, avec 5 __champions à invocations ou familiers__", inline=False)
    embed.set_image(url='https://bit.ly/3y19am1')
  elif chall == "11a" or chall == "créateurs" or chall == "Créateurs" or chall == "terrain" or chall == "Terrain":
    embed.add_field(name='Et le terrain fut', value="Gagnez avec un groupe de 5, avec 3+ __créateurs de terrain__", inline=False)
    embed.set_image(url='https://bit.ly/3u9yJ3e')
  elif chall == "12a" or chall == "classe" or chall == "Classe" or chall.lower == "homogène" or chall == "Homogène":
    embed.add_field(name='Équipe homogène', value="Gagnez avec un groupe de 5 champions __d'une même classe__", inline=False)
    embed.set_image(url='https://bit.ly/3I9mQzV')
  elif chall == "1b" or chall.lower() == "bandle":
    await message.channel.send("oui")
    embed.add_field(name='5 sur 5', value="Gagnez avec un groupe de 5 __champions de Bandle__", inline=False)
    embed.set_image(url='https://bit.ly/3OQU4pX')
  elif chall == "2b" or chall.lower() == "bilgewater":
    embed.add_field(name='Naufrageurs', value="Gagnez avec un groupe de 5 __champions de Bilgewater__", inline=False)
    embed.set_image(url='https://bit.ly/bilgewater01')
  elif chall == "3b" or chall.lower() == "demacia":
    embed.add_field(name='POUR DEMACIA', value="Gagnez avec un groupe de 5 __champions de Demacia__", inline=False)
    embed.set_image(url='https://bit.ly/3npguTs')
  elif chall == "4b" or chall.lower() == "freljord":
    embed.add_field(name='Premiers de la glace', value="Gagnez avec un groupe de 5 __champions de Freljord__", inline=False)
    embed.set_image(url='https://bit.ly/3ytZYYA')
  elif chall == "5b" or chall.lower() == "ionia":
    embed.add_field(name="Tendez l'autre Wuju", value="Gagnez avec un groupe de 5 __champions d'Ionia__", inline=False)
    embed.set_image(url='https://bit.ly/3ubJrGr')
  elif chall == "6b" or chall.lower() == "ixtal":
    embed.add_field(name='Terrible jungle', value="Gagnez avec un groupe de 5 __champions d'Ixtal'__", inline=False)
    embed.set_image(url='https://bit.ly/ixtal01')
  elif chall == "7b" or chall.lower() == "noxus":
    embed.add_field(name='La force avant tout', value="Gagnez avec un groupe de 5 __champions de Noxus__", inline=False)
    embed.set_image(url='https://bit.ly/3y4ZXsL')
  elif chall == "8b" or chall.lower() == "piltover":
    embed.add_field(name="Innovateurs", value="Gagnez avec un groupe de 5 __champions de Piltover__", inline=False)
    embed.set_image(url='https://bit.ly/3OvfxVy')
  elif chall == "9b" or chall.lower() == "îles" or chall.lower() == "iles":
    embed.add_field(name='Terreurs des îles', value="Gagnez avec un groupe de 5 __champions des Îles obscures__", inline=False)
    embed.set_image(url='https://bit.ly/3nq2d8W')
  elif chall == "10b" or chall.lower() == "shurima":
    embed.add_field(name='Artistes shurimartiaux', value="Gagnez avec un groupe de 5 __champions de Shurima__", inline=False)
    embed.set_image(url='https://bit.ly/shurima01')
  elif chall == "11b" or chall.lower() == "targon":
    embed.add_field(name='Maîtres de la montagne', value="Gagnez avec un groupe de 5 __champions de Targon__", inline=False)
    embed.set_image(url='https://bit.ly/3OyQxg6')
  elif chall == "12b" or chall.lower() == "néant" or chall.lower() == "neant":
    embed.add_field(name='(Cris inhumains)', value="Gagnez avec un groupe de 5 __champions du Néant__", inline=False)
    embed.set_image(url='https://bit.ly/3QXJZti')
  elif chall == "13b" or chall.lower() == "zaun":
    embed.add_field(name='Troupe techno-chimique', value="Gagnez avec un groupe de 5 __champions de Zaun__", inline=False)
    embed.set_image(url='https://bit.ly/3OPJXlk')
    
  else:
    await message.channel.send("Ce challenge ne fait pas partie de la liste :")
    await asyncio.sleep(1)
    await challenges(message)
    return

  embed.set_footer(text=message.author.name, icon_url=message.author.avatar)

  await message.channel.send(embed=embed)

#===============

async def challenges_champ(message):
  rien = False
  if len(message.content.split())<2:
    await message.channel.send("Merci d'ajouter un chall")
    return
  chall = message.content.split()[1]
  if chall.lower() == "lulu" or chall.lower() == "rumble" or chall.lower() == "teemo" or chall.lower() == "tristana" or chall.lower() == "veigar" or chall.lower() == "vex" or chall.lower() == "yuumi":
      region = "à **Bandle**"
  elif chall.lower() == "gangplank" or chall.lower() == "graves" or chall.lower() == "illaoi" or chall.lower() == "miss" or chall.lower() == "miss_fortune" or chall.lower() == "mf" or chall.lower() == "nautilus" or chall.lower() == "nilah" or chall.lower() == "pyke" or chall.lower() == "tahm_kench" or chall.lower() == "tk" or chall.lower() == "twisted_fate" or chall.lower() == "tf" or chall.lower() == "twisted" or chall.lower() == "nilah":
      region = "à **Bilgewater**"
  elif chall.lower() == "fiora" or chall.lower() == "galio" or chall.lower() == "garen" or chall.lower() == "jarvan_IV" or chall.lower() == "jarvan" or chall.lower() == "j4" or chall.lower() == "kayle" or chall.lower() == "lucian" or chall.lower() == "lux" or chall.lower() == "morgana" or chall.lower() == "quinn" or chall.lower() == "shyvana" or chall.lower() == "sona" or chall.lower() == "sylas" or chall.lower() == "vayne" or chall.lower() == "xin_zhao" or chall.lower() == "xin":
      region = "à **Demacia**"
  elif chall.lower() == "anivia" or chall.lower() == "ashe" or chall.lower() == "braum" or chall.lower() == "gragas" or chall.lower() == "lissandra" or chall.lower() == "nunu" or chall.lower() == "olaf" or chall.lower() == "ornn" or chall.lower() == "sejuani" or chall.lower() == "trundle" or chall.lower() == "tryndamere" or chall.lower() == "udyr" or chall.lower() == "volibear":
      region = "à **Freljord**"
  elif chall.lower() == "ahri" or chall.lower() == "akali" or chall.lower() == "irelia" or chall.lower() == "ivern" or chall.lower() == "jhin" or chall.lower() == "karma" or chall.lower() == "kayn" or chall.lower() == "lee_sin" or chall.lower() == "lee" or chall.lower() == "lillia" or chall.lower() == "yi" or chall.lower() == "master_yi" or chall.lower() == "maitre_yi" or chall.lower() == "rakan" or chall.lower() == "sett" or chall.lower() == "shen" or chall.lower() == "syndra" or chall.lower() == "varus" or chall.lower() == "wukong" or chall.lower() == "xayah" or chall.lower() == "yasuo" or chall.lower() == "yone" or chall.lower() == "zed":
      region = "à **Ionia**"
  elif chall.lower() == "malphite" or chall.lower() == "milio" or chall.lower() == "neeko" or chall.lower() == "nidalee" or chall.lower() == "qiyana" or chall.lower() == "rengar" or chall.lower() == "zyra":
      region = "à **Ixtal**"
  elif chall.lower() == "cassiopeia" or chall.lower() == "cassio" or chall.lower() == "darius" or chall.lower() == "draven" or chall.lower() == "katarina" or chall.lower() == "leblanc" or chall.lower() == "rell" or chall.lower() == "riven" or chall.lower() == "samira" or chall.lower() == "sion" or chall.lower() == "swain" or chall.lower() == "talon" or chall.lower() == "vladimir":
      region = "à **Noxus**"
  elif chall.lower() == "caitlyn" or chall.lower() == "camille" or chall.lower() == "ezreal" or chall.lower() == "jayce" or chall.lower() == "orianna" or chall.lower() == "séraphine":
      region = "à **Piltover**"
  elif chall.lower() == "elise" or chall.lower() == "evelynn" or chall.lower() == "fiddlesticks" or chall.lower() == "gwen" or chall.lower() == "hecarim" or chall.lower() == "kalista" or chall.lower() == "karthus" or chall.lower() == "maokai" or chall.lower() == "senna" or chall.lower() == "thresh" or chall.lower() == "viego" or chall.lower() == "yorick":
      region = "aux **Îles Obscures**"
  elif chall.lower() == "akshan" or chall.lower() == "amumu" or chall.lower() == "azir" or chall.lower() == "k'santé" or chall.lower() == "k'sante" or chall.lower() == "ksante" or chall.lower() == "ksanté" or chall.lower() == "nasus" or chall.lower() == "rammus" or chall.lower() == "renekton" or chall.lower() == "sivir" or chall.lower() == "skarner" or chall.lower() == "taliyah" or chall.lower() == "xerath" or chall.lower() == "zilean":
      region = "à **Shurima**"
  elif chall.lower() == "aphelios" or chall.lower() == "aurelion_sol" or chall.lower() == "aurelion" or chall.lower() == "diana" or chall.lower() == "leona" or chall.lower() == "pantheon" or chall.lower() == "soraka" or chall.lower() == "taric" or chall.lower() == "zoé" or chall.lower() == "zoe":
      region = "au **Mont Targon**"
  elif chall.lower() == "bel'veth" or chall.lower() == "cho'gath" or chall.lower() == "kai'sa" or chall.lower() == "kassadin" or chall.lower() == "kha'zix" or chall.lower() == "kog'maw" or chall.lower() == "malzahar" or chall.lower() == "rek'sai" or chall.lower() == "vel'koz":
      region = "au **Néant**"
  elif chall.lower() == "blitzcrank" or chall.lower() == "blitz" or chall.lower() == "mundo" or chall.lower() == "ekko" or chall.lower() == "janna" or chall.lower() == "jinx" or chall.lower() == "renata" or chall.lower() == "singed" or chall.lower() == "twitch" or chall.lower() == "urgot" or chall.lower() == "viktor" or chall.lower() == "warwick" or chall.lower() == "zac" or chall.lower() == "zeri":
      region = "à **Zaun**"
  elif chall.lower() == "corki" or chall.lower() == "heimerdinger":
     region = "à **Bandle** et à **Piltover**"
  elif chall.lower() == "fizz":
     region = "à **Bandle** et à **Bilgewater**"
  elif chall.lower() == "kennen":
     region = "à **Bandle** et à **Ionia**"   
  elif chall.lower() == "gnar":
     region = "à **Bandle** et à **Freljord**" 
  elif chall.lower() == "kled":
     region = "à **Bandle** et à **Noxus**" 
  elif chall.lower() == "poppy":
     region = "à **Bandle** et à **Demacia**"
  elif chall.lower() == "ziggs":
     region = "à **Bandle** et à **Zaun**"
  elif chall.lower() == "kindred" or chall.lower() == "bard" or chall.lower() == "aatrox" or chall.lower() == "nami" or chall.lower() == "brand" or chall.lower() == "nocturne" or chall.lower() == "alistar" or chall.lower() == "annie" or chall.lower() == "jax" or chall.lower() == "mordekaiser" or chall.lower() == "ryze" or chall.lower() == "shaco" :
     rien = True
     chall = chall.lower()
     region = ""

  if not rien:  
    await message.channel.send(f"**{chall}** appartient {region}")
  else:
     await message.channel.send(f"**{chall}** n'appartient à **aucune** région.")

#===============
#===============

async def compos(message):
  if message.content.lower() == "!challenges": await challenges(message)
  elif message.content.startswith("!chall") or message.content.startswith("!compo"): await challenges_images(message)
  if message.content.startswith("!region"): await challenges_champ(message)