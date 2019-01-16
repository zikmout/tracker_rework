import tornado
import json
import datetime
import time
from pintell.views.base import BaseView
from pintell.models import Permission, Role, Project, User, Content
from pintell.utils import flash_message, login_required, get_url_from_id, json_response
import pintell.session as session
from pintell.core.rproject import RProject

class ProjectsCreateView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    def get(self, username):
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
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('post args = {}'.format(args))
        # if box is checked, variable comes in like { "fromExcel": "on" }
        checked = False
        if 'fromExcel' in args:
            checked = True
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        json_project = project.as_dict()
        units = None
        # Loading project
        if checked is False:
            try:
                print('Loading project from data path ...')
                rproject = RProject(project.name, project.data_path, project.config_file)
                rproject._load_units_from_data_path()
                self.session['loading_method'] = 'data'
                self.session.save()
                units = rproject.units_stats(units=rproject.filter_units())
            except Exception as e:
                print('[ERROR] - {}'.format(e))
                flash_message(self, 'danger', 'Problem while loading project {}. Check if data path exist.'.format(project.name))
                self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
                return
        else:
            try:
                rproject = RProject(project.name, project.data_path, project.config_file)
                rproject._load_units_from_excel()
                self.session['loading_method'] = 'file'
                self.session.save()
                units = rproject.units_stats_from_excel(units=rproject.filter_units())
            except Exception as e:
                print('[ERROR] - {}'.format(e))
                flash_message(self, 'danger', 'Problem while loading project {}. Check if config path exist.'.format(project.name))
                self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
                return

        if units is None:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
            return
        else:
            self.session['units'] = units
            self.session['current_project'] = project.name
            self.session.save()
            self.render('projects/index.html', project=json_project, units=units)    
            return

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