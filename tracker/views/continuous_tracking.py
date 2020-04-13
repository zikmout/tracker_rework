import os
import shutil
import pandas as pd
from tornado import gen
import math
import re
from tracker.views.base import BaseView
from tracker.models import Permission, Role, Project, User, Content, Alert
from tracker.utils import flash_message, login_required, is_project_name_well_formated, revoke_all_tasks,\
make_sure_entries_by_user_are_well_formated, erase_link_from_hd
import tracker.session as session
from tracker.core.rproject import RProject
import tracker.core.utils as utils
import tracker.workers.continuous.continuous_worker as continuous_worker
from tracker.celery import live_view_worker_app
from tracker.workers.live.live_view_worker import live_view
from redbeat import RedBeatSchedulerEntry as Entry

class ContinuousTrackingCreateView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username):
        try:
            project_name = self.get_argument('ProjectName')
            project_name = project_name
            project_name = '_'.join(re.split(r"\s+", project_name.strip()))
            
            project_path = os.path.join(self.application.data_dir, project_name)
            if not is_project_name_well_formated(project_name):
                flash_message(self, 'danger', 'Error creating watchlist. Please use only spaces or alphanumeric characters.')
                self.redirect('/api/v1/users/{}/project_create'.format(self.session['username']))
                return
            
            # print('project name = {}, project path = {}'.format(project_name, project_path))
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
        except Exception as e:
            flash_message(self, 'danger', 'Error creating watchlist, please contact admin for further details.')
            print('Error creating watchlist : {}'.format(e))
            self.redirect('/api/v1/users/{}/project_create'.format(self.session['username']))

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
            flash_message(self, 'danger', 'Problem while loading watchlist {}. Are you sure path is correct and there is an excel file ?'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return 
        if rproject.units is None:
            flash_message(self, 'danger', 'There are no sources in watchlist {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
            return
        # TODO : check if 'is_excel' is in memory (below) and delete above check conditions
        if 'units' not in self.session or 'current_project' not in self.session or 'project_data_path' not in self.session\
        or 'project_config_file' not in self.session:
            flash_message(self, 'danger', 'No current watchlist in session at the moment. Please load one.')
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
        #print('ARGSSSS = {}'.format(args))

        print('INPUT WEBSITE ENTER = {}, INPUT TARGET ENTER = {}'.format(args['inputWebsite'][0], args['inputTarget'][0]))
        # Make sure user does not mess up with url entries otherwise messes up with the crawler/downloader !!
        args['inputWebsite'][0], args['inputTarget'][0] = make_sure_entries_by_user_are_well_formated(\
            args['inputWebsite'][0], args['inputTarget'][0])
        
        print('INPUT WEBSITE EXIT = {}, INPUT TARGET EXIT = {}'.format(args['inputWebsite'][0], args['inputTarget'][0]))
        if args['inputWebsite'][0] is False or args['inputTarget'][0] is False:
            flash_message(self, 'danger', 'Url(s) not properly formated.')
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return

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
            # print('links to generate are = {}'.format(links))
            rproject.generate_crawl_logfile(links)
            rproject._load_units_from_data_path()
            idx, url_errors = rproject.add_links_to_crawler_logfile(links)

            mailing_list = dict(zip(df['target'], df['mailing_list']))
            new_content = Content(projectname + '_default', links, mailing_list)
            project.contents.append(new_content)
            self.request_db.commit()
            units = rproject.units_stats(units=rproject.filter_units())
            self.session['units'] = units
            # self.session['is_project_empty'] = False
            self.session.save()

            if url_errors != []:
                # Supposed to be only one error here, because one link (TODO: Check if problem there is)
                for err in url_errors:
                    for k, v in err.items():
                        target_url = k
                        target_error = v
                        # Getting unit that was unable to be downloaded and take it off from crawler logfile
                        # TODO : Delete this below off when reconfiguring crawler !
                        del_unit = rproject.get_unit_from_url(k)
                        del_unit.remove_crawler_link(k)

                flash_message(self, 'danger', 'Impossible to download provided target URL : {} (Reason: {})'.format(args['inputTarget'][0], target_error))
            else:
                flash_message(self, 'success', 'Successfully downloaded URL : {}'.format(args['inputTarget'][0]))
                # self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
                # return
            # self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            # return
        else:
            rproject = RProject(project.name, project.data_path, project.config_file)
            print('config df before = {}'.format(rproject.config_df))
            config_df_updated = rproject.config_df.append({'Name': args['inputName'][0], 'Website': args['inputWebsite'][0],\
                'target': args['inputTarget'][0], 'target_label':args['inputKeywords'][0], 'mailing_list': args['inputMailingList'][0]}, ignore_index=True)
            print('config df after = {}'.format(config_df_updated))
            config_df_updated.to_excel(project.config_file, index=False)

            # generate crawl logfile
            df = pd.read_excel(project.config_file)
            links = dict(zip(df['target'], df['target_label']))
            new_link = {k:[v] for k, v in links.items() if k == args['inputTarget'][0]} # Make sur only one link is selected
            # Carreful: Need to keep all links here because new content has to be created !
            all_links = {k:[v] for k, v in links.items()}

            #links1 = {args['inputTarget'][0]:args['inputKeywords']}
            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject.generate_crawl_logfile(new_link) # TODO: take off index.html from function 
            rproject._load_units_from_data_path()
            idx, url_errors = rproject.add_links_to_crawler_logfile(new_link)
            #print('{}/{} links needed to be added to logfile.'.format(idx, len(links)))
            
            content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
            alerts_to_delete = content_to_delete.alerts.all()
            for a in alerts_to_delete:
                # print('a.name = {}'.format(a.name))
                if a.alert_type != 'Live':
                    try:
                        # print('Deleting from redbeat non Live alert : {}'.format(a.name))
                        e = Entry.from_key('redbeat:'+a.name, app=continuous_worker.app)
                        e.delete()
                    except Exception as e:
                        print('[FAIL] Deleting from redbeat non Live alert : {}'.format(a.name))
                        # print('Reason = {}'.format(e))
            if 'tasks' in self.session and 'live_view' in self.session['tasks']:
                # print('There is a live alert to be DELETED HERE : {}'.format(a.alert_type))
                try:
                    res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker\
                     in self.session['tasks']['live_view']])
                    # print('Deleting old live view tasks from session: OK !!!')
                except Exception as e:
                    print('[ERROR] Revoking live view tasks from session. /!\\ ERROR = {}'.format(e))
                del self.session['tasks']['live_view']

            self.request_db.delete(content_to_delete)
            self.request_db.commit()

            mailing_list = dict(zip(df['target'], df['mailing_list']))
            new_content = Content(projectname + '_default', all_links, mailing_list)
            project.contents.append(new_content)
            self.request_db.commit()

            # change session data to take account of deleted unit
            rproject = RProject(project.name, project.data_path, project.config_file) # freshly added
            units = rproject.units_stats(units=rproject.filter_units())
            self.session['units'] = units
            self.session.save()
            
            if url_errors != []:
                # Supposed to be only one error here, because one link (TODO: Check if problem there is)
                for err in url_errors:
                    for k, v in err.items():
                        target_url = k
                        target_error = v
                        del_unit = rproject.get_unit_from_url(k)
                        del_unit.remove_crawler_link(k)

                flash_message(self, 'danger', 'Impossible to download provided target URL : {} (Reason: {})'.format(args['inputTarget'][0], target_error))
            else:
                flash_message(self, 'success', 'Successfully downloaded URL : {}'.format(args['inputTarget'][0]))
                # self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
                # return
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
        return


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

        # Get initial links to remove later (not optimal ! Eventually change later)
        initial_df = pd.read_excel(project.config_file)
        initial_links = dict(zip(initial_df['target'], initial_df['target_label']))
        # print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df[rproject.config_df.target != args['targetToDelete'][0]]
        config_df_updated.to_excel(project.config_file, index=False)

        k = args['websiteToDelete'][0]
        print('Website to delete = {}'.format(k))
        del_unit = rproject.get_unit_from_url(k)
        print('Del Unit = {}'.format(del_unit))
        del_link = {k:[v] for k, v in initial_links.items() if k == args['targetToDelete'][0]}
        internal_link = args['targetToDelete'][0].replace(args['websiteToDelete'][0], '')
        # should not happen, but as a measure of precaution
        if internal_link.startswith('/'):
            internal_link = internal_link[1:]
        base_dir_path = os.path.join(del_unit.download_path, internal_link)

        del_unit.remove_crawler_link(args['targetToDelete'][0])
        len_files, link_on_hd = erase_link_from_hd(args['targetToDelete'][0], base_dir_path)
        # If file was alone on directory, no need to keep directory, so delete it
        if len_files == 1:
            shutil.rmtree(base_dir_path)
            print('Directory \'{}\' successfully deleted on HD'.format(base_dir_path))
        else:
            print('File \'{}\' successfully deleted on HD'.format(link_on_hd))
            os.remove(link_on_hd)

        # if (rproject.delete_unit(args['websiteToDelete'][0])):
        #     print('Unit successfully deleted from hard drive')
        # reload units from excel
        rproject._load_units_from_data_path()
        # change session data to take account of deleted unit
        units = rproject.units_stats(units=rproject.filter_units())
        self.session['units'] = units
        # if units is None, it means project can be emptied
        if units is None:
            fname = os.path.join(self.application.data_dir, projectname)
            shutil.rmtree(fname)
            content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
            self.request_db.delete(content_to_delete)
            self.request_db.commit()
        else:
            # Update content (take first content with name projectname + '_default')
            df = pd.read_excel(project.config_file)
            links = dict(zip(df['target'], df['target_label']))
            links = {k:[v] for k, v in links.items()}
            
            content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
            alerts_to_delete = content_to_delete.alerts.all()
            for a in alerts_to_delete:
                # print('a.name = {}'.format(a.name))
                if a.alert_type != 'Live':
                    try:
                        # print('Deleting from redbeat non Live alert : {}'.format(a.name))
                        e = Entry.from_key('redbeat:'+a.name, app=continuous_worker.app)
                        e.delete()
                    except Exception as e:
                        print('[FAIL] Deleting from redbeat non Live alert : {}'.format(a.name))
                        print('Reason = {}'.format(e))
            if 'tasks' in self.session and 'live_view' in self.session['tasks']:
                # print('There is a live alert to be DELETED HERE : {}'.format(a.alert_type))
                try:
                    res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker\
                     in self.session['tasks']['live_view']])
                    # print('Deleting old live view tasks from session: OK !!!')
                except Exception as e:
                    print('[ERROR] Revoking live view tasks from session. /!\\ ERROR = {}'.format(e))
                del self.session['tasks']['live_view']
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

        # Make sure user does not mess up with url entries otherwise messes up with the crawler/downloader !!
        args['inputWebsite'][0], args['inputTarget'][0] = make_sure_entries_by_user_are_well_formated(\
            args['inputWebsite'][0], args['inputTarget'][0])
        
        if args['inputWebsite'][0] is False or args['inputTarget'][0] is False:
            flash_message(self, 'danger', 'Url(s) not properly formated.')
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return

        rproject = RProject(project.name, project.data_path, project.config_file)
        # print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df.copy()
        config_df_updated = config_df_updated[config_df_updated.target != args['inputTarget'][0]]
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
        new_link = {k:[v] for k, v in links.items() if k == args['inputTarget'][0]} # Make sur only one link is selected
        # Carreful: Need to keep all links here because new content has to be created !
        all_links = {k:[v] for k, v in links.items()}
        
        # TODO: Fix this: Here we are looping on all links whereas the edit view is only for ONE LINK !!! Not possible
        for k, v in all_links.copy().items():
            #print('K = {}, V = {} (type:{})'.format(k, v, type(v)))
            try:
                if math.isnan(v[0]):
                    all_links[k] = ''
                elif ';' in v[0]:
                    all_links[k] = v[0].split(';')
            except Exception as e:
                if ';' in v[0]:
                    all_links[k] = v[0].split(';')
                #print('Not NAN')

        # Need to download new link if it changes
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
        # print('links = {} (before stuff'.format(all_links))
        # flash_message(self, 'danger', 'NOPE !')
        # self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
        # return
        # TODO: Change crawler logfile with only the link that changed, not all of them !!
        # Or use generate crawl logfile and delete the old one !
        idx, url_errors = rproject.add_links_to_crawler_logfile(new_link)

        # print('IDX = {}, URL_ERRORS  ={}'.format(idx, url_errors))
        
        content_to_delete = project.contents.filter_by(name=(projectname + '_default')).first()
        alerts_to_delete = content_to_delete.alerts.all()
        for a in alerts_to_delete:
            # print('a.name = {}'.format(a.name))
            if a.alert_type != 'Live':
                try:
                    # print('Deleting from redbeat non Live alert : {}'.format(a.name))
                    e = Entry.from_key('redbeat:' + a.name, app=continuous_worker.app)
                    e.delete()
                except Exception as e:
                    print('[FAIL] Deleting from redbeat non Live alert : {}'.format(a.name))
                    print('Reason = {}'.format(e))
        if 'tasks' in self.session and 'live_view' in self.session['tasks']:
            # print('There is a live alert to be DELETED HERE : {}'.format(a.alert_type))
            try:
                res = revoke_all_tasks(live_view_worker_app, live_view, [worker['id'] for worker\
                 in self.session['tasks']['live_view']])
                # print('Deleting old live view tasks from session: OK !!!')
            except Exception as e:
                print('[ERROR] Revoking live view tasks from session. /!\\ ERROR = {}'.format(e))
            del self.session['tasks']['live_view']
        self.request_db.delete(content_to_delete)
        self.request_db.commit()

        mailing_list = dict(zip(df['target'], df['mailing_list']))
        new_content = Content(projectname + '_default', all_links, mailing_list)
        project.contents.append(new_content)
        self.request_db.commit()

        # change session data to take account of deleted unit
        rproject = RProject(project.name, project.data_path, project.config_file)
        units = rproject.units_stats(units=rproject.filter_units())
        self.session['units'] = units
        self.session.save()
        if url_errors != []:
            # Supposed to be only one error here, because one link (TODO: Check if problem there is)
            for err in url_errors:
                for k, v in err.items():
                    target_url = k
                    target_error = v
                    del_unit = rproject.get_unit_from_url(k)
                    del_unit.remove_crawler_link(k)

            flash_message(self, 'danger', 'Impossible to download provided target URL : {} (Reason: {})'.format(args['inputTarget'][0], target_error))
        else:
            flash_message(self, 'success', 'Successfully downloaded URL : {}'.format(args['inputTarget'][0]))
            # self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            # return
        self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
        return
