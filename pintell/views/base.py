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