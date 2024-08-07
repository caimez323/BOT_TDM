import random
import asyncio

async def random_number(message):
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