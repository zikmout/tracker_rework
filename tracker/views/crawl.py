import os
import tornado
import time
from tracker.views.base import BaseView
from tracker.utils import flash_message, login_required, get_url_from_id, get_id_from_url
from tracker.workers.crawl_worker import link_crawler
from tracker.models import User
from tracker.core.rproject import RProject


class UserProjectCrawlView(BaseView):
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
            nb_crawled = 0
            nb_units = 0
            total_crawled = 0
            for k, v in self.session['units'].items():
                nb_units += 1
                if 'task' in v and self.session['units'][k]['task'] != '':
                    nb_crawled += 1
                if self.session['units'][k]['is_base_crawled'] == True:
                    total_crawled += 1
            self.render('projects/crawl.html', units=units, nb_crawled=nb_crawled, 
                nb_units=nb_units, total_crawled=total_crawled)

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
                    print('DEPTH FOUND == {}'.format(args['depth' + uid]))
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
        # load only needed units
        rproject.load_units_from_list(list(units_url_to_crawl))
        # crawl selected units form selected path
        tasks = rproject.crawl_units(units_url_to_crawl)
        print('Launched task = {}'.format(tasks))
        # save tasks in session
        for url, task in tasks.items():
            uid = get_id_from_url(self.session['units'].copy(), url)
            if task is not None:
                self.session['units'][uid]['task'] = task.id
        self.session.save()
        self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))

class UserCrawlStop(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname, task_id):
        if task_id == 'all':
            print('STOPPING ALL TASKS')
            for uid, details in self.session['units'].items():
                if 'task' in details:
                    link_crawler.AsyncResult(details['task']).revoke(terminate=True)
                    del self.session['units'][str(uid)]['task']
            self.session.save()
            flash_message(self, 'success', 'All tasks have been successfuly stopped.')
            self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))
        else:
            print('STOPPING ONE TASK')
            link_crawler.AsyncResult(task_id).revoke(terminate=True)
            for uid, details in self.session['units'].items():
                if 'task' in details and details['task'] == task_id:
                    del self.session['units'][str(uid)]['task']
                    self.session.save()
                    flash_message(self, 'success', 'Task_id {} was found and has been successfuly stopped.'.format(task_id))
                    self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))


class UserCrawlDeleteLogfile(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname, uid):
        units = self.session['units'].copy()
        url = get_url_from_id(units, uid)
        domain = url.split('//')[-1].split('/')[0]
        logfile = os.path.join(self.session['project_data_path'], self.session['current_project'],\
            domain, domain + '.txt')
        os.remove(logfile)
        self.session['units'][str(uid)]['is_base_crawled'] = False
        self.session['units'][str(uid)]['duration'] = 0
        self.session['units'][str(uid)]['total'] = 0
        self.session['units'][str(uid)]['pages'] = 0
        self.session['units'][str(uid)]['pdfs'] = 0
        self.session['units'][str(uid)]['excels'] = 0
        self.session['units'][str(uid)]['errors'] = 0
        self.session.save()
        flash_message(self, 'success', 'Logfile {} was found and has been successfuly deleted.'.format(logfile))
        self.redirect('/api/v1/users/{}/projects/{}/crawl'.format(username, projectname))

class DeleteCrawlTaskFromSession(BaseView):
    SUPPORTED_METHODS = ['GET']
    @login_required
    def get(self, username, projectname, uid):
        # maybe change the command here to delete task from queue
        # because task should be already terminated
        try:
            task_id = self.session['units'][str(uid)]['task']
            link_crawler.AsyncResult(task_id).revoke(terminate=True)

            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            rproject = RProject(project.name, project.data_path, project.config_file)
            # load only needed units and update session
            rproject.load_units_from_list([self.session['units'][str(uid)]['url']])
            unit_session = rproject.units_stats()[1]
            self.session['units'][str(uid)] = unit_session
            self.session.save()
        except Exception:
            pass


