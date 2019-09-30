import os
import tornado
import json
import datetime
import time
import pandas as pd
import shutil
from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required, get_url_from_id, json_response,\
replace_mix_option_with_all_existing_keywords
import tracker.session as session
from tracker.core.rproject import RProject


class FastProjectCreateView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username):
        file1 = self.request.files['file1'][0]
        fname = file1['filename'].replace(' ', '_')
        project_name = file1['filename'].replace(' ', '_')#os.path.splitext(fname)[0]
        project_path = os.path.join(self.application.data_dir, project_name)

        if os.path.isdir(project_path):
            flash_message(self, 'danger', 'A directory with the same watchlist name seems to already exist.')
            self.redirect('/')
        else:
            try:
                # creating project directory
                os.mkdir(project_path)
                # puting xlsx config file in it
                config_path = os.path.join(project_path, 'config' + os.path.splitext(fname)[1])
                with open(config_path, 'wb+') as fd:
                    fd.write(file1['body'])

                #create project
                print('name = {}, data_path = {}, config_df = {}'.format(project_name, self.application.data_dir, config_path))
                user = self.request_db.query(User).filter_by(username=username).first()
                new_project = Project(project_name, self.application.data_dir, config_path)
                user.projects.append(new_project)
                
                df = pd.read_excel(config_path)
                links = dict(zip(df['target'], df['target_label']))
                links = replace_mix_option_with_all_existing_keywords(links)
                # links = {k:[v] for k, v in links.items()}
                
                # add links to crawler logfile
                rproject = RProject(new_project.name, new_project.data_path, new_project.config_file)
                rproject.generate_crawl_logfile(links)
                rproject._load_units_from_data_path()
                rproject.add_links_to_crawler_logfile(links)

                # create content
                mailing_list = dict(zip(df['target'], df['mailing_list']))
                print('Mailing LIST = {}'.format(mailing_list))
                new_content = Content(project_name + '_default', links, mailing_list)
                new_project.contents.append(new_content)

                # # create live alert
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                new_alert = Alert(project_name + '_default', 'Live', now)
                new_content.alerts.append(new_alert)
                self.request_db.add(user)
                self.request_db.commit()

                flash_message(self, 'success', '\'{}\' successfully uploaded. Alert {} created.'.format(fname, fname.replace('.xlsx', '')))
                self.redirect('/')
            except Exception as e:
                print('ERROR = {}'.format(e))
                flash_message(self, 'danger', 'Problem creating quick watchlist. Check logs.')
                self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

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
        print('name = {}, data_path = {}, config_df = {}'.format(name, data_path, config_df))
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        new_project = Project(name, data_path, config_df)
        user.projects.append(new_project)
        try:
            self.request_db.add(user)
            self.request_db.commit()
            flash_message(self, 'success', 'Watchlist {} succesfully created.'.format(name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
        except Exception as e:
            flash_message(self, 'danger', 'Problem creating watchlist: {}. Maybe try another name ?'.format(name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

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
        # if box is checked, variable comes in like { "fromExcel": "on" }
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        json_project = project.as_dict()
        print('json_project = {}'.format(json_project))
        units = None
        if not os.path.isfile(project.config_file):
            self.session['units'] = units
            self.session['current_project'] = project.name
            self.session['project_data_path'] = project.data_path
            self.session['project_config_file'] = project.config_file
            # self.session['is_project_empty'] = True
            self.session.save()
            #flash_message(self, 'warning', 'There are no units at the moment. Go on the \'Website\' section and add one.')
            flash_message(self, 'danger', 'No website in watchlist {} yet.'.format(projectname))
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            # self.render('projects/index.html', project=json_project, units=units)    
            return
        try:
            rproject = RProject(project.name, project.data_path, project.config_file)
            if 'fromExcel' in args:
                rproject._load_units_from_excel()
            else:
                rproject._load_units_from_data_path()
            units = rproject.units_stats(units=rproject.filter_units())
        except Exception as e:
            print('[ERROR] - {}'.format(e))
            flash_message(self, 'danger', 'Problem while loading watchlist {}. Please check paths.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return 
        if units is None:
            flash_message(self, 'danger', 'There are no units in watchlist {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return
        else:
            self.session['units'] = units
            self.session['current_project'] = project.name
            self.session['project_data_path'] = project.data_path
            self.session['project_config_file'] = project.config_file
            # self.session['is_project_empty'] = False
            self.session.save()
            if 'is_admin' in self.session and 'is_simplified' in self.session and self.session['is_simplified'] is False:
                self.render('projects/index.html', project=json_project, units=units)
                return
            else:
                self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))


class UserProjectDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname):
        #print('ARGS DELETE = {}'.format(self.args))
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        project = user.projects.filter_by(name=projectname).first()
        self.request_db.delete(project)
        self.request_db.commit()

        # if deleted project was the current project, delete it from user session
        keys_to_delete = ['units', 'current_project', 'project_data_path', 'project_config_file']
        for k in keys_to_delete:
            if k in self.session:
                del self.session[k]
        self.session.save()

        if 'deleteRelatedFilesCheck' in self.args:
            #print('Removing project from hard drive ...')
            fname = os.path.join(self.application.data_dir, projectname)
            if not os.path.exists(fname):
                flash_message(self, 'warning', 'Watchlist {} succesfully deleted from DB but was not \
                    found on server ! Maybe no websites were parameterized yet?'.format(projectname))
            else:
                shutil.rmtree(fname)
                print('Folder \'{}\' successfully removed.'.format(fname))
                flash_message(self, 'success', 'Watchlist {} succesfully deleted from DB and server.'.format(projectname))
        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
