import json
import datetime
import time
import tornado
from tornado import gen
import pickle
import traceback
from tornado.web import RequestHandler
from werkzeug import check_password_hash
from tracker.models import Permission, Role, Project, User
from tracker.utils import make_session_factory, flash_message, login_required, admin_required
from tracker.models import User
import tracker.session as session
from tracker.workers.live.live_view_worker import live_view

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
        if hasattr(self.session, 'tasks') and hasattr(self.session['tasks'], 'live_view') and self.session['tasks']['live_view'][0]['id']:
            task_id_to_stop = self.session['tasks']['live_view'][0]['id']
            live_view.AsyncResult(task_id_to_stop).revoke(terminate=True)
            del self.session['tasks']['live_view'][:]
            self.session.save()
            flash_message(self, 'info', 'Live view task on url {} stopped because you quited the page.'.format(task_id_to_stop))
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
        self.args = {k:self.get_argument(k) for k in self.request.arguments}

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

    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            tb = list()
            # self.write('Exception :\n{}'.format(kwargs['exc_info'][0].__name__))
            for line in traceback.format_exception(*kwargs["exc_info"]):
                tb.append(line)
            self.render('pages/500.html', traceback=tb)
        else:
            self.write('ERROR : (Status Code {})'.format(status_code))

class HomePage(BaseView):
    SUPPORTED_METHODS = ['GET']
    def get(self):
        self.render('index.html')

class SwitchMode(BaseView):
    SUPPORTED_METHODS = ['POST']
    # @admin_required
    @gen.coroutine
    def post(self):
        # is_simplified = self.get_argument('is_simplified')
        # user = self.app_db.query(User).filter_by(username=self.session['username']).first()
        # print('Switch to : {}'.format(is_simplified))
        # del self.session['is_simplified']
        self.session['is_simplified'] = not self.session['is_simplified']
        self.session.save()
        flash_message(self, 'info', 'Simplified interface : {}.'.format(self.session['is_simplified']))
        self.send_response({ 'response': 'OK' })

class My404Handler(BaseView):
    def prepare(self):
        self.set_status(404)
        self.render('pages/404.html')