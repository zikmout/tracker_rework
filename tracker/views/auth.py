from tornado import gen
from tracker.views.base import BaseView
from werkzeug.security import check_password_hash, generate_password_hash
from tracker.utils import flash_message, login_required
from tracker.models import User
from sqlalchemy import update
import tracker.session as session

from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view
from tracker.utils import revoke_all_tasks

class AuthLoginView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @gen.coroutine
    def get(self):
        self.render('auth/login.html')

    @gen.coroutine
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
        self.session['is_live_simplified'] = False
        self.session['is_pos_live'] = True
        self.session['is_neg_live'] = True
        self.session['is_timeout_live'] = False
        if self.session['is_admin'] == True:
            self.session['is_simplified'] = True
            self.session['is_timeout_live'] = True
        self.session['rolename'] = registered_user.get_rolename()
        self.session['tasks'] = {}
        self.session.save()
        flash_message(self, 'success', 'User {} succesfully logged in.'.format(registered_user.username))
        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

class AuthUpdatedPasswordView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @gen.coroutine
    def get(self):
        self.render('auth/change-password.html')

    @gen.coroutine
    def post(self):
        old_password = self.get_argument('old_password')
        new_password_1 = self.get_argument('new_password_1')
        new_password_2 = self.get_argument('new_password_2')
        username = self.get_current_user()
        registered_user = self.request_db.query(User).filter_by(username=username).first()
        if registered_user is None or not check_password_hash(registered_user.password, old_password):
            flash_message(self, 'danger', 'Password is incorrect.')
            self.redirect('/api/v1/auth/update-password')
            return
        if new_password_1 != new_password_2:
            flash_message(self, 'danger', 'New password does not match !')
            self.redirect('/api/v1/auth/update-password')
            return
        if check_password_hash(registered_user.password, old_password) and new_password_1 == new_password_2:
            registered_user.password = generate_password_hash(new_password_1)
            self.request_db.commit()
            flash_message(self, 'success', 'Password successfully updated.')
            self.redirect('/')

class AuthRegisterView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @gen.coroutine
    def get(self):
        if self.get_current_user() != None:
            flash_message(self, 'danger', 'Please log out before trying to register new user.')
            self.redirect('/')
        self.render('auth/register.html')

    @gen.coroutine
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
            self.session['is_live_simplified'] = False
            self.session['is_pos_live'] = True
            self.session['is_neg_live'] = True
            self.session['is_timeout_live'] = False
            if self.session['is_admin'] == True:
                self.session['is_simplified'] = True
                self.session['is_timeout_live'] = True
            self.session['rolename'] = user.get_rolename()
            self.session['tasks'] = {}
            self.session.save()
            flash_message(self, 'success',
                          'User {} succesfully registered.'.format(username))
            self.redirect('/')
        except Exception as e:
            print('Exception : {}'.format(e))
            flash_message(self, 'danger', 'Username {} already exists or email {} already taken.'.format(
                username, email))
            self.redirect('/api/v1/auth/register')

class AuthLogoutView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    @gen.coroutine
    def get(self):
        # if session live view task present in session, delete them and revoke associated tasks
        if 'live_view' in self.session['tasks']:
            res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
            print('Deleting old live view tasks from session.')
            del self.session['tasks']['live_view']
        self.session.delete()
        flash_message(self, 'success', 'You successfully logged out.')
        self.redirect('/')
