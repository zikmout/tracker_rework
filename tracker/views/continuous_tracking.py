import os
import shutil
import pandas as pd
from tornado import gen
import re
from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required
import tracker.session as session
from tracker.core.rproject import RProject

class ContinuousTrackingCreateView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username):
        project_name = self.get_argument('ProjectName')
        project_name = project_name.replace(' ', '_') 
        project_path = os.path.join(self.application.data_dir, project_name)
        print('project name = {}, project path = {}'.format(project_name, project_path))

        # check whether project with similar name exist on computer
        if os.path.exists(project_path):
            flash_message(self, 'danger', '\'{}\' project name already exists. Please choose a different name.'\
                .format(project_name))
            self.redirect('/api/v1/users/admin/project_create')
            return

        config_path = os.path.join(project_path, 'config.xlsx')
        user = self.request_db.query(User).filter_by(username=username).first()
        new_project = Project(project_name, self.application.data_dir, config_path)
        user.projects.append(new_project)
        self.request_db.add(user)
        self.request_db.commit()

        flash_message(self, 'success', 'Watchlist \'{}\' successfully created.'\
            .format(project_name))
        self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))

class UserProjectWebsitesView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    @gen.coroutine
    def get(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        # if box is checked, variable comes in like { "fromExcel": "on" }
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        json_project = project.as_dict()
        units = None
        if not os.path.isfile(project.config_file):
            #print('project lines ==> {}'.format(rproject.lines))
            self.render('projects/websites.html', project=json_project, units=units, lines=None)
            return
        try:
            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject._load_units_from_excel()
            rproject._load_tracking_config_excel()
            #units = rproject.units_stats(units=rproject.filter_units())
        except Exception as e:
            print('[ERROR] - {}'.format(e))
            flash_message(self, 'danger', 'Problem while loading project {}. Are you sure path is correct and there is an excel file ?'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return 
        if rproject.units is None:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return
        # TODO : check if 'is_excel' is in memory (below) and delete above check conditions
        if 'units' not in self.session or 'current_project' not in self.session or 'project_data_path' not in self.session\
        or 'project_config_file' not in self.session:
            flash_message(self, 'danger', 'No current project in session at the moment. Please load one.')
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return
        else:
            #print('project lines ==> {}'.format(rproject.lines))
            self.render('projects/websites.html', project=json_project, units=units, lines=rproject.lines.copy())

class UserProjectAddWebsite(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = self.form_data
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        # print('ARGSSSS = {}'.format(args))
        if args['inputWebsite'][0] == '':
            regex = r"^https?://[^/]+"
            url = re.findall(regex, args['inputTarget'][0])[0]
            args['inputWebsite'][0] = url
        # If first time adding website, must create config_file, folder, logfile
        if not os.path.isfile(project.config_file):
            # create project directory
            project_path = os.path.join(self.application.data_dir, projectname)
            os.mkdir(project_path)
            # put xlsx config file in it with both column 'target' and 'target_label' to prepare header of excel file
            config_path = os.path.join(project_path, 'config.xlsx')
            df = pd.DataFrame({'Name':args['inputName'], 'Website':args['inputWebsite'], 'target':args['inputTarget'],\
                'target_label':args['inputKeywords'], 'mailing_list': args['inputMailingList']})
            writer = pd.ExcelWriter(config_path, engine='xlsxwriter')
            df.to_excel(writer)
            writer.save()
            
            df = pd.read_excel(config_path)
            links = dict(zip(df['target'], df['target_label']))
            links = {k:[v] for k, v in links.items()}
            
            # add links to crawler logfile
            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject.generate_crawl_logfile(links)
            rproject._load_units_from_data_path()
            rproject.add_links_to_crawler_logfile(links)

            mailing_list = dict(zip(df['target'], df['mailing_list']))
            new_content = Content(projectname + '_default', links, mailing_list)
            project.contents.append(new_content)
            self.request_db.commit()
            units = rproject.units_stats(units=rproject.filter_units())
            self.session['units'] = units
            # self.session['is_project_empty'] = False
            self.session.save()
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return
        else:
            rproject = RProject(project.name, project.data_path, project.config_file)
            print('config df before = {}'.format(rproject.config_df))
            config_df_updated = rproject.config_df.append({'Name': args['inputName'][0], 'Website': args['inputWebsite'][0],\
                'target': args['inputTarget'][0], 'target_label':args['inputKeywords'][0], 'mailing_list': args['inputMailingList'][0]}, ignore_index=True)
            print('config df after = {}'.format(config_df_updated))
            config_df_updated.to_excel(project.config_file, index=False)

            # generate crawl logfile
            

            links1 = {args['inputTarget'][0]:args['inputKeywords']}
            #rproject.generate_crawl_logfile(links) # TODO: take off index.html from function 
            rproject._load_units_from_data_path()
            idx = rproject.add_links_to_crawler_logfile(links1)
            #print('{}/{} links needed to be added to logfile.'.format(idx, len(links)))
            
            # Update content (take first content with name projectname + '_default')
            df = pd.read_excel(project.config_file)
            links = dict(zip(df['target'], df['target_label']))
            links = {k:[v] for k, v in links.items()}

            content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
            self.request_db.delete(content_to_delete)
            self.request_db.commit()

            mailing_list = dict(zip(df['target'], df['mailing_list']))
            new_content = Content(projectname + '_default', links, mailing_list)
            project.contents.append(new_content)
            self.request_db.commit()

            # change session data to take account of deleted unit
            units = rproject.units_stats(units=rproject.filter_units())
            self.session['units'] = units
            self.session.save()
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))

class UserProjectDeleteWebsite(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = self.form_data
        print('args = {}'.format(args))
        # delete unit from excel file
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df[rproject.config_df.Website != args['websiteToDelete'][0]]
        config_df_updated.to_excel(project.config_file, index=False)
        # delete unit from hard drive
        # TODO: Here it delete the entire unit, not the target subunit, need to correct this !!
        # (i.e use args['targetToDelete'] which is not used yet)
        if (rproject.delete_unit(args['websiteToDelete'][0])):
            print('Unit successfully deleted from hard drive')
        # reload units from excel
        rproject._load_units_from_data_path()
        # change session data to take account of deleted unit
        units = rproject.units_stats(units=rproject.filter_units())
        self.session['units'] = units
        # if units is None, it means project can be emptied
        if units is None:
            fname = os.path.join(self.application.data_dir, projectname)
            shutil.rmtree(fname)
        else:
            # Update content (take first content with name projectname + '_default')
            df = pd.read_excel(project.config_file)
            links = dict(zip(df['target'], df['target_label']))
            links = {k:[v] for k, v in links.items()}
            
            content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
            self.request_db.delete(content_to_delete)
            self.request_db.commit()

            mailing_list = dict(zip(df['target'], df['mailing_list']))
            new_content = Content(projectname + '_default', links, mailing_list)
            project.contents.append(new_content)
            self.request_db.commit()

        self.session.save()
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))

