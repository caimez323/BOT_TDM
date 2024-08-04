#====================================CLASH====================================

async def clash(message):
  liste = message.content.split(",")
  del liste[0]
  res = "https://porofessor.gg/pregame/euw/"
  for i in liste:
    i=i.replace(" ","")
    res=res+i
    res=res+","
  await message.channel.send(res)