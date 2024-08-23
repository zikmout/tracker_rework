FROM python:3.8-alpine

# Install necessary build dependencies
RUN apk add --update --no-cache \
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
    firefox-esr \
    musl-dev \
    python3-dev \
    gcc

WORKDIR /app



RUN which python3 && python3 --version

# Create the virtual environment
RUN python3 -m venv ENV

COPY . /app

# Set the virtual environment path
ENV PATH="/app/ENV/bin:$PATH"

# RUN pip install --upgrade pip==19.0.1
RUN pip install --upgrade pip

RUN pip install versioneer

RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

RUN python setup.py install
RUN python setup.py build

EXPOSE 6000

CMD ["tracker_app", "no_model"]
