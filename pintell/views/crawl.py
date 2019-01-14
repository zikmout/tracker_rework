import tornado
from pintell.views.base import BaseView
from pintell.utils import flash_message, login_required
from pintell.workers.download_worker import download_website


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