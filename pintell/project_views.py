import json
import datetime
import time
from pintell.views import BaseView
from pintell.models import Permission, Role, Project, User
from pintell.utils import flash_message, login_required
import pintell.session as session
from pintell.core.rproject import RProject

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
        units_stats = sbb_project.units_stats(units=sbb_project.filter_units())
        if units_stats is None:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.session['units_stats'] = units_stats
            self.render('projects/index.html', project=json_project, units_stats=units_stats)

class UserProjectDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        project = user.projects.filter_by(name=projectname).first()
        print('project details path2 = {}'.format(project.config_file))
        self.request_db.delete(project)
        self.request_db.commit()
        flash_message(self, 'success', 'Project {} succesfully deleted.'.format(projectname))
        self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))