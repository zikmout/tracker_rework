# Base stage
FROM python:3.8-buster AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    poppler-utils \
    libnss3-dev \
    libgpgmepp-dev \
    qtbase5-dev \
    libcairo2-dev \
    libboost-dev \
    gcc \
    git \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libjpeg-dev \
    redis-server \
    nginx \
    xvfb \
    firefox-esr \
    libxml2-dev \
    libxslt-dev \
    postgresql-client \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/facebookresearch/fastText.git /fastText \
    && cd /fastText \
    && pip install .

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.24.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

RUN wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb && \
    dpkg -i erlang-solutions_1.0_all.deb && \
    apt-get update && \
    apt -y install esl-erlang && \
    apt -y install rabbitmq-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r mygroup && useradd -r -m -g mygroup tracker

# Define environment variables
ENV APP_DIR=/app
# ENV ENV_USER=tracker



COPY . /home/tracker
RUN chown -R tracker:mygroup /home/tracker/data
RUN chown -R tracker:mygroup /home/tracker

# Ensure the /home/tracker/data directory is writable by tracker
RUN chmod -R u+w /home/tracker/data

WORKDIR /app

# RUN sed -i '1s|^.*$|#!/usr/bin/env python|' /app/ENV/bin/tracker_app

RUN python3 -m venv ENV

COPY . /app



RUN pip install --no-cache-dir numpy
RUN pip install --upgrade pip==19.3.1
RUN pip install versioneer
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

RUN python setup.py install
RUN python setup.py build

FROM base AS app

USER root

COPY tracker/config/supervisord.conf /etc/supervisor/supervisord.conf
COPY tracker/config/conf.d/*.conf /etc/supervisor/conf.d/

RUN chown -R tracker:mygroup /etc/supervisor/conf.d /etc/supervisor/supervisord.conf
RUN chown -R tracker:mygroup /app

USER tracker

EXPOSE 5567
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]