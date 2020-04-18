import os
import sys
import base64
import logging
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
import tornado.web
from tornado.web import url
from tracker.utils import make_session_factory
import tracker.session as session

from tracker.views.base import HomePage, My404Handler, SwitchMode, SwitchDetailedLiveView, SwitchPosLiveView,\
SwitchNegLiveView, SwitchTimeoutLiveView, BlankPage
from tracker.views.user import UserListView, UserDelete, UserUnitView, UserUnitEditView, AdminUserCreate
from tracker.views.auth import AuthLoginView, AuthRegisterView, AuthLogoutView, AuthUpdatedPasswordView
from tracker.views.mail import UserProjectSendMail
from tracker.views.tasks import RevokeLiveTasks, DeleteTaskQueues
from tracker.views.content import UserProjectContent, UserProjectContentFromFile, UserProjectDeleteContent,\
UserProjectSpider
from tracker.views.project import ProjectsCreateView, UserProjectListView, UserProjectView,\
 UserProjectDelete, FastProjectCreateView, DownloadFile, EmailToWatchlist
from tracker.views.continuous_tracking import ContinuousTrackingCreateView, UserProjectWebsitesView,\
 UserProjectAddWebsite, UserProjectDeleteWebsite, UserProjectEditWebsite
from tracker.views.alert import AlertView, AlertCreate, AlertLiveView, AlertLaunch, AlertDelete,\
AlertLiveUpdate, AlertStop, AlertLiveUpdateJSON
from tracker.views.download import UserDownloadCreate, UserDownloadStop, UserDownloadStatus,\
 UserProjectDownloadView
from tracker.views.crawl import UserProjectCrawlView, UserCrawlsCreate, UserCrawlStop,\
 UserCrawlDeleteLogfile, DeleteCrawlTaskFromSession
from tracker.views.socket import EchoWebSocket

def main():
    LOAD_MODEL = False
    if 'no_model' not in sys.argv:
        LOAD_MODEL = True
        from tracker.views.predict import SBBPredict
    define('port', default=5567, help='Port to listen on.')
    app_db, meta = make_session_factory()
    dirname = os.getcwd()
    
    # TODO : Check if data dir exist, if not create it and insert_Roles()
    project_path = os.path.join(dirname, 'data')
    if not os.path.isdir(project_path):
        from tracker.models import Role
        os.mkdir(project_path)
        Role.insert_roles()
    
    """Construct and serve the tornado application."""
    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
            # tracker.views.base.py
            url(r'/', HomePage, name='home'),
            url(r'/blank', BlankPage, name='blank'),
            url(r'/switch-mode', SwitchMode),
            url(r'/switch-detailded-live-view', SwitchDetailedLiveView),
            url(r'/switch-pos-live-view', SwitchPosLiveView),
            url(r'/switch-neg-live-view', SwitchNegLiveView),
            url(r'/switch-timeout-live-view', SwitchTimeoutLiveView),
            url(r'/api/v1/update-content', AlertLiveUpdateJSON),

            # tracker.views.user.py
            url(r'/api/v1/users_list', UserListView, name='users_list'),
            url(r'/api/v1/user-create', AdminUserCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?', UserDelete, name='user_delete'),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/unit/?(?P<uid>[0-9]+)?', UserUnitView, name='user_unit_view'),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/unit-edit', UserUnitEditView, name='unit-edit-view'),

            # tracker.views.auth.py
            url(r'/api/v1/auth/login', AuthLoginView, name='login'),
            url(r'/api/v1/auth/logout', AuthLogoutView, name='logout'),
            url(r'/api/v1/auth/register', AuthRegisterView, name='register'),
            url(r'/api/v1/auth/update-password', AuthUpdatedPasswordView, name='update_password'),

            # tracker.views.mail.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/send_report', UserProjectSendMail),

            # tracker.views.tasks.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/tasks/revoke-all', RevokeLiveTasks),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/tasks/delete-all', DeleteTaskQueues),

            # tracker.views.content.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/content', UserProjectContent),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/spider', UserProjectSpider),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/content-delete', UserProjectDeleteContent),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/content-from-file', UserProjectContentFromFile),

            # tracker.views.crawl.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl', UserProjectCrawlView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/create_task', UserCrawlsCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/delete/?(?P<uid>[A-Za-z0-9-]+)?', UserCrawlDeleteLogfile),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/stop_task/?(?P<task_id>[A-Za-z0-9-]+)?', UserCrawlStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/crawl/end_task/?(?P<uid>[A-Za-z0-9-]+)?', DeleteCrawlTaskFromSession), 

            # tracker.views.download.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/unit/?(?P<uid>[0-9]+)?', UserDownloadCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/unit/?(?P<uid>[0-9]+)?/stop', UserDownloadStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download', UserProjectDownloadView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/download/?(?P<task_id>[A-Za-z0-9-]+)?', UserDownloadStatus),
            
            # tracker.views.project.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/project_create', ProjectsCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects-manage', UserProjectListView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/quick-project-create', FastProjectCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/export-watchlist', DownloadFile),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/email-to-watchlist', EmailToWatchlist),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?', UserProjectView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/delete', UserProjectDelete),

            # tracker.views.continuous_tracking.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/continuous-tracking-create', ContinuousTrackingCreateView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/websites-manage', UserProjectWebsitesView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-add', UserProjectAddWebsite),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-delete', UserProjectDeleteWebsite),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/website-edit', UserProjectEditWebsite),

            # tracker.views.alert.py
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts', AlertView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/create', AlertCreate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alert/stop', AlertStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/delete', AlertDelete),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/stop', AlertStop),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/live/view', AlertLiveView),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/live/update', AlertLiveUpdate),
            url(r'/api/v1/users/?(?P<username>[A-Za-z0-9-_]+)?/projects/?(?P<projectname>[A-Za-z0-9-_]+)?/alerts/launch/?(?P<alertid>[A-Za-z0-9-_]+)?', AlertLaunch),

            # tracker.views.socket.py
            url(r'/websocket', EchoWebSocket, name='websocket')
            ]
            if LOAD_MODEL:
                handlers.append(url(r'/api/v1/predict/is_sbb', SBBPredict))
            # todo : activate xsrf_cookies = True
            settings = {
                'template_path': os.path.join(dirname, 'tracker/templates'),
                'static_path': os.path.join(dirname, 'tracker/static'),
                'cookie_secret': '22cb77ce055301d377346c6deb8c2db097bd191577c6fd811e18faff4f645f26',#os.urandom(32).hex(),
                'session_secret': 'c230848c20f2eb8119080c92677aacf1695df092251ed2c712d3c9110480c4ee',#os.urandom(32).hex(),
                'session_timeout': 60000,
                'store_options': {
                    'redis_host': 'localhost',
                    'redis_port': 6379,
                    'redis_pass': None
                },
                'xheaders': True,
                'debug': True,
                'autoreload': True,
                'serve_traceback': True,
                'compiled_template_cache': False,
                'default_handler_class': My404Handler
            }
            tornado.web.Application.__init__(self, handlers, **settings)
            try:
                # app_db not used yet
                self.data_dir = project_path 
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
