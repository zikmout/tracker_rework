import tornado
from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_url_from_id, get_celery_task_state
from tracker.models import User
from tracker.core.rproject import RProject
from tracker.workers.download_worker import download_website

class UserDownloadCreate(BaseView):
    SUPPORTED_METHOD = ['POST']
    def post(self, username, projectname, uid):
        # check if download already started
        task_exists = False
        if 'download' in self.session['tasks']:
            for task in self.session['tasks']['download']:
                if task['uid'] == uid:
                    task_exists = True
        if task_exists is False:
            #load user
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            # Loading project
            rproject = RProject(project.name, project.data_path, project.config_file)
            if len(self.session['project_config_file']) == 0:
                rproject._load_units_from_data_path()
            else:
                rproject._load_units_from_excel()
            url = get_url_from_id(self.session['units'], uid)
            list_url = list()
            list_url.append(url)
            print('URL = {}'.format(list_url))
            tasks = rproject.download_units(list_url)
            # in case of more scalability, download_units function is
            # ready to take more tasks at once, so it returns an array 
            task = tasks[0]

            if 'download' not in self.session['tasks']:
                self.session['tasks']['download'] = list()

            task_object = {
                'username': username,
                'projectname': projectname,
                'uid': uid,
                'url': url,
                'id': task.id
            }
            self.session['tasks']['download'].append(task_object)
            self.session.save()
            self.set_header('Location', '/api/v1/users/{}/projects/{}/download/{}'.format(self.session['username'], projectname, task.id))
        else:
            self.set_header('Location', 0)

    def delete(self, username, projectname, uid):
        print('Task to be deleted : {}'.format(uid))
        pass

class UserDownloadStatus(BaseView):
    SUPPORTED_METHODS = ['GET']
    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self, username, projectname, task_id):
        task = download_website.AsyncResult(task_id)
        print('Task backend = {}'.format(task.backend))
        #task = task.get()
        print('task_id: {}'.format(task_id))
        response = get_celery_task_state(task)
        self.write(response)

class UserDownloadStop(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    def post(self, username, projectname, uid):
        task_id = None
        if 'download' in self.session['tasks']:
            for task in self.session['tasks']['download']:
                if task['uid'] == uid:
                    task_id = task['id']
                    break;
        if task_id is not None:
            download_website.AsyncResult(task_id).revoke(terminate=True)
            idx = 0
            for task in self.session['tasks']['download']:
                if uid == task['uid']:
                    url = task['url']
                    self.session['tasks']['download'].pop(idx)
                    # Loading project to update session
                    user = self.request_db.query(User).filter_by(username=username).first()
                    project = user.projects.filter_by(name=projectname).first()
                    sbb_project = RProject(project.name, project.data_path, project.config_file)
                    updated_unit = sbb_project.update_unit(url)
                    self.session['units'][str(uid)]['downloaded_files'] = len(updated_unit._local_tree())
                    self.session.save()
                    flash_message(self, 'success', 'Download {} successfully canceled.'.format(url))
                    self.redirect('/api/v1/users/{}/projects/{}/download'.format(username, projectname))
                idx += 1
        else:
            flash_message(self, 'danger', 'There is no download to stop.')
            self.redirect('/api/v1/users/{}/projects/{}/download'.format(username, projectname))

class UserProjectDownloadView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'No units in the project {}.'.format(projectname))
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return
        else:
            self.render('projects/download.html', units=units)