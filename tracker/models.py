from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean, Time, PickleType
from sqlalchemy.orm import relationship
from tracker.base import Base
from tracker.utils import make_session_factory
from werkzeug.security import generate_password_hash

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
            role = session.query(Role).filter_by(name=r).first()
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
    id = Column(Integer, primary_key=True)
    username = Column('username', String(20), unique=True, index=True)
    password = Column('password', String(500))
    email = Column('email', String(50), unique=True, index=True)
    registration_date = Column('registration_date', DateTime)
    role_id = Column(Integer, ForeignKey('roles.id'))
    projects = relationship('Project', cascade='save-update, delete', backref='users', lazy='dynamic')

    def __init__(self, username, password, email, session, meta, role=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.registration_date = datetime.now().replace(microsecond=0)
        self.role = role
        if self.role is None:
            print('self.role is none')
            print('self.email = {}'.format(self.email))
            if self.email == 'simon.sicard@gmail.com':
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

    def get_rolename(self):
        if self.can(Permission.ADMIN):
            return 'Administrator'
        elif self.can(Permission.MODERATE):
            return 'Moderator'
        elif self.can(Permission.WRITE):
            return 'User'
        else:
            return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
        
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<user {}>'.format(self.username)

class Project(Base):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column('name', String(64), unique=True, index=True)
    data_path = Column('data_path', String(500))
    config_file = Column('config_file', String(500))
    creation_date = Column('creation_date', DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    contents = relationship('Content', cascade='save-update, delete', backref='project', lazy='dynamic')

    def __init__(self, name, data_path, config_file):
        self.name = name
        self.data_path = data_path
        self.config_file = config_file
        self.creation_date = datetime.now().replace(microsecond=0)
    
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Content(Base):
    __tablename__ = 'content'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    links = Column(PickleType)
    mailing_list = Column(PickleType) # must include template type
    project_id = Column(Integer, ForeignKey('project.id'))
    alerts = relationship('Alert', cascade='save-update, delete', backref='content', lazy='dynamic')

    def __init__(self, name, links, mailing_list=None):
        self.name = name
        self.links = links
        self.mailing_list = mailing_list

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Alert(Base):
    __tablename__ = 'alert'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    alert_type = Column(String(64))
    creation_date = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    # for BasicReccurent alerts
    repeat = Column(String(64))
    interval = Column(Integer)
    max_count = Column(Integer)
    # for CrontabSchedule alerts
    repeat_at = Column(String(64))
    days_of_week = Column(PickleType) # Array with corresponding days of the week from 0 to 6
    # Remainder
    email_notify = Column(Boolean)
    show_links = Column(Boolean)
    show_diff_pos = Column(Boolean)
    show_diff_neg = Column(Boolean)
    template_type = Column(String(64))
    diff_links = Column(String(64)) # Not bolean to keep possibility for ml algo in label
    launched = Column(Boolean)
    content_id = Column(Integer, ForeignKey('content.id'))

    def __init__(self, name, alert_type, start_time, end_time=None, repeat=None, interval=None,\
        max_count=None, repeat_at=None, days_of_week=None, email_notify=False, show_links=False,\
        show_diff_pos=True, show_diff_neg=True, template_type='diff', diff_links=True, launched=False):
        self.name = name
        self.alert_type = alert_type
        self.creation_date = datetime.now().replace(microsecond=0)
        self.start_time = start_time
        self.end_time = end_time
        self.repeat = repeat
        self.interval = interval
        self.max_count = max_count
        self.repeat_at = repeat_at
        self.days_of_week = days_of_week
        self.email_notify = email_notify
        self.show_links = show_links
        self.show_diff_pos = show_diff_pos
        self.show_diff_neg = show_diff_neg
        self.template_type = template_type
        self.diff_links = diff_links
        self.launched = launched

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class AnonymousUser(Base):
    __tablename__ = 'users_anonymous'
    id = Column(Integer, primary_key=True)
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
