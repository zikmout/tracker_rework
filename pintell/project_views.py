import tornado
import json
import datetime
import time
from pintell.views import BaseView
from pintell.models import Permission, Role, Project, User
from pintell.utils import flash_message, login_required, get_url_from_id
import pintell.session as session
from pintell.core.rproject import RProject
from pintell.workers.download_worker import download

class ProjectsCreateView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    def get(self, username):
        #print('params ======== {}'.format(selg.get_argument('username')))
        self.render('projects/create.html')

    @login_required
    def post(self, username):
        name = self.get_argument('ProjectName')
        data_path = self.get_argument('ProjectLocation')
        try:
            config_df = self.get_argument('ConfigLocation')
        except Exception as e:
            config_df = None
            print('-> No config location provided.')
        print('name = {}, data_path = {}, config_df = {}'.format(name, data_path, config_df))
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        new_project = Project(name, data_path, config_df)
        user.projects.append(new_project)
        try:
            self.request_db.add(user)
            self.request_db.commit()
            flash_message(self, 'success', 'Project {} succesfully created.'.format(name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        except Exception as e:
            flash_message(self, 'danger', 'Problem creating project: {}. Maybe try another name ?'.format(name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))

class UserProjectListView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username):
        user = self.request_db.query(User).filter_by(username=username)
        user_projects_json = list()
        user_projects = user[0].projects.all()
        if user_projects:
            [user_projects_json.append(project.as_dict()) for project in user_projects]
        self.render('projects/manage.html', projects=user_projects_json)

class UserProjectView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        print('arrived project name = {}'.format(projectname))
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        json_project = project.as_dict()
        # Loading project
        sbb_project = RProject(project.name, project.data_path, project.config_file)
        sbb_project._load_units_from_data_path()
        units = sbb_project.units_stats(units=sbb_project.filter_units())
        #sbb_project.download_units(['http://www.viscofan.com'])
        if units is None:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.session['units'] = units
            self.session.save()
            self.render('projects/index.html', project=json_project, units=units)

class UserUnitView(BaseView):
    SUPPORTED_METHODS = ['GET']
    def get(self, username, projectname, uid):
        url = get_url_from_id(self.session['units'], uid)
        self.render('unit/index.html', url=url)

class UserTaskCreate(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self, username):
        print('SELF SESSION BEFORE: {}'.format(self.session))
        # Load celery background task
        task = download.apply_async((username,))#username, 1, 1000)
        if not hasattr(self.session['tasks'], 'download'):
            self.session['tasks']['download'] = dict()
        self.session['tasks']['download'].update({task.id : username})
        self.session.save()
        print('SELF SESSION AFTER: {}'.format(self.session))
        self.set_header('Location', '/api/v1/users/{}/tasks/status/{}'.format(self.session['username'], task.id))

class UserTaskStatus(BaseView):
    SUPPORTED_METHODS = ['GET']
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self, username, task_id):
        task = download.AsyncResult(task_id)
        print('task_id: {}'.format(task_id))
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending ...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info)
            }
        print('response : {}'.format(response))
        self.write(response)

class UserProjectDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        project = user.projects.filter_by(name=projectname).first()
        self.request_db.delete(project)
        self.request_db.commit()
        flash_message(self, 'success', 'Project {} succesfully deleted.'.format(projectname))
        self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))