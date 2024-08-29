FROM python:3.8-buster as base

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

WORKDIR /app

RUN python3 -m venv ENV

COPY . /app

RUN sed -i '1s|^.*$|#!/usr/bin/env python|' /app/ENV/bin/tracker_app

RUN pip install --no-cache-dir numpy
RUN pip install --upgrade pip==19.3.1
RUN pip install versioneer
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

RUN python setup.py install
RUN python setup.py build

EXPOSE 5567
CMD ["tracker_app", "no_model"]

# Worker stage for live_view_worker
# FROM base as worker

# WORKDIR /app/tracker/workers/live

# # Set up command for live_view_worker
# CMD ["celery", "-A", "live_view_worker", "worker", "--loglevel=INFO", "--hostname=w1@%h", "--concurrency=10", "-Ofair", "--autoscale=30"]