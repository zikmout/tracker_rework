import os
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
import tornado.web
from tornado.web import url
from pintell.views import InfoView, HomePage, UserListView, AuthLoginView, AuthRegisterView, AuthLogoutView, UserDelete
from pintell.utils import make_session_factory
import pintell.session as session

define('port', default=5567, help='port to listen on')

app_db, meta = make_session_factory()

def main():
    dirname = os.getcwd()
    
    """Construct and serve the tornado application."""
    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
            url(r'/', HomePage, name='home'),
            url(r'/api/v1', InfoView),
            url(r'/api/v1/users/list', UserListView, name='users_list'), #?(?P<username>[A-Za-z0-9-]+)?/', RoleListView)
            url(r'/api/v1/auth/login', AuthLoginView, name='login'),
            url(r'/api/v1/auth/logout', AuthLogoutView, name='logout'),
            url(r'/api/v1/auth/register', AuthRegisterView, name='register'),
            url(r'/api/v1/users/', UserDelete, name='user_delete')
            ]
            # todo : activate xsrf_cookies = True
            settings = {
                'template_path': os.path.join(dirname, 'pintell/templates'),
                'static_path': os.path.join(dirname, 'pintell/static'),
                'cookie_secret': 'd5006258ba9aaa1d86a8014e767c6d8cf3d2ad69a4021901e6c47af740b15ad5',#os.urandom(32).hex(),
                'session_secret': '28bd17bdb79af5032d2dd03dd549d60e14ef83e5c7902bed0ed4497c5e0fc011',#os.urandom(32).hex(),
                'session_timeout': 600,
                'store_options': {
                    'redis_host': 'localhost',
                    'redis_port': 6379,
                    'redis_pass': None
                }
            }
            tornado.web.Application.__init__(self, handlers, **settings)
            try:
                # app_db not used yet
                self.app_db = app_db
                self.meta = meta
                self.session_manager = session.SessionManager(settings['session_secret'], settings['store_options'], settings['session_timeout'])
            except Exception as e:
                print(e)

    app = Application()
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:{}'.format(options.port))
    print('dirname ={}'.format(dirname))
    IOLoop.instance().start()
