import os
from sqlalchemy import engine_from_config
#from pintell import SQLALCHEMY_URL
from pintell.base import Base, url
from pintell.models import Role

def main():
    settings = {'sqlalchemy.url': url}
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #Role.insert_roles()
    print('[X] DB successfully deleted.')