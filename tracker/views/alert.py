import tornado
import json
import datetime
import time
import pytz
from tornado import gen

from redbeat.schedules import rrule
from celery.schedules import crontab
# import tracker.workers.continuous_worker as continuous_worker
import tracker.workers.continuous.continuous_worker as continuous_worker
from redbeat import RedBeatSchedulerEntry as Entry
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
    @gen.coroutine
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
                if json_alert['alert_type'] != 'Live':
                    try:
                        e = Entry.from_key('redbeat:'+alert.name, app=continuous_worker.app)
                        if json_alert['launched'] == 'True':
                            json_alert['state'] = 'Active'
                            if e.is_due()[1] is None:
                                json_alert['next_due'] = '?'
                            else:
                                json_alert['next_due'] = e.is_due()[1]
                        else:
                            json_alert['state'] = 'Problem'
                            json_alert['next_due'] = '-'
                    except Exception as e:
                        if json_alert['launched'] == 'False':
                            json_alert['state'] = 'Ready'
                            json_alert['next_due'] = '-'
                        elif json_alert['launched'] == 'True':
                            json_alert['state'] = 'Lost'
                            json_alert['next_due'] = '-'
                elif json_alert['launched'] == 'True':
                    json_alert['state'] = 'Active'
                    json_alert['next_due'] = '-'
                else:
                    json_alert['state'] = 'Ready'
                    json_alert['next_due'] = '-'
                all_alerts.append(json_alert)
        #print('*********************\n{}'.format(all_alerts))
        self.render('projects/alerts/index.html', contents=json_contents, alerts=all_alerts)

class AlertCreate(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('post args = {}'.format(args))
        # if box is checked, variable comes in like { "gridCheck": "on" }
        email_notify = False

        if 'gridCheck' in args:
            email_notify = True

        if not 'inputContent' in args:
            flash_message(self, 'danger', 'Please specify some content to base your alert on.')
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
            return
        content_name = args['inputContent'].split('(')[0]
        print('content -> {}'.format(content_name))

        print('START TIME = {}'.format(args['inputStartTime']))

        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            content = project.contents.filter_by(name=content_name).first()
            
            if email_notify and content.mailing_list is None:
                flash_message(self, 'danger', 'Cannot create alert. Content \'{}\' has no mailing list in it. \
                    Select content with mailing list please.'.format(content_name))
                self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
                return
            #print('mails_content ===> {}'.format(mails_content))
            if args['inputStartTime'] == '':
                start_time = datetime.datetime.now().replace(microsecond=0)
            else:
                start_time = args['inputStartTime']
            if args['inputType'] == 'Live':
                if email_notify:
                    email_notify = False
                    msg = ['warning', 'You selected live alert and checked the option \'send mail \'\
                    but mails are manually sent on live alert. Setting mail notify to False.']
                else:
                    msg = ['success', 'Alert {} successfully created.'.format(args['inputName'])]
                start_time = datetime.datetime.now().replace(microsecond=0)
                new_alert = Alert(args['inputName'], args['inputType'], start_time, email_notify=email_notify,\
                    template_type=args['mailTemplateType'])
            elif args['inputType'] == 'BasicReccurent':
                new_alert = Alert(args['inputName'], args['inputType'], start_time, repeat=args['inputRepeat'],\
                    interval=args['inputEvery'], max_count=args['inputMaxCount'], email_notify=email_notify,\
                    template_type=args['mailTemplateType'])
                msg = ['success', 'Alert {} successfully created.'.format(args['inputName'])]
            elif args['inputType'] == 'CrontabSchedule':
                new_alert = Alert(args['inputName'], args['inputType'], start_time, repeat_at=args['inputRepeatTime'],\
                    days_of_week=[int(v[0]) for k, v in args.items() if k.startswith('crontabDay')],\
                    email_notify=email_notify, template_type=args['mailTemplateType'])
                msg = ['success', 'Alert {} successfully created.'.format(args['inputName'])]
                
            content.alerts.append(new_alert)
            self.request_db.add(content)
            self.request_db.commit()
            # need to put the code for crontab here now !! 
            flash_message(self, msg[0], msg[1])
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
        except Exception as e:
            print('Error recording alert in DB : {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Please choose another name.'.format(args['inputName']))
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))

