import time
import random

async def justeprix(message,client):
    nombre_deviner = random.randint(0, 10000)
    await message.channel.send("Tentez de deviner le nombre (compris entre 0 et 10 000). Vous avez 30 secondes ! (stop pour abandonner)")
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
          if tentative.content == "stop" :
            await message.channel.send(f"Vous avez décidé d'abandonner... Le nombre était {nombre_deviner}")
            return  
          if int(tentative.content) > 10000 or int(tentative.content)< 0:
            await message.channel.send("Erreur, veuillez n'entrer que des nombres compris **entre 0 et 10 000**")
            continue
          if int(tentative.content) > nombre_deviner :
            await message.channel.send("C'est moins")
            print ("Chrono :",time.time()-chrono)
          elif int(tentative.content) < nombre_deviner :
            await message.channel.send("C'est plus")
            print ("Chrono :",time.time()-chrono)
          elif int(tentative.content) == nombre_deviner:
            await message.channel.send(f"C'est gagné ! Le nombre était bien {nombre_deviner}")
            print ("Chrono :",time.time()-chrono)
            return
        except :
          await message.channel.send("Erreur, veuillez n'entrer que des **nombres**")