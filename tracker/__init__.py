import os
import base64
import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
import tornado.web
from tornado.web import url
from tracker.utils import make_session_factory
import tracker.session as session

from tracker.views.base import HomePage
from tracker.views.user import UserListView, UserDelete, UserUnitView, UserUnitEditView
from tracker.views.auth import AuthLoginView, AuthRegisterView, AuthLogoutView
from tracker.views.mail import UserProjectSendMail
from tracker.views.tasks import RevokeLiveTasks, DeleteTaskQueues
from tracker.views.content import UserProjectContent, TestingView, UserProjectContentFromFile
from tracker.views.project import ProjectsCreateView, UserProjectListView, UserProjectView,\
 UserProjectDelete, FastProjectCreateView
from tracker.views.continuous_tracking import ContinuousTrackingCreateView, UserProjectWebsitesView,\
 UserProjectAddWebsite, UserProjectDeleteWebsite, UserProjectEditWebsite
from tracker.views.alert import AlertView, AlertCreate, AlertLiveView, AlertLiveCreate, AlertLiveUpdate
from tracker.views.download import UserDownloadCreate, UserDownloadStop, UserDownloadStatus,\
 UserProjectDownloadView
from tracker.views.crawl import UserProjectCrawlView, UserCrawlsCreate, UserCrawlStop,\
 UserCrawlDeleteLogfile, DeleteCrawlTaskFromSession
from tracker.views.socket import EchoWebSocket

define('port', default=5567, help='Port to listen on.')

app_db, meta = make_session_factory()

def main():
    dirname = os.getcwd()
    
    """Construct and serve the tornado application."""
    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
            # tracker.views.base.py
            url(r'/', HomePage, name='home'),

            # tracker.views.user.py
            url(r'/api/v1/users_list', UserListView, name='users_list'),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?', UserDelete, name='user_delete'),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/unit/?(?P<uid>[0-9]+)?', UserUnitView, name='user_unit_view'),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/unit-edit', UserUnitEditView, name='unit-edit-view'),

            # tracker.views.auth.py
            url(r'/api/v1/auth/login', AuthLoginView, name='login'),
            url(r'/api/v1/auth/logout', AuthLogoutView, name='logout'),
            url(r'/api/v1/auth/register', AuthRegisterView, name='register'),

            # tracker.views.mail.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/send_report', UserProjectSendMail),

            # tracker.views.tasks.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/tasks/revoke-all', RevokeLiveTasks),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/tasks/delete-all', DeleteTaskQueues),

            # tracker.views.content.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/content', UserProjectContent),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/content-from-file', UserProjectContentFromFile),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/testview', TestingView),

            # tracker.views.crawl.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl', UserProjectCrawlView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/create_task', UserCrawlsCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/delete/?(?P<uid>[A-Za-z0-9-]+)?', UserCrawlDeleteLogfile),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/stop_task/?(?P<task_id>[A-Za-z0-9-]+)?', UserCrawlStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/end_task/?(?P<uid>[A-Za-z0-9-]+)?', DeleteCrawlTaskFromSession), 

            # tracker.views.download.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/unit/?(?P<uid>[0-9]+)?', UserDownloadCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/unit/?(?P<uid>[0-9]+)?/stop', UserDownloadStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download', UserProjectDownloadView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/?(?P<task_id>[A-Za-z0-9-]+)?', UserDownloadStatus),
            
            # tracker.views.project.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/project_create', ProjectsCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects_manage', UserProjectListView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/quick-project-create', FastProjectCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?', UserProjectView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/delete', UserProjectDelete),

            # tracker.views.continuous_tracking.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/continuous-tracking-create', ContinuousTrackingCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/websites-manage', UserProjectWebsitesView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-add', UserProjectAddWebsite),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-delete', UserProjectDeleteWebsite),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-edit', UserProjectEditWebsite),

            # tracker.views.alert.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts', AlertView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/create', AlertCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/live/view', AlertLiveView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/live/update', AlertLiveUpdate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/live/create/?(?P<alertid>[A-Za-z0-9-_]+)?', AlertLiveCreate),

            # tracker.views.socket.py
            url(r'/websocket', EchoWebSocket, name='websocket')
            ]
            # todo : activate xsrf_cookies = True
            settings = {
                'template_path': os.path.join(dirname, 'tracker/templates'),
                'static_path': os.path.join(dirname, 'tracker/static'),
                'cookie_secret': 'd5006258ba9aaa1d86a8014e767c6d8cf3d2ad69a4021901e6c47af740b15ad5',#os.urandom(32).hex(),
                'session_secret': '28bd17bdb79af5032d2dd03dd549d60e14ef83e5c7902bed0ed4497c5e0fc011',#os.urandom(32).hex(),
                'session_timeout': 60000,
                'store_options': {
                    'redis_host': 'localhost',
                    'redis_port': 6379,
                    'redis_pass': None
                },
                'debug': True,
                'autoreload': True,
                'serve_traceback':True,
                'compiled_template_cache':False
            }
            tornado.web.Application.__init__(self, handlers, **settings)
            try:
                # app_db not used yet
                self.data_dir = os.path.join(dirname, 'data')
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
    logging.warning("Server running on port %d", options.port)
    #IOLoop.instance().start()
    IOLoop.current().start()