import discord
from discord.ui import View


class HelperView(View):
    def __init__(self,pages):
        super().__init__()
        self.current_page = 0
        self.pages = pages
    
    @discord.ui.button(label="", style=discord.ButtonStyle.gray,emoji="<:240_Amoa:1017107527961424014>")
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await self.update_message(interaction)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.gray,emoji="<:238_Maraiste:1133163882999971991>")
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

    COMMAND_ARAM = {\
        "!aram_teamrdm *p1 p2...*": "créé un matchmaking d'ARAM (équipes aléatoires)",\
        "!aram_rdm *p1 p2...*": "créé un matchmaking d'ARAM (équipes dans l'ordre)",\
        "!reroll *player*": "choisit 2 nouveaux picks aléatoirement",\
        "!pick_rdm": "choisit 1 pick aléatoire",\
    }

    COMMAND_FIGHT = {\
        "!duel @adversaire": "choisit 1 adversaire pour faire un duel",\
        "!bolosse ": "choisit 1 bolosse parmi les joueurs du vocal",\
        "!fight *p1 p2*": "combat entre 2 personnes",\
    }
    
    COMMAND_COMPOS = {\
        "!challenges": "affiche la liste des challenges lol",\
        "!chall *nom/n° challenge*": "affiche les conditions du challenge",\
        "!region *champion*": "donne la région à laquelle appartient le champion",\
    }

    COMMAND_MUSIQUE = {\
        "!play *lien/titre*": "jouer la musique",\
        "!skip": "passer la musique",\
        "!join": "rejoindre le channel vocal",\
        "!leave": "quitter le channel vocal",\
        "!queue": "afficher la queue",\
        "!shuffle": "mélanger la queue",\
        "!np": "afficher la musique en cours",\
        "!pause": "mettre la musique en pause",\
        "!resume": "reprendre la musique mise en pause",\
        "!remove *n°*": "supprimer une musique de la queue",\
        "!goto *timer*": "se déplacer à un moment de la musique",\
        "!volume *value*": "modifier le volume du bot entre 0 et 2 (0.25 par défaut)",\
    }

    COMMAND_CALCULS = {\
        "!piece": "lance la pièce pour faire un pile ou face",\
        "!number_rdm *(min) max*": "affiche un nombre aléatoire en fonction des bornes",\
        "!justeprix *(max)*": "démarre le jeu du juste prix",\
    }

    COMMAND_RECHERCHE = {\
        "!w2g": "affiche le lien du Watch2Gether",\
        "!pp *nom/id/mention*": "affiche la photo de profil d'un membre",\
        "!ytb *titre/lien de la vidéo*": "affiche les 5 premières vidéos Youtube de la recherche",\
        "!clash": "en développement",\
    }
    
    COMMAND_SNIFSNOUF = {\
        "!addList": "ajoute un créateur à la liste",\
        "!website": "affiche le site web",\
        "!listMacro ": "génère une macro téléchargeable pour tout ouvrir d'un coup",\
        "!iwu": "vérifie si la database est syncro avec le SnifSnouf",\
        "!dataSync ": "syncronisation de la database avec le SnifSnouf",\
    }

    COMMAND_CUSTOMWORDS = [
        "hello",
        "ping",
        "kebab",
        "croco",
        "wéwéwé",
        "cochon"
    ]
        
    COMMAND_LIST = {\
        "BLOC_ARAM": COMMAND_ARAM,\
        "BLOC_FIGHT": COMMAND_FIGHT,\
        "BLOC_COMPOS": COMMAND_COMPOS,\
        "BLOC_MUSIQUE (en développement)": COMMAND_MUSIQUE,\
        "BLOC_CALCULS": COMMAND_CALCULS,\
        "BLOC_RECHERCHE": COMMAND_RECHERCHE,\
        "BLOC_SNIFSNOUF": COMMAND_SNIFSNOUF,\
        "CUSTOM WORDS": COMMAND_CUSTOMWORDS,\
    }
    
    COMMAND_LIST = dict(sorted(COMMAND_LIST.items()))
    #page c'est une liste d'embed
    pages = []
    cReturn = 0  
    thisMBD = None
    for command, desc in COMMAND_LIST.items():
        if cReturn==0 or cReturn>=10:
            cReturn = 0
            thisMBD=discord.Embed(title="", url="", description="", color=0x6d97cd)
            thisMBD.set_author(name='⚙️ Command List', icon_url=(""))
            thisMBD.set_footer(text=f"{message.author.name} - page {len(pages) +1}/total", icon_url=message.author.avatar)
        if command.startswith("BLOC_"):
            block_name = command.split("_", 1)[1]
            block_dict = desc
            block_fulldesc = ""
            for block_command, block_desc in block_dict.items():
                block_fulldesc += f"**{block_command}** : {block_desc}\n"
                cReturn += 1
            thisMBD.add_field(name=f"**\n{block_name}**", value=block_fulldesc, inline=False)
        elif command == "CUSTOM WORDS":
            custom_words_str = ", ".join(desc)
            thisMBD.add_field(name=f"**\n{command}**", value=custom_words_str, inline=False)        
            cReturn += 1
        else:
            thisMBD.add_field(name="", value=f"**{command}** : {desc}", inline=False)
        cReturn += 1
        if cReturn>=10:
            thisMBD.add_field(name=f"", value="\u200b", inline=False)        
            pages.append(thisMBD)
    thisMBD.add_field(name=f"", value="\u200b", inline=False)        
    pages.append(thisMBD)
    for i, page in enumerate(pages):
        page.set_footer(text=f"{message.author.name} - Page {i + 1}/{len(pages)}", icon_url=message.author.avatar)
    return pages


async def help(message):

    pages = helpPagesCreation(message)
    await message.channel.send(embed=pages[0],view = HelperView(pages))
