import tornado
from pintell.views.base import BaseView
from pintell.utils import flash_message, login_required, get_url_from_id
from pintell.workers.download_worker import download_website
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
        print('post args = {}'.format(args))
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
        print('LAUNCHED TASKS !!! => {}'.format(tasks))
