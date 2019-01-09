import tornado
from pintell.views.base import BaseView
from pintell.utils import flash_message, login_required, get_url_from_id, get_celery_task_state
from pintell.models import User
from pintell.core.rproject import RProject
from pintell.workers.download_worker import download_website

class UserDownloadTaskCreate(BaseView):
    SUPPORTED_METHOD = ['POST']
    def post(self, username, projectname, uid):
        #load user
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        # Loading project
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
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
        self.set_header('Location', '/api/v1/users/{}/tasks/status/{}'.format(self.session['username'], task.id))

    def delete(self, username, projectname, uid):
        print('Task to be deleted : {}'.format(uid))
        pass

class UserDownloadTaskStatus(BaseView):
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