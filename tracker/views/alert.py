import tornado
import json
import datetime
import time
from tornado import gen

from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required, get_url_from_id, \
json_response, make_session_factory, get_celery_task_state, revoke_all_tasks
from tornado.websocket import WebSocketHandler
from tracker.core.rproject import RProject
from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view
import tracker.workers.continuous_worker as continuous_worker
# from tracker.celery import continuous_tracking_worker_app
# from tracker.workers.continuous_worker import setup_periodic_tasks

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
            if args['inputStartTime'] == '':
                start_time = datetime.datetime.now().replace(microsecond=0)
            else:
                start_time = args['start_time']
            if args['inputType'] == 'Live':
                start_time = datetime.datetime.now().replace(microsecond=0)
                new_alert = Alert(args['inputName'], args['inputType'], start_time, email_notify=checked)
            elif args['inputType'] == 'BasicReccurent':
                new_alert = Alert(args['inputName'], args['inputType'], start_time, repeat=args['inputRepeat'],\
                    interval=args['inputEvery'], max_count=args['inputMaxCount'], email_notify=checked)
            elif args['inputType'] == 'CrontabSchedule':
                new_alert = Alert(args['inputName'], args['inputType'], start_time, repeat_at=args['inputRepeatTime'],\
                    days_of_week=[v[0] for k, v in args.items() if k.startswith('crontabDay')], email_notify=checked)
                
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

        if args['alertType'] == 'Live':
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
                flash_message(self, 'danger', 'Problem creating LIVE ALERT.')
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
                
                # Put status 'launched' on alert
                alert = content.alerts.filter_by(name=args['alertName']).first()
                alert.launched = True
                self.request_db.commit()

                self.session['tasks']['live_view'] = updated_tasks
                self.session.save()
                self.redirect('/api/v1/users/{}/projects/{}/alerts/live/view'.format(username, projectname))
        else:
            self.write('Continuous Tracking Alert launching ...')
            import cluster
            #from tracker.celery import continuous_tracking_worker_app
            from redbeat import RedBeatSchedulerEntry as Entry
            # e = Entry('thingo', 'cluster.add_task', 10, args=[15, 4], app=cluster.app)
            e = Entry('thingo1', 'continuous_tracking_worker.add_task', 5, args=[15, 4], app=continuous_worker.app)
            e.save()
            print('E = {}'.format(e))
            #key = e.key()
            # setup_periodic_tasks(continuous_tracking_worker_app)
            self.write('periodic tasks ok')

class AlertStop(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('ARGS = {}'.format(args))

        user = self.request_db.query(User).filter_by(username=username).first()
        print('USER = {}'.format(user.username))
        project = user.projects.filter_by(name=projectname).first()
        content = project.contents.filter_by(name=args['contentName']).first()
        alert = content.alerts.filter_by(name=args['alertName']).first()

        if 'live_view' in self.session['tasks']:
            res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
            print('Deleting old live view tasks from session.')
            del self.session['tasks']['live_view']
            self.session.save()

        alert.launched = False
        self.request_db.commit()
        flash_message(self, 'success', 'Alert {} succesfully stopped.'.format(args['alertName']))
        self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))


class AlertDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self, username, projectname):
        #print('ARGS = {}'.format(self.form_data))
        content_name = self.get_argument('contentName')
        alert_name = self.get_argument('alertName')
        user = self.request_db.query(User).filter_by(username=username).first()
        print('USER = {}'.format(user.username))
        project = user.projects.filter_by(name=projectname).first()
        content = project.contents.filter_by(name=content_name).first()
        alert = content.alerts.filter_by(name=alert_name).first()
        if alert:
            try:
                self.request_db.delete(alert)
                self.request_db.commit()
                flash_message(self, 'success', 'Alert {} succesfully deleted.'.format(alert_name))
            except Exception as e:
                flash_message(self, 'success', 'Impossible to delete alert. Check shell logs for more information.')
                print('Exception : Impossible to delete user because : {}'.format(e))
        else:
            flash_message(self, 'danger', 'Alert {} not found. Delete aborded.'.format(alert_name))
        self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))

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