class AlertLaunch(BaseView):
    SUPPORTED_METHODS = ['POST']

    @login_required
    @gen.coroutine
    def post(self, username, projectname, alertid):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        #print('args AlertLaunch => {}'.format(args))
        # Checkbox in UI ready to use :)
        # save_log_checked = False
        # if 'saveLogChecked' + alertid in args:
        #     save_log_checked = True

        schedule = None
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        content = project.contents.filter_by(name=args['contentName']).first()
        alert = content.alerts.filter_by(name=args['alertName']).first()

        if args['alertType'] == 'Live':
            # if session live view task present in session, delete them and revoke associated tasks
            if 'live_view' in self.session['tasks']:
                res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
                print('Deleting old live view tasks from session.')
                del self.session['tasks']['live_view']

            print('content --> {}'.format(content))
            # Loading project
            rproject = RProject(project.name, project.data_path, project.config_file)
            if len(self.session['project_config_file']) == 0:
                rproject._load_units_from_data_path()
            else:
                rproject._load_units_from_excel()
            print('RPROJECT UNITS = {}'.format([unit.url for unit in rproject.units]))
            # need to change following line with PickleType
            tasks = rproject.download_units_diff(alert.template_type, content.links, save=True)
            #print('alert.template type = {}'.format(alert.template_type))
            #print('TASKSS ===> {}'.format(tasks))

            if tasks == None:
                flash_message(self, 'danger', 'Problem creating LIVE ALERT.')
                self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
                return
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
                alert.launched = True
                self.request_db.commit()

                self.session['tasks']['live_view'] = updated_tasks
                self.session['current_live_view_content'] = args['contentName']
                self.session['current_live_view_alert'] = args['alertName']
                self.session.save()
                self.redirect('/api/v1/users/{}/projects/{}/alerts/live/view'.format(username, projectname))
                return
        elif args['alertType'] == 'BasicReccurent' or args['alertType'] == 'CrontabSchedule':
            print('content --> {}'.format(content))
            # Loading project
            rproject = RProject(project.name, project.data_path, project.config_file)
            if len(self.session['project_config_file']) == 0:
                rproject._load_units_from_data_path()
            else:
                rproject._load_units_from_excel()

            if args['alertType'] == 'BasicReccurent':
                date_delayed = alert.start_time
                date_delayed = date_delayed.astimezone(pytz.utc)
                schedule = rrule(alert.repeat, dtstart=date_delayed, count=alert.max_count, interval=alert.interval)
                print('SCHEDULED BASIC RECC = {}'.format(schedule))
            else: # is necessarily a crontab schedule alert
                print('hour = {}, minute = {}'.format(alert.repeat_at.split(':')[0], alert.repeat_at.split(':')[1]))
                print('days_of_week = {}'.format(alert.days_of_week))
                schedule = crontab(hour=int(alert.repeat_at.split(':')[0]), minute=int(alert.repeat_at.split(':')[1]),\
                    day_of_week=alert.days_of_week, day_of_month='*', month_of_year='*')
                print('SCHEDULED CRONTAB = {}'.format(schedule))
        else: # there is room for further alert type
            flash_message(self, 'danger', 'Alert type not recognized. Contact admin.')
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
            return


        # Sync alert with Redbeat scheduler
        entry = rproject.download_units_diff_delayed_with_email(alert.name, alert.template_type,\
            schedule, content.links, content.mailing_list, user.email, project.name, save=True)
        
        # Scheduler must return an entry
        if entry is False:
            flash_message(self, 'danger', 'Scheduler not reachable.')
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
            return

        if entry.is_due()[1] is None:
            #delete entry that does not want to start
            entry.delete()
            flash_message(self, 'danger', 'Unable to start alert. Check if start date is greater than now.')
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
            return

        # Update DB state
        alert.launched = True
        self.request_db.commit()
        flash_message(self, 'warning', 'Reccurent ({}) alert {} succesfully launched. Alert is supposed to start in {} seconds.'.format(args['alertType'], alert.name, entry.is_due()[1]))
        self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))


class AlertStop(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('ARGS = {}'.format(args))

        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        content = project.contents.filter_by(name=args['contentName']).first()
        alert = content.alerts.filter_by(name=args['alertName']).first()
        #print('alert.alert_type = {}'.format(alert.alert_type))
        if alert.alert_type == 'Live':
            if 'live_view' in self.session['tasks']:
                res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
                print('Deleting old live view tasks from session.')
                del self.session['tasks']['live_view']
                self.session.save()
        elif alert.alert_type == 'BasicReccurent' or alert.alert_type == 'CrontabSchedule':
            print('Passe heree')
            try:
                # TODO: ADD try / catch if key not found in redbeat
                e = Entry.from_key('redbeat:'+alert.name, app=continuous_worker.app)
                e.delete()
                print('Alert {} succesfully deleted from redbeat'.format(alert.name))
            except Exception as e:
                print('Exception finding redbeat key : {}'.format(e))
                flash_message(self, 'danger', 'Alert {} not found in scheduler database.'.format(args['alertName']))
                self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
                return # TODO : Check if return is justified here

        alert.launched = False
        self.request_db.commit()
        flash_message(self, 'success', 'Alert {} succesfully stopped.'.format(args['alertName']))
        self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))


class AlertDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        #print('ARGS = {}'.format(self.form_data))
        content_name = self.get_argument('contentName')
        alert_name = self.get_argument('alertName')
        user = self.request_db.query(User).filter_by(username=username).first()
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
    @gen.coroutine
    def get(self, username, projectname):
        if 'live_view' in self.session['tasks']:
            tasks  = self.session['tasks']['live_view'].copy()
            self.render('projects/alerts/live-view.html', tasks=tasks)
        else:
            flash_message(self, 'warning', 'No current live view tasks yet.')
            self.redirect('/blank')            

class AlertLiveUpdate(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
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
                    if response['state'] == 'SUCCESS' and (response['status']['diff_neg'] != []\
                        or response['status']['diff_pos'] != []):
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
            flash_message(self, 'success', 'Pages successfully updated.')
            self.redirect('/')

class AlertLiveUpdateJSON(BaseView):
    SUPPORTED_METHODS = ['POST']
    @gen.coroutine
    def post(self):
        # try:
        args = json.loads(self.request.body)
        print('received args to update ------------------> {}'.format(args))
        user = self.request_db.query(User).filter_by(email=args['user_email']).first()
        project = user.projects.filter_by(name=args['project_name']).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_excel()
        print('TYPE args[url] = > {}'.format(type(args['urls'])))
        rproject.update_units_links(args['urls'])
        self.send_response(data={ 'message': 'OK' })
        # except Exception as e:
        #     print('Error updating content. Reason {}'.format(e))
        #     self.send_response(data={ 'message': 'ERROR {}'.format(e) })
