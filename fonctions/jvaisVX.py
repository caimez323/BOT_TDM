
reputation_dict = {}
bot_prefix = "!"

async def jvaisVX(message):

    if ('https://twitter.com/') in message.content :
        await message.channel.send(f"-# essaie {message.content.replace("https://twitter.com/","https://vxtwitter.com/")}")
        # await message.channel.send(message.content.replace("https://twitter.com/","https://vxtwitter.com/") + " (" + message.author.name + ")")
        # await message.delete()

    if ('https://x.com/') in message.content:
        await message.channel.send(f"-# essaie {message.content.replace("https://x.com/","https://fixvx.com/")}")
        # await message.channel.send(message.content.replace("https://x.com/","https://fixvx.com/") + " (" + message.author.name + ")")
        # await message.delete()
        
    # if ("https://www.instagram.com/") in message.content:
    #     await message.channel.send(message.content.replace("https://www.instagram.com/","https://www.ddinstagram.com/") + " (" + message.author.name + ")")
    #     await message.delete()
        
    # if message.content.startswith(bot_prefix):
    #     return
        