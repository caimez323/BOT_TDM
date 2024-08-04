import random
async def customW(message):
  if message.content.lower() == "hello" or message.content.lower() == "salut":
    await message.channel.send("Hello! <:05_CuteQuokka:873337522174959626>")

  if message.content.lower() == "kebab":
    await message.channel.send("J'aime les kebabs")

  if message.content.lower() == "croco":
    await message.channel.send("🐊 🐊 🐊")

  if message.content.lower() == "ping":
    coeff = 0.95
    reponses = ["pong 🏓","J'ai perdu... <:43_PTN_ZBI:873337845052477501>"]
    coeffs = [coeff,1-coeff]
    await message.channel.send(random.choices(reponses,coeffs)[0]) 

  if message.content.lower() == "cochon":
    await message.channel.send("https://tenor.com/view/chewing-viralhog-cute-pig-chew-gif-17948209")

  if message.content.lower() == "wéwéwé":
    await message.channel.send("ouais ouais ouais <:25_ClaFteChezImnot:873337734155083786>") 

  #Not sure this works
  if message.content.lower() == "!member_count" :
    channel_members = message.guild.get_channel(866455272478343208)
    number = message.guild.member_count
    await channel_members.edit(name=f"Members: {number-3}")