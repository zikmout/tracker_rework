FROM python:3.8-buster

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
    libpq-dev \
    git \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    libjpeg-dev \
    redis-server \
    rabbitmq-server \
    nginx \
    xvfb \
    firefox-esr \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m venv ENV

COPY . /app

ENV PATH="/app/ENV/bin:$PATH"

RUN pip install --no-cache-dir numpy

RUN pip install --upgrade pip==19.3.1

RUN pip install versioneer

RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

RUN python setup.py install

RUN python setup.py build

EXPOSE 6000

CMD ["tracker_app", "no_model"]
