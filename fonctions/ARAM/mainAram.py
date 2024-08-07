import random

#===============

async def aram_maker(message):
  teamType = message.content.split()[0].replace("!aram_","")
  
  if teamType not in ["rdm","teamrdm"]:
    return "Merci de choisir un type de team valide : rdm ou teamrdm"

  playersList = message.content.split()[1:]
  nbrJoueurs = len(playersList)

  if nbrJoueurs %2 != 0 :
    return "Merci de mettre un nombre pair de joueurs"
  
  if teamType == "teamrdm":
    random.shuffle(playersList)
    
  mid = int(nbrJoueurs/2)
  team_1 = playersList[:mid]
  team_2 = playersList[mid:]

  await message.channel.send(randomizeur(team_1,team_2))

#====randomizeur

def randomizeur(team_1,team_2):
  with open("fonctions/ARAM/persos_lol.txt","r") as file:
    Champions_list = [name.replace("\n","") for name in list(file.readlines())]

  players=team_1+team_2
  picks=[]

  nbr_players=len(players)

  for _ in range(nbr_players*2): #Since each player have 2 champs
    pick=random.choice(Champions_list) 
    picks.append(pick)
    Champions_list.remove(pick)
  
  #Display 
  finalString = ""

  for i,champ in enumerate(picks):
    if i == 0 or i == int(nbr_players/2)*2: 
      finalString +="{}────────────────────Team n°{}───────────────────".format("```" if i == 0 else "\n",1 if i == 0 else 2)
    if i%2 == 0:
      finalString += '\n{:<9}'.format(players[int(i/2)])
    finalString += " {} {:<12}".format(" : " if i%2 == 0 else "|" ,champ)
  return finalString+"```"

#===============

async def reroll(message):
  if len(message.content.split())<2:
    return ("Merci d'envoyer le nom de la personne à reroll")
  with open("fonctions/ARAM/persos_lol.txt","r") as file:
    Champions_list = [name.replace("\n","") for name in list(file.readlines())]
  pick_reroll1=random.choice(Champions_list)
  Champions_list.remove(pick_reroll1)
  pick_reroll2=random.choice(Champions_list)

  await message.channel.send(' '.join(["""```─────────────────────Reroll────────────────────""",'\n',
    '{:<9}'.format(message.content.split()[1]),'{:<3}'.format(" : "),'{:<12}'.format(pick_reroll1),'{:^3}'.format("|"), '{:<12}'.format(pick_reroll2),'\n',
"""──────────────────────────────────────────────```"""]))

#===============

async def pick_rdm(message):
  with open("fonctions/ARAM/persos_lol.txt","r") as file:
    Champions_list = [name.replace("\n","") for name in list(file.readlines())]
    await message.channel.send("```──────────────────────────────────────────────\nChampion : "+random.choice(Champions_list)+"\n──────────────────────────────────────────────```")

#===============
#===============

async def mainAram(message):
  if message.content.startswith("!aram_"): await aram_maker(message)
  if message.content.startswith("!reroll"): await reroll(message)
  if message.content.startswith("!pick_rdm"): await pick_rdm(message)