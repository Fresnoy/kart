FROM python:3.11-slim

# Bonnes pratiques : éviter les .pyc et forcer l'affichage
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système utiles
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev gcc python3-dev musl-dev \
    netcat-openbsd \
    && apt-get clean


# Créer et se placer dans le dossier de l'app
WORKDIR /app

# Copier le fichier requirements avant tout pour profiter du cache Docker
COPY requirements.txt .
COPY app /app/


# Installer les paquets Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install python-dotenv


# Copier le script d'entrée
# COPY config/web/entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh

# ENTRYPOINT ["/app/entrypoint.sh"]

# DEV : Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# PROD : à activer au besoin
# CMD ["gunicorn", "kart.wsgi:application", "--bind", "0.0.0.0:8000"]

