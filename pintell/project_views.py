import tornado
import json
import datetime
import time
from pintell.views import BaseView
from pintell.models import Permission, Role, Project, User, Content
from pintell.utils import flash_message, login_required, get_url_from_id, json_response, \
get_celery_task_state
from pintell.core.utils import get_formated_units
import pintell.session as session
from pintell.core.rproject import RProject
from pintell.workers.download_worker import download_website

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
        user = self.request_db.query(User).filter_by(username=username).first()
        user_projects_json = list()
        user_projects = user.projects.all()
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
            self.session['current_project'] = project.name
            self.session.save()
            self.render('projects/index.html', project=json_project, units=units)

class UserProjectDownloadView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.render('projects/download.html', units=units)

class UserProjectDiffCreateView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
        formated_units = get_formated_units(rproject.units)
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.render('projects/diff_create.html', formated_units=formated_units)

class UserProjectDiffSchedule(BaseView):
    SUPPORTED_METHODS = ['POST']
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
    @login_required
    def post(self, username, projectname):
        data = tornado.escape.json_decode(self.request.body)
        print('POST received, links are = {}'.format(data))
        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            new_content = Content(data['name'], data['links'])
            project.contents.append(new_content)
            self.request_db.add(project)
            self.request_db.commit()
            flash_message(self, 'success', 'Content {} successfully created.'.format(data['name']))
            self.write(json_response('success', None, 'Content succesfully created.'))
        except Exception as e:
            print('Error recording content in DB : {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(data['name']))
            self.write(json_response('error', None, '{}'.format(e)))

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

        print('View DESACTIVATED')
        exit(0)
        #task = download.apply_async((username,))
        #print('Task backend = {}'.format(task.backend))
        if 'download' not in self.session['tasks']:
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
        task = download_website.AsyncResult(task_id)
        print('Task backend = {}'.format(task.backend))
        #task = task.get()
        print('task_id: {}'.format(task_id))
        response = get_celery_task_state(task)
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