FROM python:3.12-slim

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:jonathonf/ffmpeg-4 \
    && apt-get update && \
    apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Créer un répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande d'entrée
CMD ["python", "main.py"]
