import os
from sqlalchemy import engine_from_config
#from tracker import SQLALCHEMY_URL
from tracker.base import Base, url
from tracker.models import Role

def main():
    settings = {'sqlalchemy.url': url}
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    if bool(os.environ.get('DEBUG', '')):
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Role.insert_roles()
    print('[X] DB successfully initialized.')