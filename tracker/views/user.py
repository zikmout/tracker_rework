from tornado import gen
import json
from tracker.views.base import BaseView
from tracker.models import User
from tracker.utils import flash_message, login_required, get_url_from_id
from tracker.models import User, Role
from tracker.core.rproject import RProject
import tracker.workers.continuous.continuous_worker as continuous_worker
from redbeat import RedBeatSchedulerEntry as Entry

class UserListView(BaseView):
    """View for reading and adding new roles."""
    SUPPORTED_METHODS = ['GET']
    @login_required
    @gen.coroutine
    def get(self):
        """Get all tasks for an existing user."""
        db_users = self.request_db.query(User).all()
        users_json = []
        for user in db_users:
            users_json.append({
                "username": user.username,
                "registration_date": user.registration_date,
                "email": user.email,
                "role": user.get_rolename()
                })
        self.render('admin/list_users.html', users_json=users_json)

class AdminProjectsView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    @gen.coroutine
    def get(self):
        """Get all tasks for an existing user."""
        db_users = self.request_db.query(User).all()
        users_all_json = []
        users_json = []
        
        for user in db_users:
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
            users_all_json.append({user.username:user_projects_json})

        self.render('admin/list-projects.html', users_json=users_all_json)

class UserDelete(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username):
        user = self.request_db.query(User).filter_by(username=username).first()
        if user:
            try:
                self.request_db.delete(user)
                self.request_db.commit()
                flash_message(self, 'success', 'User {} succesfully deleted.'.format(username))
            except Exception as e:
                flash_message(self, 'success', 'Impossible to delete user. Check shell logs for more information.')
                print('Exception : Impossible to delete user because : {}'.format(e))
        else:
            flash_message(self, 'danger', 'Username {} not found. Delete aborded.'.format(username))
        self.redirect('/api/v1/users_list')

class UserUnitView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    @gen.coroutine
    def get(self, username, projectname, uid):
        url = get_url_from_id(self.session['units'], uid)
        self.render('unit/index.html', url=url)

class UserUnitEditView(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        # print('FORM DATA EDIT = {}'.format(self.form_data))
        url = self.form_data['editUnitName'][0] ####

        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()

        rproject = RProject(project.name, project.data_path, project.config_file)
        # print('config df before = {}'.format(rproject.config_df))
        config_df_updated = rproject.config_df.copy()
        #config_df_updated.loc[config_df_updated['target'] == url, 'target_label'] = 'test;key;words'
        # line = {'Name': config_df_updated.loc[config_df_updated['target'] == url, 'Name'], 'Website': args['inputWebsite'][0],\
            # 'target': args['inputTarget'][0], 'target_label':args['inputKeywords'][0]}
        keys = ['Name', 'Website', 'target', 'target_label', 'mailing_list']
        # print('keywords = ->{}<-'.format(config_df_updated[config_df_updated['target'] == url]['target_label'].item()))
        line = {k:config_df_updated[config_df_updated['target'] == url][k].item() for k in keys}
        if not isinstance(line['target_label'], float):
            line['target_label'] = line['target_label'].split(';')
        else:
            line['target_label'] = ''
        if not isinstance(line['mailing_list'], float):
            line['mailing_list'] = line['mailing_list'].split(';')
        else:
            line['mailing_list'] = ''
        # print('mailing_list = {}'.format(line['mailing_list']))
        # print('project config file : {}'.format(project.config_file))
        config_df_updated.to_excel(project.config_file, index=False)
        #line = config_df_updated.loc[config_df_updated['target'] == url].to_json()
        self.render('unit/edit.html', url=url, line=line)

class AdminUserCreate(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self):
        args = self.form_data
        # print('Args = {}'.format(args))
        if 'inputUpdatedRole' in args and 'inputUsername' in args:
            try:
                user = self.request_db.query(User).filter_by(username=args['inputUsername'][0]).first()
                user.role = self.request_db.query(Role).filter_by(name=args['inputUpdatedRole'][0]).first()
                self.request_db.commit()
                flash_message(self, 'success', 'User {} : Permission succesfully updated to {}.'\
                    .format(args['inputUsername'][0], args['inputUpdatedRole'][0]))
            except Exception as e:
                print('Exception updating user role : {}'.format(e))
                flash_message(self, 'danger', 'Failed changing permission for user: {}.'\
                .format(args['inputUsername'][0]))
        else:
            try:
                user = User(args['inputUsername'][0], args['inputPassword'][0], args['inputEmail'][0], \
                    self.request_db, self.meta, role=self.request_db.query(Role).filter_by(name=args['inputRole'][0]).first())
                self.request_db.add(user)
                self.request_db.commit()
                flash_message(self, 'success', 'User {} succesfully registered.'.format(args['inputUsername'][0]))
            except Exception as e:
                print('Exception : {}'.format(e))
                flash_message(self, 'danger', 'Username {} already exists or email {} already taken.'\
                    .format(args['inputUsername'][0], args['inputEmail'][0]))
        self.redirect('/api/v1/users_list')