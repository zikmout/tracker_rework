import os
import tornado
from tornado import gen
import json
import datetime
import time
import pandas as pd
import numpy
import shutil
import math
from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required, get_url_from_id, json_response,\
replace_mix_option_with_all_existing_keywords, is_project_name_well_formated, check_valid_mail
import tracker.session as session
from tracker.core.rproject import RProject
import tracker.workers.continuous.continuous_worker as continuous_worker
from redbeat import RedBeatSchedulerEntry as Entry

from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view
from tracker.utils import revoke_all_tasks

class EmailToWatchlist(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        print('ARGS = {}'.format(self.form_data))
        if 'emailForWatchlist' not in self.form_data or\
         check_valid_mail(self.form_data['emailForWatchlist'][0]) is False:
            flash_message(self, 'danger', '\'{}\' is not a valid email address.'.format(self.form_data['emailForWatchlist'][0]))
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return
        to_delete = False
        to_add = False
        if 'emailForWatchlistType' in self.form_data and self.form_data['emailForWatchlistType'][0] == 'add':
            to_add = True
        else:
            to_delete = True

        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()

        rproject = RProject(project.name, project.data_path, project.config_file)
        # print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df.copy()

        # print('type col == {}'.format(type(config_df_updated['mailing_list'])))
        # if isinstance(config_df_updated['mailing_list'], numpy.float64):
            # config_df_updated.at[i, 'mailing_list'] = config_df_updated.at[i, 'mailing_list'].astype(str)
        # print('TYPE OF DF COL MAILING LIST = {}'.format(config_df_updated.dtypes['mailing_list']))
        if config_df_updated.dtypes['mailing_list'] == 'float64':
            # print('FLOAAT')
            config_df_updated['mailing_list'] = config_df_updated['mailing_list'].astype(str)
            # config_df_updated['mailing_list'].fillna('', inplace=True)
        for i in config_df_updated.index:
            cell = config_df_updated['mailing_list'][i]
            # print('cell == {}'.format(cell))
            # print('cell type : {}'.format(type(cell)))
            if to_add:
                if isinstance(cell, float) and math.isnan(cell):
                    # print('-> Is NaN or is equal to nothing')
                    # config_df_updated.at[i, 'mailing_list'] = config_df_updated.at[i, 'mailing_list'].astype(str)
                    # if isinstance(ccell, float):
                        # config_df_updated.at[i, 'mailing_list'] = config_df_updated.at[i, 'mailing_list'].astype(str)
                    # config_df_updated.at[i, 'mailing_list'] = config_df_updated.at[i, 'mailing_list'].astype(str)
                    config_df_updated.at[i, 'mailing_list'] = self.form_data['emailForWatchlist'][0]
                elif self.form_data['emailForWatchlist'][0] in cell:
                    flash_message(self, 'danger', '\'{}\' already in mailing_list.'.format(self.form_data['emailForWatchlist'][0]))
                    self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
                    return
                elif ';' in cell:
                    # print('-> Is MulTiPlE')
                    config_df_updated.at[i, 'mailing_list'] = cell + ';' + self.form_data['emailForWatchlist'][0]
                elif cell == 'nan':
                    # print('is nan guillement')
                    config_df_updated.at[i, 'mailing_list'] = self.form_data['emailForWatchlist'][0]
                else:
                    config_df_updated.at[i, 'mailing_list'] = config_df_updated.at[i, 'mailing_list'] + ';' + \
                    self.form_data['emailForWatchlist'][0]
            elif to_delete:
                print('CELL TO DELETE = {}'.format(cell))
                if isinstance(cell, float) and math.isnan(cell):
                    config_df_updated['mailing_list'][i] = ''
                    # No need to delete from nothing !
                    pass
                elif ';' in cell:
                    split_cell = cell.split(';')
                    try:
                        split_cell.remove(self.form_data['emailForWatchlist'][0])
                        split_cell = ';'.join(split_cell)
                        config_df_updated.at[i, 'mailing_list'] = split_cell
                    except Exception as e:
                        pass
                        # print('enter except = {}'.format(e))
                elif cell == 'nan':
                    config_df_updated.at[i, 'mailing_list'] = ''
                elif cell == self.form_data['emailForWatchlist'][0]:
                    config_df_updated.at[i, 'mailing_list'] = ''
                else:
                    pass
                    # config_df_updated.at[i, 'mailing_list'] = ''
        
        config_df_updated.to_excel(project.config_file, index=False)

        if to_add:
            flash_message(self, 'success', '\'{}\' successfully added to email recipients.'.format(self.form_data['emailForWatchlist'][0]))
        elif to_delete:
            flash_message(self, 'success', '\'{}\' successfully deleted from email recipients.'.format(self.form_data['emailForWatchlist'][0]))
        
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))

