import tornado
from pintell.views import BaseView
from pintell.utils import flash_message, login_required, get_url_from_id
from pintell.models import User
from pintell.core.rproject import RProject

class UserDownloadTaskCreate(BaseView):
    SUPPORTED_METHOD = ['POST']
    def post(self, username, projectname, uid):
        #load user
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        # Loading project
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
        url = list()
        url.append(get_url_from_id(self.session['units'], uid))
        print('URL = {}'.format(url))
        tasks = rproject.download_units(url)
        task = tasks[0]
        #task = download.apply_async((username, projectname, uid, url, rproject))

        if 'download' not in self.session['tasks']:
            self.session['tasks']['download'] = dict()

        task_object = {
            'username': username,
            'projectname': projectname,
            'uid': uid,
            'url': url
        }
        self.session['tasks']['download'].update(task_object)
        self.session.save()
        self.set_header('Location', '/api/v1/users/{}/tasks/status/{}'.format(self.session['username'], task.id))