FROM python:3.12-slim

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier pyproject.toml
COPY pyproject.toml /app/

# Copier le reste des fichiers de l'application
COPY . /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir .

# Définir la commande d'entrée
CMD ["python", "main.py"]
