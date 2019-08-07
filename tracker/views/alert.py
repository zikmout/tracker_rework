import tornado
import json
import datetime
import time
from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required, get_url_from_id, \
json_response, make_session_factory, get_celery_task_state, revoke_all_tasks
from tornado.websocket import WebSocketHandler
from tracker.core.rproject import RProject
from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view

class AlertView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        # get contents for 'content lookup' button
        contents = project.contents.all()
        json_contents = []
        if contents:
            [json_contents.append(content.as_dict()) for content in contents]
        #print('JSON CONTENTS -1 ==== {}'.format(json_contents[:-1]))
        # get recorded alerts for alert list
        all_alerts = []
        for content in contents:
            alerts = content.alerts.all()
            for alert in alerts:
                json_alert = alert.as_dict()
                json_alert['content_id'] = content.name
                all_alerts.append(json_alert)
        print('*********************\n{}'.format(all_alerts))
        self.render('projects/alerts/index.html', contents=json_contents, alerts=all_alerts)

class AlertCreate(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('post args = {}'.format(args))
        # if box is checked, variable comes in like { "gridCheck": "on" }
        checked = False

        if 'gridCheck' in args:
            checked = True
        content_name = args['inputContent'].split('(')[0]
        print('content -> {}'.format(content_name))
        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            content = project.contents.filter_by(name=content_name).first()
            new_alert = Alert(args['inputName'], args['inputType'], args['inputStartTime'],\
                repeat=args['inputRepeat'], notify=checked)
            content.alerts.append(new_alert)
            self.request_db.add(content)
            self.request_db.commit()
            # need to put the code for crontab here now !! 
            flash_message(self, 'success', 'Alert {} successfully created.'.format(args['inputName']))
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
        except Exception as e:
            print('Error recording alert in DB : {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(args['inputName']))
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))

class AlertLiveCreate(BaseView):
    SUPPORTED_METHODS = ['POST']

    @login_required
    def post(self, username, projectname, alertid):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('args AlertLiveCreate => {}'.format(args))
        save_log_checked = False
        if 'saveLogChecked' + alertid in args:
            save_log_checked = True

        if args['alert_type'] == 'Live':
            # if session live view task present in session, delete them and revoke associated tasks
            if 'live_view' in self.session['tasks']:
                res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
                print('Deleting old live view tasks from session.')
                del self.session['tasks']['live_view']

            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            content = project.contents.filter_by(name=args['contentName']).first()
            print('content --> {}'.format(content))
            # Loading project
            rproject = RProject(project.name, project.data_path, project.config_file)
            if len(self.session['project_config_file']) == 0:
                rproject._load_units_from_data_path()
            else:
                rproject._load_units_from_excel()
            # need to change following line with PickleType
            tasks = rproject.download_units_diff(content.links, save=True)

            if tasks == None:
                flash_message(self, 'danger', 'Problem creating LIVE ARLERT.')
                self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
            else:
                updated_tasks = list()
                for task in tasks:
                    task_object = {
                        'username': username,
                        'projectname': projectname,
                        'uid': None, # reverse function get_id_from_url
                        'url': None,#url, # to change with link list
                        'id': task.id
                    }
                    updated_tasks.append(task_object)
                self.session['tasks']['live_view'] = updated_tasks
                self.session.save()
                self.redirect('/api/v1/users/{}/projects/{}/alerts/live/view'.format(username, projectname))
        else:
            self.write('Continuous Tracking Alert launching ...')

class AlertLiveView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        if 'live_view' in self.session['tasks']:
            tasks  = self.session['tasks']['live_view'].copy()
            self.render('projects/alerts/live-view.html', tasks=tasks)
        else:
            flash_message(self, 'warning', 'No current live view tasks')
            self.redirect('/')            

class AlertLiveUpdate(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        if 'fromPage' not in args:
            flash_message(self, 'danger', 'Impossible to know from what page to download pages from.')
            self.redirect('/')
        else:
            if args['fromPage'] == 'live_view' and 'live_view' in self.session['tasks']:
                task_results = list()
                for worker in self.session['tasks']['live_view']:
                    task = live_view.AsyncResult(worker['id'])
                    response = get_celery_task_state(task)
                    if response['state'] == 'SUCCESS' and (response['status']['diff_neg'] != [] or response['status']['diff_pos'] != []):
                        task_results.append(response['status'])
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            # Loading project
            rproject = RProject(project.name, project.data_path, project.config_file)
            if len(self.session['project_config_file']) == 0:
                rproject._load_units_from_data_path()
            else:
                rproject._load_units_from_excel()
            rproject.update_units_links([x['url'] for x in task_results])
            self.redirect('/')