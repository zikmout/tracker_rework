import tornado
from pintell.views.base import BaseView
from pintell.models import User, Content
from pintell.utils import flash_message, login_required, json_response
from pintell.core.rproject import RProject
from pintell.core.unit import Unit
from pintell.core.utils import get_formated_units

class UserProjectContent(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
        formated_units = get_formated_units(rproject.units)
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'There are no units in the project {}. Or filtered units are 0.'.format(project.name))
            self.redirect('/api/v1/users/{}/projects_manage'.format(self.session['username']))
        else:
            self.render('projects/content/index.html', formated_units=formated_units)

    @login_required
    def post(self, username, projectname):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        data = tornado.escape.json_decode(self.request.body)
        print('POST received, links are = {}'.format(data))
        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            new_content = Content(data['name'], data['links'])
            project.contents.append(new_content)
            self.request_db.add(project)
            self.request_db.commit()
            flash_message(self, 'success', 'Content {} successfully created.'.format(data['name']))
            self.write(json_response('success', None, 'Content succesfully created.'))
        except Exception as e:
            print('Error recording content in DB : {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(data['name']))
            self.write(json_response('error', None, '{}'.format(e)))

class TestingView(BaseView):
    SUPPORTED_METHODS = ['GET']
    def get(self, username, projectname):
        self.write(username)
        self.write(projectname)
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        rproject = RProject(project.name, project.data_path, project.config_file)
        rproject._load_units_from_data_path()
        print('begin crawling')
        #unit = Unit(rproject.data_path, 'https://www.rsagroup.com')
        #unit.crawl(max_depth=8)
        print('-> DONE CRAWLING')
