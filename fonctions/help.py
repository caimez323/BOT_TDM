import discord

async def help(message):
    embed = discord.Embed(title = "Help Embed", 
    description = "TDM helper", 
    colour = discord.Colour.green())

    embed.add_field(name='**!duel**',value=" : fait un duel",  inline=False)

    embed.set_footer(text=message.author.name, icon_url=message.author.avatar)

    await message.channel.send(embed=embed)
    """
    displayString = ""
    displayString += "> Voici la liste des commandes disponibles : \n"
    
    await message.channel.send(displayString)
    """