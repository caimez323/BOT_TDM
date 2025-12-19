
bot_prefix = "!"

async def jvaisVX(message):

    if ('https://twitter.com/') in message.content :
        twitter_link = next((w for w in message.content.split() if "twitter.com" in w), None).replace("https://twitter.com/","https://d.fxtwitter.com/")
        await message.channel.send("[⠀]("+twitter_link+")")

    if ('https://x.com/') in message.content:
        x_link = next((w for w in message.content.split() if "x.com" in w), None).replace("https://x.com/","https://d.fxtwitter.com/")
        await message.channel.send("[⠀]("+x_link+")")

        
    if ("https://www.instagram.com/") in message.content:
        instagram_link = next((w for w in message.content.split() if "instagram.com" in w), None).replace("https://www.instagram.com/","https://www.kkinstagram.com/")
        await message.channel.send("[⠀]("+instagram_link+")")  # Utilisation de l'espace insécable pour masquer le lien
        
    # if message.content.startswith(bot_prefix):
    #     return
        