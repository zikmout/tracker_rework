import tornado
from pintell.base import Session, Base, engine, meta

def make_session_factory():
    # generate database schema  
    Base.metadata.create_all(engine)

    # create a new session
    session = Session()
    return session, meta

def flash_message(self, type, message):
    message = dict(type=type, message=message)
    print('set cookie, message = {}'.format(message))
    self.set_secure_cookie("flash", tornado.escape.json_encode(message))