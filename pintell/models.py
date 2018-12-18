from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from pintell.base import Base
from pintell.utils import make_session_factory
from werkzeug.security import generate_password_hash

class Results(Base):
    __tablename__ = 'results'
    __table_args__ = {'extend_existing': True}
    updated_time = Column(DateTime, primary_key=True)
    query_time = Column(Integer)
    current_price = Column(Float)

    def __init__(self, updated_time, query_time, current_price):
        print('constructor of results....')
        self.updated_time = updated_time
        self.query_time = query_time
        self.current_price = current_price

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    default = Column(Boolean, default=False, index=True)
    permissions = Column(Integer)
    users = relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
            }
        default_role = 'User'
        session, meta = make_session_factory()
        for r in roles:
            role = session.query(Role).filter_by(name=r).first()#Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            session.add(role)
        session.commit()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column('user_id', Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(500))
    email = Column('email', String(50), unique=True, index=True)
    registration_date = Column('registration_date', DateTime)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __init__(self, username, password, email, session, meta):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.registration_date = datetime.now()
        #session, meta = make_session_factory()
        if self.role is None:
            print('self.role is none')
            #print('current_app.config[\'FLASK_ADMIN\'] = {}'.format(current_app.config['FLASK_ADMIN']))
            print('self.email = {}'.format(self.email))
            if self.email == 'toto@gmail.com':#current_app.config['FLASK_ADMIN']:
                self.role = session.query(Role).filter_by(name='Administrator').first()
                print('<OK Admin registration detected>')
                print('self.role 1 = {}'.format(self.role))
            if self.role is None:
                self.role = session.query(Role).filter_by(default=True).first()
                print('self.role 2 = {}'.format(self.role))

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<user {}>'.format(self.username)

class AnonymousUser(Base):
    __tablename__ = 'users_anonymous'
    id = Column(Integer, primary_key=True)
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False