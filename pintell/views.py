import json
import datetime
import time
import tornado
import pickle
from tornado.web import RequestHandler
from werkzeug import check_password_hash
from pintell.models import Permission, Role, Project, User
from pintell.utils import make_session_factory, flash_message
from pintell.models import User
import pintell.session as session
import json

def login_required(f):
    def _wrapper(self, *args, **kwargs):
        logged = self.get_current_user()
        if logged is None:
            self.redirect('/api/v1/auth/login')
        else:
            ret = f(self, *args, **kwargs)
    return _wrapper

class InfoView(RequestHandler):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self):
        """List of routes for this API."""
        routes = {
            'API infos': 'GET /api/v1',
            'list users': 'GET /api/v1/users/list',
            'login': 'POST /api/v1/auth/login',
            'logout': 'GET /api/v1/auth/logout',
            'register': 'POST /api/v1/auth/register',
            'delete user': 'POST /api/v1/users/<email>',

            'register': 'POST /api/v1/accounts',
            'single profile detail': 'GET /api/v1/accounts/<username>',
            'edit profile': 'PUT /api/v1/accounts/<username>',
            'delete profile': 'DELETE /api/v1/accounts/<username>',
            'login': 'POST /api/v1/accounts/login',
            'logout': 'GET /api/v1/accounts/logout',
            "user's tasks": 'GET /api/v1/accounts/<username>/tasks',
            "create task": 'POST /api/v1/accounts/<username>/tasks',
            "task detail": 'GET /api/v1/accounts/<username>/tasks/<id>',
            "task update": 'PUT /api/v1/accounts/<username>/tasks/<id>',
            "delete task": 'DELETE /api/v1/accounts/<username>/tasks/<id>'
        }
        self.write(json.dumps(routes))

class BaseView(RequestHandler):
    """Base view for this application."""
    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        try:
            self.session = session.Session(self.application.session_manager, self)
        except Exception as e:
            print('EXCEPTION -------> {}'.format(e))

    @property
    def app_db(self):
        return self.application.app_db

    @property
    def meta(self):
        return self.application.meta

    def get_current_user(self):
        if hasattr(self, 'session'):
            return self.session.get('username')
        else:
            return None

    def prepare(self):
        # capture flash messages cookies
        cookie = self.get_secure_cookie("flash")
        if cookie:
            cookie = tornado.escape.json_decode(cookie)
            self.flash = cookie
            self.clear_cookie("flash")
        # create session factory for each request
        db, meta = make_session_factory()
        self.request_db = db
        self.form_data = {
            key: [val.decode('utf8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def on_finish(self):
        self.request_db.close()

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        #self.set_header("Content-Type", 'application/json; charset="utf-8"')
        pass

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

class HomePage(BaseView):
    SUPPORTED_METHODS = ['GET']
    def get(self):
        self.render('index.html')

class AuthLoginView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    def get(self):
        self.render('auth/login.html')

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        registered_user = self.app_db.query(User).filter_by(email=email).first()
        if registered_user is None or not check_password_hash(registered_user.password, password):
            flash_message(self, 'danger', 'User does not exist or password is incorrect.')
            self.redirect('/api/v1/auth/login')
            return
        self.session['username'] = registered_user.username
        self.session['role_id'] = registered_user.role_id
        self.session.save()
        flash_message(self, 'success', 'User {} succesfully logged in.'.format(registered_user.username))
        self.redirect('/')

class AuthRegisterView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    def get(self):
        self.render('auth/register.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        email = self.get_argument('email')
        user = User(username, password, email, self.request_db, self.meta)
        try:
            self.request_db.add(user)
            self.request_db.commit()
            self.session['username'] = username
            self.session['role_id'] = user.role_id
            self.session.save()
            flash_message(self, 'success', 'User {} succesfully registered.'.format(username))
            self.redirect('/')
        except Exception as e:
            print('Exception : {}'.format(e))
            flash_message(self, 'danger', 'Username {} already exists or email {} already taken.'.format(username, email))
            self.redirect('/api/v1/auth/register')
        
class ProjectsCreateView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    def get(self, username):
        #print('params ======== {}'.format(selg.get_argument('username')))
        self.render('projects/create.html')

    @login_required
    def post(self, username):
        name = self.get_argument('ProjectName')
        data_path = self.get_argument('ProjectLocation')
        try:
            config_df = self.get_argument('ConfigLocation')
        except Exception as e:
            config_df = None
            print('-> No config location provided.')
        print('name = {}, data_path = {}, config_df = {}'.format(name, data_path, config_df))
        self.write('project succesfully created !')
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        new_project = Project(name, data_path, config_df)
        user.projects.append(new_project)
        self.request_db.add(user)
        self.request_db.commit()
        print(new_project)

class UserProjectListView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self):
        user = self.request_db.query(User).filter_by(username=self.session['username'])
        user_projects_json = list()
        user_projects = user[0].projects.all()
        if user_projects:
            [user_projects_json.append(project.as_dict()) for project in user_projects]
        self.render('projects/manage.html', projects=user_projects_json)

class AuthLogoutView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self):
        self.session.delete()
        flash_message(self, 'success', 'You succesfully logged out.')
        self.redirect('/')

class UserListView(BaseView):
    """View for reading and adding new roles."""
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self): #, username):
        """Get all tasks for an existing user."""
        username = self.get_current_user()
        users_json = list()
        users = self.request_db.query(User).all()
        if users:
            [users_json.append(user.as_dict()) for user in users]
        self.render('admin/list_users.html', users_json=users_json)

class UserDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self):
        email = self.get_argument('email')
        print('User to be deleted : {}'.format(email))
        if self.request_db.query(User).filter_by(email=email).delete():
            print('User found. Deleting it now....')
            try:
                self.request_db.commit()
                self.redirect('/api/v1/users/list')
            except Exception as e:
                print('EXCEPTION :::::::::: {}'.format(e))
        else:
            print('User email {} not found. Delete aborded.'.format(email))
            self.redirect('/api/v1/users/list')