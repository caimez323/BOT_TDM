import random
import asyncio

async def random_number(message):
  messLen = len(message.content.split())
  if messLen< 2:
    await message.channel.send("Merci de mettre le maximum")
    return
  min,max = None,None
  if messLen == 3:
    min,max = int(message.content.split()[1]),int(message.content.split()[2])
  else:
    max = int(message.content.split()[1])

  choix = random.choice(range(1, max+1)) if not min else random.choice(range(min,max))
  await message.channel.send("Lancement de la roulette...")
  await asyncio.sleep(3)
  await message.channel.send(f"Le numéro **{choix}** !")