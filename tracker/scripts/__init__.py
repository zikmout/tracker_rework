from sqlalchemy import engine_from_config
#from pintell import SQLALCHEMY_URL
from tracker.base import Base, url
from tracker.models import Role

def main():
    settings = {'sqlalchemy.url': 'postgresql://matt:toto@localhost:8080/testpython'}
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    if bool(os.environ.get('DEBUG', '')):
        Base.metadata.drop_all(engine)
    #Role.insert_roles()
    Base.metadata.create_all(engine)