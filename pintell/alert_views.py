import tornado
import json
import datetime
import time
from pintell.views import BaseView
from pintell.models import Permission, Role, Project, User, Content, Alert
from pintell.utils import flash_message, login_required, get_url_from_id, json_response
import pintell.session as session

class AlertCreateView(BaseView):
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
        # get recorded alerts for alert list
        all_alerts = []
        for content in contents:
            alerts = content.alerts.all()
            for alert in alerts:
                json_alert = alert.as_dict()
                json_alert['content_id'] = content.name
                all_alerts.append(json_alert)
        self.render('projects/alerts/index.html', contents=json_contents, alerts=all_alerts)

class AlertCreate(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('post args = {}'.format(args))
        # if box is checked, variable comes in like { "gridCheck": "on" }
        checked = False
        if hasattr(args, 'gridCheck'):
            checked = True
        content_name = args['inputContent'].split('(')[0]
        print('content -> {}'.format(content_name))
        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            content = project.contents.filter_by(name=content_name).first()
            new_alert = Alert(args['inputName'], args['inputType'], args['inputStartTime'], notify=checked)
            content.alerts.append(new_alert)
            self.request_db.add(content)
            self.request_db.commit()
            # need to put the code for crontab here now !! 
            flash_message(self, 'success', 'Alert {} successfully created.'.format(args['inputName']))
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts/create'.format(username, projectname))
        except Exception as e:
            print('Error recording alert in DB : {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(args['inputName']))
            # to be change to redirect to alerts/monitor_all view
            self.redirect('/api/v1/users/{}/projects/{}/alerts/create'.format(username, projectname))

class AlertLiveView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname, uid):
        self.render('projects/alerts/live-view.html', alertuid=uid)



















        