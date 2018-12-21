import json
import datetime
import time
import tornado
import pickle
from tornado.web import RequestHandler
from werkzeug import check_password_hash
from pintell.models import Permission, Role, Project, User
from pintell.utils import make_session_factory, flash_message, login_required
from pintell.models import User
import pintell.session as session
import json

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
            'list users': 'GET /api/v1/users_list',
            'login': 'POST /api/v1/auth/login',
            'logout': 'GET /api/v1/auth/logout',
            'register': 'POST /api/v1/auth/register',
            'delete user': 'POST /api/v1/users/<username>',

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
        if hasattr(self, 'request_db'):
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
        self.session['tasks'] = {}
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
            self.session['tasks'] = {}
            self.session.save()
            flash_message(self, 'success', 'User {} succesfully registered.'.format(username))
            self.redirect('/')
        except Exception as e:
            print('Exception : {}'.format(e))
            flash_message(self, 'danger', 'Username {} already exists or email {} already taken.'.format(username, email))
            self.redirect('/api/v1/auth/register')

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
    def post(self, username):
        print('User to be deleted : {}'.format(username))
        user = self.request_db.query(User).filter_by(username=username).first()
        if user:
            print('User found. Deleting it now....')
            try:
                self.request_db.delete(user)
                self.request_db.commit()
                self.redirect('/api/v1/users_list')
            except Exception as e:
                print('Exception : Impossible to delete user because : {}'.format(e))
        else:
            print('Username {} not found. Delete aborded.'.format(username))
            self.redirect('/api/v1/users_list')