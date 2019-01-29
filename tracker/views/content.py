import tornado
from math import isnan
from tracker.views.base import BaseView
from tracker.models import User, Content
from tracker.utils import flash_message, login_required, json_response
from tracker.core.rproject import RProject
from tracker.core.unit import Unit
from tracker.core.utils import get_formated_units
from tracker.core.loader import get_df_from_excel

class UserProjectContent(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        # rproject = RProject(project.name, project.data_path, project.config_file)
        # rproject._load_units_from_data_path()
        # formated_units = get_formated_units(rproject.units)
        # for now, formated_units is desactivated because loading is too big
        formated_units = {}
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
            # need to change following line too according to PickleType
            # Try with this new_dict
            #new_dict = dict()
            #for link in data['links']:
            #    new_dict.append(link : [])
            #new_content = Content(data['name'], new_dict)
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

class UserProjectContentFromFile(BaseView):
    SUPPORTED_METHODS = ['POST']
    def post(self, username, projectname):
        args = { k: self.get_argument(k) for k in self.request.arguments }
        print('Received args = {}'.format(args))
        add_stranger = False
        if 'addStrangerChecked' in args:
            add_stranger = True
        if args['fileNamePath'] == '':
            file_path = self.session['project_config_file']
        else:
            file_path = args['fileNamePath']
        
        try:
            df_links = get_df_from_excel(file_path)
            links = dict(zip(df_links[args['columnLinkName']], df_links[args['columnKeyWordName']]))
            #print('links from excel file = {}\n'.format(links))
            #print('list(links.values()) = {}'.format(list(links.values())))
            # if mixed set to True, links with label '<MIX>' are taking all tags of the list
            # temporary solution, does not really make sense yet
            all_words = set()
            if '<MIX>' in list(links.values()):
                # create set of all keywords
                for key_word in list(links.values()):
                    if key_word != '<MIX>':
                        #print('key word = {}'.format(key_word))
                        all_words.add(key_word)
                        # not case sensitive
                        all_words.add(key_word.upper())
                        all_words.add(key_word.lower())
                # if <MIX> in the column, apply all key words matching
                for k, v in links.copy().items():
                    if v == '<MIX>':
                        links[k] = list(all_words)
                    else:
                        links[k] = [v]
            # can save space here
            else:
                links = {k:[v] for k, v in links.items()}
            print('Link big dict = {}\n'.format(links))
            #print('Set of all_words = {}\n'.format(all_words))
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()

            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject._load_units_from_data_path()
            idx = rproject.add_links_to_crawler_logfile(list(links))
            print('{}/{} links needed to be added to logfile.'.format(idx, len(links)))

            new_content = Content(args['inputName'], links)
            project.contents.append(new_content)
            self.request_db.add(project)
            self.request_db.commit()
            flash_message(self, 'success', 'Content {} successfully created.'.format(args['inputName']))
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))
        except Exception as e:
            print('ERROR -> {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(args['inputName']))
            self.redirect('/api/v1/users/{}/projects/{}/alerts'.format(username, projectname))


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
