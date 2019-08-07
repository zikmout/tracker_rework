import os
import shutil
import pandas as pd
from tornado import gen
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
        project_path = os.path.join(self.application.data_dir, project_name)
        print('project name = {}, project path = {}'.format(project_name, project_path))

        # check whether project with similar name exist on computer
        if os.path.exists(project_path):
            flash_message(self, 'danger', '\'{}\' project name already exists. Please choose a different name.'\
                .format(project_name))
            self.redirect('/api/v1/users/admin/project_create')
            return

        # else create project directory
        os.mkdir(project_path)

        # puting xlsx config file in it
        config_path = os.path.join(project_path, 'config.xlsx')

        # create both column 'target' and 'target_label' to prepare header of excel file
        df = pd.DataFrame({'Name':['invader'], 'Website':['https://space-invaders.com/'], 'target':['https://space-invaders.com/spaceshop/'], 'target_label':['space-invader']})
        writer = pd.ExcelWriter(config_path, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()

        #create project in db
        print('name = {}, data_path = {}, config_df = {}'.format(project_name, self.application.data_dir, config_path))
        user = self.request_db.query(User).filter_by(username=username).first()
        new_project = Project(project_name, self.application.data_dir, config_path)
        user.projects.append(new_project)
        
        df = pd.read_excel(config_path)
        links = dict(zip(df['target'], df['target_label']))
        links = {k:[v] for k, v in links.items()}

        print('links look like this = {}'.format(links))
        
        # add links to crawler logfile
        rproject = RProject(new_project.name, new_project.data_path, new_project.config_file)
        rproject.generate_crawl_logfile(links)
        rproject._load_units_from_data_path()
        rproject.add_links_to_crawler_logfile(links)


        # create content (consistent with name)
        new_content = Content('invader_spider', links)
        new_project.contents.append(new_content)

        # # create live alert
        #new_alert = Alert(project_name + '_qp_live', 'Live', "2011-08-19T13:45:00")
        #new_content.alerts.append(new_alert)
        self.request_db.add(user)
        self.request_db.commit()

        flash_message(self, 'success', 'Continuous tracker project \'{}\' successfully created.'\
            .format(project_name))
        self.redirect('/api/v1/users/admin/projects_manage')

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
        try:
            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject._load_units_from_excel()
            rproject._load_tracking_config_excel()
            #units = rproject.units_stats(units=rproject.filter_units())
        except Exception as e:
            print('[ERROR] - {}'.format(e))
            flash_message(self, 'danger', 'Problem while loading project {}. Are you sure path is correct and there is an excel file ?'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
            return 
        if rproject.units is None:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
            return
        # TODO : check if 'is_excel' is in memory (below) and delete above check conditions
        if 'units' not in self.session or 'current_project' not in self.session or 'project_data_path' not in self.session\
        or 'project_config_file' not in self.session:
            flash_message(self, 'danger', 'No current project in session at the moment. Please load one.')
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
            return
        else:
            print('project lines ==> {}'.format(rproject.lines))
            self.render('projects/websites.html', project=json_project, units=units, lines=rproject.lines.copy())

class UserProjectAddWebsite(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        args = self.form_data
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df.append({'Name': args['inputName'][0], 'Website': args['inputWebsite'][0],\
            'target': args['inputTarget'][0], 'target_label':args['inputKeywords'][0]}, ignore_index=True)
        print('config df after = {}'.format(config_df_updated))
        config_df_updated.to_excel(project.config_file, index=False)

        # generate crawl logfile
        links = {args['inputTarget'][0]:args['inputKeywords']}
        rproject.generate_crawl_logfile(links) # TODO: take off index.html from function 
        rproject._load_units_from_data_path()
        rproject.add_links_to_crawler_logfile(links)

        # create content (consistent with name)
        new_content = Content(args['inputName'][0] + '_spider', links)
        project.contents.append(new_content)

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
        config_df_updated = config_df_updated.append({'Name': args['inputName'][0], 'Website': args['inputWebsite'][0],\
            'target': args['inputTarget'][0], 'target_label':keywords_excel}, ignore_index=True)
        print('config df after = {}'.format(config_df_updated))
        config_df_updated.to_excel(project.config_file, index=False)

        # change session data to take account of deleted unit
        units = rproject.units_stats(units=rproject.filter_units())
        self.session['units'] = units
        self.session.save()
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