class UserProjectEditWebsite(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = self.form_data
        print('args = {}'.format(args))
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()

        rproject = RProject(project.name, project.data_path, project.config_file)
        print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df.copy()
        config_df_updated = config_df_updated[config_df_updated.Website != args['inputWebsite'][0]]
        if 'inputKeywords' in args:
            keywords_excel = ';'.join(args['inputKeywords'])
        else:
            keywords_excel = ''
        if 'inputMailingList' in args:
            mailing_list_excel = ';'.join(args['inputMailingList'])
        else:
            mailing_list_excel = '' # why is this ??!
        config_df_updated = config_df_updated.append({'Name': args['inputName'][0], 'Website': args['inputWebsite'][0],\
            'target': args['inputTarget'][0], 'target_label':keywords_excel, 'mailing_list': mailing_list_excel}, ignore_index=True)
        print('config df after = {}'.format(config_df_updated))
        config_df_updated.to_excel(project.config_file, index=False)

        # Update content (take first content with name projectname + '_default')
        df = pd.read_excel(project.config_file)
        links = dict(zip(df['target'], df['target_label']))
        links = {k:[v] for k, v in links.items()}
        
        content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
        self.request_db.delete(content_to_delete)
        self.request_db.commit()

        mailing_list = dict(zip(df['target'], df['mailing_list']))
        new_content = Content(projectname + '_default', links, mailing_list)
        project.contents.append(new_content)
        self.request_db.commit()

        # change session data to take account of deleted unit
        units = rproject.units_stats(units=rproject.filter_units())
        self.session['units'] = units
        self.session.save()
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
