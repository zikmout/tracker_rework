import tornado
import time
from pintell.views.base import BaseView
from pintell.utils import flash_message, login_required, get_url_from_id, get_id_from_url
from pintell.workers.crawl_worker import link_crawler
from pintell.models import User
from pintell.core.rproject import RProject


class UserProjectCrawlView(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname):
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.render('projects/crawl.html', units=units)

class UserCrawlsCreate(BaseView):
    @login_required
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        units_url_to_crawl = dict()
        for _ in list(args):
            if 'selectedCheck' in _:
                uid = _.replace('selectedCheck', '')
                url = get_url_from_id(self.session['units'], uid)
                if args['startPath' + uid] == '':
                    starting_path = '/'
                else:
                    starting_path = args['startPath' + uid]
                if args['depth' + uid] == '':
                    depth = 8
                else:
                    depth = args['depth' + uid]
                unit_dict = { 
                    url : {
                        'starting_path': starting_path,
                        'depth': depth 
                    }
                }
                units_url_to_crawl.update(unit_dict)
                print('Selected uid to crawl : {}'.format(url))
                print('Start path : {}'.format(starting_path))
        # launch project
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        # crawl selected units form selected path
        # maybe check here if session units is consistent with rproject units
        tasks = rproject.crawl_units(units_url_to_crawl)
        print('tasks =** : {}'.format(tasks))
        print('LAUNCHED TASKS !!! => {}'.format(tasks))
        # save tasks in session
        units = self.session['units'].copy()
        for url, task in tasks.items():
            print('task_url = {}'.format(url))
            print('uid = {}'.format(uid))
            uid = get_id_from_url(units, url)
            if task is not None:
                self.session['units'][uid]['task'] = task.id
        self.session.save()
        self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))

class UserCrawlStop(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname, task_id):
        print('DEMAND STOP TASQ : {}'.format(task_id))

        task = link_crawler.AsyncResult(task_id)
        link_crawler.AsyncResult(task_id).revoke(terminate=True)
        copy_session = self.session.copy()
        for uid, details in self.session['units'].items():
            if 'task' in details and details['task'] == task_id:
                del self.session['units'][str(uid)]['task']
                self.session.save()
                flash_message(self, 'success', 'Task_id {} was found and has been successfuly stopped.'.format(task_id))
                self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))







