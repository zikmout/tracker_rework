import sqlalchemy
from sqlalchemy import create_engine
#from tornado_sqlalchemy import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def connect_psycopg2(user, password, db, host='localhost', port='5432'):
    try:
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        engine = sqlalchemy.create_engine(url, client_encoding='utf8')
        # bind the connection to MetaData()
        meta = sqlalchemy.MetaData(bind=engine, reflect=True)
        SQLALCHEMY_ECHO = False
        return url, engine, meta
    except Exception as e:
        print('[STOP] Exception Invalid Credentials ? : {}'.format(e))

print('\n[x] DB initialisation : Running SQL Alchemy version {}'.format(sqlalchemy.__version__))
url, engine, meta = connect_psycopg2(user='simon', password='trackerNPH9', db='trackerdb')

#engine = create_engine('postgresql://matt:toto@localhost:8080/testpython')
Session = sessionmaker(bind=engine)

Base = declarative_base()