class DownloadFile(BaseView):
    @login_required
    @gen.coroutine
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        ifile  = open(project.config_file, 'rb')
        self.set_header('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.set_header('Content-Disposition', 'attachment; filename='+project.name+'.xlsx')
        self.write (ifile.read())

class FastProjectCreateView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username):
        file1 = self.request.files['file1'][0]
        fname = file1['filename'].replace(' ', '_').replace('.xlsx', '')
        project_name = file1['filename'].replace(' ', '_').replace('.xlsx', '')#os.path.splitext(fname)[0]
        if not is_project_name_well_formated(project_name):
            flash_message(self, 'danger', 'Error creating watchlist. Excel file name must only contain spaces or\
                alphanumeric characters.')
            self.redirect('/api/v1/users/{}/project_create'.format(username))
            return
        project_path = os.path.join(self.application.data_dir, project_name)

        if os.path.isdir(project_path):
            flash_message(self, 'danger', 'A directory with the same watchlist name seems to already exist.')
            self.redirect('/')
            return
        else:
            try:
                # creating project directory
                os.mkdir(project_path)
                # puting xlsx config file in it
                config_path = os.path.join(project_path, 'config.xlsx')
                with open(config_path, 'wb+') as fd:
                    fd.write(file1['body'])

                df = pd.read_excel(config_path)
                required_columns = ['Name', 'Website', 'target', 'target_label', 'mailing_list']
                for _ in required_columns:
                    if _ not in df.columns:
                        shutil.rmtree(project_path)
                        flash_message(self, 'danger', 'Problem creating watchlist. Please make sure following\
                         columns name are in excel file : {}.'.format(','.join(required_columns)))
                        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
                        return

                #create project
                print('name = {}, data_path = {}, config_df = {}'.format(project_name, self.application.data_dir, config_path))
                user = self.request_db.query(User).filter_by(username=username).first()
                new_project = Project(project_name, self.application.data_dir, config_path)
                user.projects.append(new_project)
                
                links = dict(zip(df['target'], df['target_label']))
                links = replace_mix_option_with_all_existing_keywords(links)
                # links = {k:[v] for k, v in links.items()}
                
                # add links to crawler logfile
                rproject = RProject(new_project.name, new_project.data_path, new_project.config_file)
                rproject.generate_crawl_logfile(links)
                rproject._load_units_from_data_path()
                idx, url_errors = rproject.add_links_to_crawler_logfile(links, wait=2)

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

                if len(url_errors) != 0:
                    formated_errors = list()
                    for errs in url_errors:
                        for k, v in errs.items():
                            formated_errors.append('{} ({})'.format(k, v)) 
                    flash_message(self, 'warning', '\'{}\' successfully uploaded. Default live alert {} created. Here are the website that could\
                        not be downloaded : {}'.format(fname, fname.replace('.xlsx', ''), '-'.join(formated_errors)))
                else:
                    flash_message(self, 'success', '\'{}\' successfully uploaded. Alert {} created.'.format(fname, fname.replace('.xlsx', '')))
                self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            except Exception as e:
                print('ERROR = {}'.format(e))
                flash_message(self, 'danger', 'Problem creating watchlist. Contact admin for further details.')
                self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

class ProjectsCreateView(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    @gen.coroutine
    def get(self, username):
        self.render('projects/create.html')

    @login_required
    @gen.coroutine
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
    @gen.coroutine
    def get(self, username):
        user = self.request_db.query(User).filter_by(username=username).first()
        user_projects_json = list()
        user_projects = user.projects.all()
        if user_projects:
            [user_projects_json.append(project.as_dict()) for project in user_projects]
        # get nb of active alerts in projects from redbeat
        actives_json = {k['name']:0 for k in user_projects_json}
        for user_project in user_projects:
            user_contents = user_project.contents.all()
            for user_content in user_contents:
                alerts = user_content.alerts.all()
                for alert in alerts:
                    json_alert = alert.as_dict()
                    if json_alert['alert_type'] != 'Live':
                        try:
                            e = Entry.from_key('redbeat:'+alert.name, app=continuous_worker.app)
                            if json_alert['launched'] == 'True':
                                if user_project.name in actives_json:
                                    actives_json[user_project.name] = actives_json[user_project.name] + 1
                                else:
                                    actives_json[user_project.name] = 1
                        except Exception as e:
                            pass
        for user_project_json in user_projects_json.copy():
            user_project_json['nb_active_alerts'] = actives_json[user_project_json['name']]
        self.render('projects/manage.html', projects=user_projects_json)

class UserProjectView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
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
            flash_message(self, 'danger', 'No source in watchlist {} yet.'.format(projectname))
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
            flash_message(self, 'danger', 'There are no source in watchlist {}.'.format(project.name))
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
                # TODO: Also set all alert in postgresql so status launched = False if s.o. forget to stop its alert
                # Deleting live view from session and killing backend task
                if 'live_view' in self.session['tasks']:
                    res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker in self.session['tasks']['live_view']])
                    print('Deleting live view tasks from session.')
                    del self.session['tasks']['live_view']
                    self.session.save()
                self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))


class UserProjectDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        #print('ARGS DELETE = {}'.format(self.args))
        user = self.request_db.query(User).filter_by(username=self.session['username']).first()
        project = user.projects.filter_by(name=projectname).first()
        content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
        if content_to_delete is not None:
            alerts_to_delete = content_to_delete.alerts.all()
            for a in alerts_to_delete:
                #print('a.name = {}'.format(a.name))
                if a.alert_type != 'Live':
                    try:
                        print('Deleting non Live alert from redbeat : {}'.format(a.name))
                        e = Entry.from_key('redbeat:'+a.name, app=continuous_worker.app)
                        e.delete()
                    except Exception as e:
                        print('[FAIL] Deleting non Live alert from redbeat : {}'.format(a.name))
                        print('Reason = {}'.format(e))
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
                    found on server ! Maybe no source had been parameterized yet?'.format(projectname))
            else:
                shutil.rmtree(fname)
                print('Folder \'{}\' successfully removed.'.format(fname))
                flash_message(self, 'success', 'Watchlist {} succesfully deleted from DB and server.'.format(projectname))
        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
