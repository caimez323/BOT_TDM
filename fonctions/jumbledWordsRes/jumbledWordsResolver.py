import discord
from discord.ext import commands
import requests
import pytesseract
from io import BytesIO
from PIL import Image
import pyautogui
import io
import numpy as np
import cv2
import re

# Chemin vers le binaire Tesseract-OCR (à adapter selon l'installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\leotr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def load_words(file_path):
    """Charge la liste de mots depuis un fichier et convertit tous les mots en majuscules."""
    with open(file_path, 'r') as file:
        return set(word.strip().upper() for word in file)

def search_word_in_grid(grid, word):
    """Cherche un mot dans la grille dans toutes les directions possibles."""
    def search_from(x, y, dx, dy, word):
        length = len(word)
        for i in range(length):
            nx, ny = x + i * dx, y + i * dy
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])) or grid[nx][ny] != word[i]:
                return False
        return True

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                if search_from(x, y, dx, dy, word):
                    return True
    return False

def solve_word_search(grid, words):
    """Trouve tous les mots dans la grille."""
    found_words = []
    for word in words:
        if search_word_in_grid(grid, word):
            found_words.append(word)
    return found_words

async def resolver(message, content):
    # Séparer les lignes
    lines = content.split('\n')
    
    # Nettoyer et vérifier que chaque ligne a la même longueur
    lines = [line.strip().upper() for line in lines if line.strip()]
    if not lines:
        await message.channel.send("Le message doit contenir une grille.")
        return

    max_length = max(len(line) for line in lines)
    grid = [list(line.ljust(max_length, ' ')) for line in lines]

    # Afficher la grille pour le débogage
    print("Grille construite:")
    for row in grid:
        print("".join(row))

    # Trouver les mots prédéfinis dans la grille
    predefined_words = load_words('fonctions/jumbledWordsRes/words.txt')
    found_words = solve_word_search(grid, predefined_words)
    
    # Envoyer les résultats
    if found_words:
        await message.channel.send(f"**Jeux trouvés :** {', '.join(found_words)}")
    else:
        await message.channel.send("Aucun mot trouvé.")

def cleanMsg(extracted_text):
    # Séparer les lignes du texte extrait
    lines = extracted_text.splitlines()
    cleaned_text = []
    for line in lines:
        # Supprimer les espaces
        cleaned_line = re.sub(r'\s', '', line)
        # Supprimer les chiffres
        cleaned_line = re.sub(r'\d', '', cleaned_line)
        # Supprimer les barres inverses '\'
        cleaned_line = re.sub(r'\\', '', cleaned_line)
        # Supprimer les barres obliques '/'
        cleaned_line = re.sub(r'/', '', cleaned_line)
        # Supprimer les parenthèses '(' et ')'
        cleaned_line = re.sub(r'[()]', '', cleaned_line)
        # Supprimer les crochets '[' et ']'
        cleaned_line = re.sub(r'[\[\]]', '', cleaned_line)
        # Supprimer les barres verticales '|'
        cleaned_line = re.sub(r'\|', '', cleaned_line)
        # Supprimer les apostrophes
        cleaned_line = re.sub(r"'", '', cleaned_line)
        # Supprimer les "O" directement devant les "D"
        cleaned_line = re.sub(r'O(?=D)', '', cleaned_line)
        # Supprimer les "2" directement devant les "Z"
        cleaned_line = re.sub(r'2(?=Z)', '', cleaned_line)
        # Ajouter la ligne nettoyée à la liste
        cleaned_text.append(cleaned_line)
    # Joindre les lignes nettoyées
    final_text = "\n".join(cleaned_text)
    return final_text

async def jumbledWordsResolver(message):
    if (message.content.lower().startswith("!jb") and message.attachments) or (message.attachments and message.channel.id == 1271525568625639566):
        for attachment in message.attachments:
            image_url = attachment.url
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))


            # Convertir l'image PIL en format numpy pour utiliser OpenCV
            img_cv = np.array(img)

            # Convertir en niveaux de gris
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

            # (Optionnel) Sauvegarder l'image pour voir le résultat
            cv2.imwrite('gray_image.png', gray)

            # Convertir l'image traitée de retour au format PIL
            img_preprocessed = Image.fromarray(gray)

            # Configuration de Tesseract
            custom_config = r'--oem 3 --psm 6'

            # Utiliser pytesseract pour extraire le texte de l'image prétraitée
            extracted_text = pytesseract.image_to_string(img_preprocessed, config=custom_config)

            # Supprimer les espaces et les caractères indésirables
            extracted_text = cleanMsg(extracted_text)

            # Afficher le texte extrait pour le débogage
            print("Texte extrait:", extracted_text)

            # Envoyer le texte extrait au resolver
            await resolver(message, extracted_text)

    if message.channel.id == 1271525568625639566 and not message.attachments:
        await resolver(message, message.content)

    if message.content.startswith("!g"):
        content = message.content[2:].strip()
        print("Message reçu pour !g:", content)
        await resolver(message, content)
