import random
import asyncio
import time

#===============

async def roulette(message):
    if message.content.startswith("!roulette"):
        concurrents = message.content.split()[1:]    
        await message.channel.send("Lancement de la roulette... 🎡")
        await asyncio.sleep(1)
        msg = await message.channel.send("La personne sélectionnée est : ")
        await asyncio.sleep(0.1)
        end_time = asyncio.get_event_loop().time() + random.uniform(5, 10)
        while asyncio.get_event_loop().time() < end_time:
            await asyncio.sleep(0.1)
            index = random.randint(0, len(concurrents) - 1)
            await msg.edit(content="La personne sélectionnée est : " + concurrents[index])
        await msg.edit(content=f"La personne sélectionnée est : **{concurrents[index]}** ! 🥳")

#===============

async def number_rdm(message):
  messLen = len(message.content.split())
  min,max = None,None

  if messLen < 2:
    await message.channel.send("Merci de renseigner la valeur max")
    return  

  if messLen > 3:
    await message.channel.send("Merci de ne renseigner que les valeurs min et max")
    return
  
  val1 = message.content.split()[1]

  if messLen == 2:
    try: 
      int(val1)
    except ValueError: 
      await message.channel.send("Merci de renseigner un nombre entier **supérieur à 1**")
      return
    if int(val1) < 1 : 
      await message.channel.send("Merci de renseigner un nombre entier **supérieur à 1**")
      return
    max = int(val1)
  else:
    val2 = message.content.split()[2]
    try: 
      int(val1)
      int(val2)
    except ValueError: 
      await message.channel.send("Merci de renseigner des **nombres entiers**")
      return
    if int(val1) > int(val2):
      await message.channel.send("La valeur min doit être **inférieure** à la valeur max")
    min,max = int(val1),int(val2)

  choix = random.choice(range(1, max+1)) if min == None else random.choice(range(min,max+1))
  await message.channel.send("Lancement de la roulette...")
  await asyncio.sleep(3)
  await message.channel.send(f"Le numéro **{choix}** !")

#===============

async def justeprix(message,client):
    if len(message.content.split()) == 2:
      max = message.content.split()[1]
      try: 
        int(max)
      except ValueError: 
        await message.channel.send("Merci de renseigner un nombre entier positif")
        return
    else:
      max = 10000
    nombre_deviner = random.randint(0, int(max))
    await message.channel.send(f"Tentez de deviner le nombre (compris entre **0** et **{max}**). Vous avez 30 secondes ! (**stop** pour abandonner)")
    chrono = time.time()

    def checkMessage(tentatives):
      return tentatives.author == message.author and tentatives.channel == message.channel

    while "l'utilisateur n'a pas trouvé le nombre":
        if time.time()-chrono > 30:
          await message.channel.send(f"Temps écoulé, vous avez échoué. Le nombre était {nombre_deviner}")
          return
        tentative = await client.wait_for("message", check = checkMessage)
        try: 
          if tentative.content =="!justeprix":
            return
          if tentative.content.lower() == "stop" or tentative.content.lower() == "!stop" :
            await message.channel.send(f"Vous avez décidé d'abandonner... Le nombre était **{nombre_deviner}**")
            return  
          if int(tentative.content) > int(max) or int(tentative.content) < 0:
            await message.channel.send(f"Erreur, veuillez n'entrer que des nombres compris entre **0** et **{max}**")
            continue
          if int(tentative.content) > nombre_deviner :
            await message.channel.send("C'est **moins** ⬇️")
          elif int(tentative.content) < nombre_deviner :
            await message.channel.send("C'est **plus** ⬆️")
          elif int(tentative.content) == nombre_deviner:
            await message.channel.send(f"C'est **gagné** ! Le nombre était bien **{nombre_deviner}**")
            return
        except :
          await message.channel.send("Erreur, veuillez n'entrer que des **nombres**")

#===============

async def piece(message):
    await message.channel.send("Lancement de la pièce...")
    await asyncio.sleep(1)
    await message.channel.send(random.choice(["Pile","Face"]))

#===============
#===============

async def calculs(message, client):
    if message.content.startswith("!roulette"): await roulette(message)
    if message.content.startswith("!number_rdm"): await number_rdm(message)
    if message.content.startswith("!justeprix"): await justeprix(message, client)
    if message.content.startswith("!piece"): await piece(message)
