from pintell.base import Session, Base, engine, meta

def make_session_factory():
	# generate database schema	
	Base.metadata.create_all(engine)

	# create a new session
	session = Session()
	return session, meta