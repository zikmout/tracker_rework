from tracker.views.base import BaseView
from werkzeug import check_password_hash
from tracker.utils import flash_message, login_required
from tracker.models import User
import tracker.session as session

from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view
from tracker.utils import revoke_all_tasks

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
        self.session['is_admin'] = registered_user.is_administrator()
        if self.session['is_admin'] == True:
            self.session['is_simplified'] = True
        self.session['rolename'] = registered_user.get_rolename()
        self.session['tasks'] = {}
        self.session.save()
        flash_message(self, 'success', 'User {} succesfully logged in.'.format(registered_user.username))
        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

class AuthRegisterView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    def get(self):
        if self.get_current_user() != None:
            flash_message(self, 'danger', 'Please log out before trying to register new user.')
            self.redirect('/')
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
            self.session['is_admin'] = user.is_administrator()
            if self.session['is_admin'] == True:
                self.session['is_simplified'] = True
            self.session['rolename'] = user.get_rolename()
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
        # if session live view task present in session, delete them and revoke associated tasks
        if 'live_view' in self.session['tasks']:
            res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
            print('Deleting old live view tasks from session.')
            del self.session['tasks']['live_view']
        self.session.delete()
        flash_message(self, 'success', 'You succesfully logged out.')
        self.redirect('/')
