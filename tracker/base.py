import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis


def connect_psycopg2():
    try:
        # Ensure critical environment variables are set
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        db = os.getenv('POSTGRES_DB')
        host = os.getenv('POSTGRES_HOST')
        port = os.getenv('POSTGRES_PORT')

        if not all([user, password, db, host, port]):
            raise ValueError(
                "Missing one or more required environment variables for PostgreSQL connection")

        # Construct the database URL
        url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
        engine = create_engine(url, client_encoding='utf8')
        meta = sqlalchemy.MetaData(bind=engine)
        meta.reflect(bind=engine)
        return url, engine, meta
    except Exception as e:
        print(f'[STOP] Exception during DB connection: {e}')
        return None, None, None


def connect_redis():
    try:
        # Ensure environment variables are set for Redis
        host = os.getenv('REDIS_HOST')
        port = os.getenv('REDIS_PORT')

        if not all([host, port]):
            raise ValueError(
                "Missing one or more required environment variables for Redis connection")

        r = redis.Redis(host=host, port=int(port))
        r.ping()
        print("[x] Redis connected successfully")
        return r
    except redis.ConnectionError as e:
        print(f'[STOP] Redis Connection Error: {e}')
        return None


print('\n[x] DB initialisation : Running SQL Alchemy version {}'.format(sqlalchemy.__version__))
url, engine, meta = connect_psycopg2()

if engine is not None:
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
else:
    print("[ERROR] Failed to connect to the database.")

redis_client = connect_redis()

if redis_client is None:
    print("[ERROR] Failed to connect to Redis.")
