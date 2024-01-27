import sqlalchemy
from sqlalchemy import create_engine
from tornado_sqlalchemy import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from sqlalchemy import MetaData
from sqlalchemy import create_engine

metadata_obj = MetaData()

def connect_psycopg2(user, password, db, host='localhost', port='5432'):
    try:
        url = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)



        engine = create_engine(url)

        with engine.connect() as conn:
            conn.commit()  # commit as you go
            
            SQLALCHEMY_ECHO = False
            return url, engine, metadata_obj

    except Exception as e:
        print('[STOP] Exception Invalid Credentials ? : {}'.format(e))


print('\n[x] DB initialisation : Running SQL Alchemy version {}'.format(sqlalchemy.__version__))
url, engine, meta = connect_psycopg2(user='simon', password='trackerNPH9', db='trackerdb')

#engine = create_engine('postgresql://matt:toto@localhost:8080/testpython')
Session = sessionmaker(bind=engine)

Base = declarative_base()
