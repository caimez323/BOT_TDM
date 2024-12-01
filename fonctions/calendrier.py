import os
import requests
import json
import re

cookie_session = os.getenv("COOKIES_ADV")

# URL de l'API
url = "https://adventofcode.com/2024/leaderboard/private/view/4363575.json"

# Effectuer une requête GET
cookies = {
    "session": cookie_session
}

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def extract_numbers(line):
    match = re.search(r'\[\s*(\d+)-(\d+)\s*\]', line)
    if match:
        first_number = int(match.group(1))
        second_number = int(match.group(2))
        return (first_number, second_number)
    return (float('inf'), float('inf'))


async def adv_code_leaderboard(message):
    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()
    data = response.json()

    bigString = ""
    toBeSorted = []
    for k,v in data['members'].items():
        #TODO maybe sort by order if needed ?
        listejours =""
        for jours,detail in v["completion_day_level"].items():
            if listejours == "":
                listejours = "1"
                continue
            listejours+= ", "+str(jours)
        memberString = "{:<11}".format(v["name"])
        memberString = memberString+ " [ " +str(v["stars"])+ "-"+str(v["local_score"])+ " ]" + "   Jours : "+listejours
        toBeSorted.append(memberString)

    # Trier en utilisant les nombres extraits
    sorted_lines = sorted(toBeSorted, key=extract_numbers,reverse=True)
    for line in sorted_lines:
        bigString+= line+"\n"
    await message.channel.send(bigString)
    return 0


async def calendrier(message):
    if message.content.lower() == "!codeadv": await adv_code_leaderboard(message)

