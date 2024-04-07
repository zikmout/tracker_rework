# Choisir une image de base
FROM python:3.8-alpine

# Mettre à jour et installer les dépendances nécessaires
RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    git \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    jpeg-dev \
    redis \
    rabbitmq-server \
    nginx \
    xvfb \
    firefox-esr

# Cloner le projet depuis GitHub
WORKDIR /app
RUN git clone git@github.com:zikmout/tracker_rework.git tracker


COPY tracker_rework /app

# Créer et activer l'environnement virtuel
RUN python -m venv ENV
ENV PATH="/app/ENV/bin:$PATH"

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Installer et construire l'application
RUN python setup.py install
RUN python setup.py build


# Installer Python et les dépendances de Tracker
# WORKDIR /app/tracker
# RUN python3 -m venv ENV && \
#     source ENV/bin/activate && \
#     pip install -r requirements.txt && \
#     python setup.py install

# Copier les fichiers de configuration Nginx
# COPY ./tracker/config/ssl/nginx.conf /etc/nginx/nginx.conf
# COPY ./tracker/config/ssl/default /etc/nginx/sites-available/default

# Exposer le port nécessaire
EXPOSE 80 443

# Commande pour exécuter l'application
# CMD ["sh", "-c", "service nginx start && service redis-server start && service rabbitmq-server start && source ENV/bin/activate && tracker_app no_model"]
CMD ["tracker_app", "no_model"]
