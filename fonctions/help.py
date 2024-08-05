import discord
from discord.ui import View


class HelperView(View):
    def __init__(self,pages):
        super().__init__()
        self.current_page = 0
        self.pages = pages
    
    @discord.ui.button(label="", style=discord.ButtonStyle.red,emoji="🎁")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await self.update_message(interaction)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.green,emoji="▶️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.pages)
        await self.update_message(interaction)
    
    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.current_page]
        await interaction.response.edit_message(embed=embed, view=self)

def helpPagesCreation(message):
    #===========================================================
    # POUR AJOUTER UNE COMMANDE ICI, MERCI DE SUIVRE LA SYNTAXE
    #===========================================================
    COMMAND_LIST = {\
        "!duel":"Permet de défier en duel",\
        "!snifHelp" : "Affiche l'aide de snifSnouf (prefix dependant)",\
        "!2" : "1",\
        "!3" : "1",\
        "!4" : "1",\
        "!5" : "1",\
        "!6" : "1",\
        "!7" : "1",\
        }

    COMMAND_LIST = dict(sorted(COMMAND_LIST.items()))
    #page c'est une liste d'embed
    pages = []
    cReturn = 0  
    thisMBD = None
    for command, desc in COMMAND_LIST.items():
        if cReturn%5 == 0:
            if thisMBD:pages.append(thisMBD)
            cReturn = 0
            thisMBD=discord.Embed(title="Help menu", url="https://github.com/caimez323/BOT_TDM", description="List of all the commands", color=0xa24a01)
            thisMBD.set_footer(text=message.author.name, icon_url=message.author.avatar)
        thisMBD.add_field(name="",value="**"+command+"** : "+desc,inline=False)
        cReturn += 1
    if cReturn%5 != 0:
        pages.append(thisMBD)
    return pages


async def help(message):

    pages = helpPagesCreation(message)
    await message.channel.send(embed=pages[0],view = HelperView(pages))
