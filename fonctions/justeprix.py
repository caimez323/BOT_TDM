import time
import random

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