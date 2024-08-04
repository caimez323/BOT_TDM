import urllib.parse, urllib.request, re

async def youtube_search(message):
  liste = message.content.split()
  del liste[0]
  search = ""
  for mots in liste:
    search = search + mots + " "

  search = search[:-1]

  query_string = urllib.parse.urlencode({'search_query': search})
  htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)

  search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
  displayString = ""
  checkList = []
  index = 0
  while len(checkList) <3 and index <9999:
    print(index)
    theString = 'http://www.youtube.com/watch?v={}'.format(search_results[index])
    index+=1
    if theString in checkList:
      continue
    checkList.append(theString)
    displayString+=(theString+"\n")
  await message.channel.send(displayString)