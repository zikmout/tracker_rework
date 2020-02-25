import tornado
from tornado import gen
from math import isnan
import json
import time
from tracker.views.base import BaseView
from tracker.models import User, Content
from tracker.utils import flash_message, login_required, json_response
from tracker.core.rproject import RProject
from tracker.core.unit import Unit
from tracker.core.utils import get_formated_units
from tracker.utils import replace_mix_option_with_all_existing_keywords
from tracker.core.loader import get_df_from_excel

class UserProjectDeleteContent(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        content_to_delete = project.contents.filter_by(id=int(self.args['contentIdToDelete'])).first()
        self.request_db.delete(content_to_delete)
        self.request_db.commit()
        flash_message(self, 'success', 'Spider \'{}\' successfuly deleted.'.format(content_to_delete.name))
        self.redirect('/api/v1/users/{}/projects/{}/spider'.format(username, projectname))

class UserProjectContent(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    @gen.coroutine
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
            flash_message(self, 'danger', 'No source in watchlist {}.'.format(projectname))
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return
        else:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            contents = project.contents.all()
            json_contents = [_.as_dict() for _ in contents]
            self.render('projects/content/index.html', formated_units=formated_units, contents=json_contents)

    @login_required
    @gen.coroutine
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


class UserProjectSpider(BaseView):
    SUPPORTED_METHODS = ['GET', 'POST']
    @login_required
    @gen.coroutine
    def get(self, username, projectname):
        user = self.request_db.query(User).filter_by(username=username).first()
        project = user.projects.filter_by(name=projectname).first()
        json_project = project.as_dict()
        # rproject = RProject(project.name, project.data_path, project.config_file)
        # rproject._load_units_from_data_path()
        # formated_units = get_formated_units(rproject.units)
        # for now, formated_units is desactivated because loading is too big
        formated_units = {}
        if 'units' in self.session:
            units = self.session['units']
        if units is None or units == {}:
            flash_message(self, 'danger', 'No sources in watchlist {}.'.format(projectname))
            self.redirect('/api/v1/users/{}/projects/{}/websites-manage'.format(username, projectname))
            return
        else:
            try:
                rproject = RProject(project.name, project.data_path, project.config_file)
                rproject._load_units_from_excel()
                rproject._load_tracking_config_excel()
                # print('LINES ====== {}'.format(rproject.lines))
            #units = rproject.units_stats(units=rproject.filter_units())
            except Exception as e:
                print('[ERROR] UserProjectSpider : {}'.format(e))
                flash_message(self, 'danger', 'Problem while loading watchlist {}. Check DB.'.format(project.name))
                self.redirect('/api/v1/users/{}/projects-manage'.format(self.session['username']))
                return
            contents = project.contents.all()
            json_contents = [_.as_dict() for _ in contents]
            
            self.render('projects/content/spider.html', formated_units=formated_units, contents=json_contents,\
                project=json_project, lines=[_ for _ in rproject.lines.copy() if not isinstance(_['name'], float)])

    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        
        print('POST received, links are = {}'.format(self.args))
        
        content = json.loads(self.args['content'])
        links = dict()
        for obj in content:
            links[obj['target']] = obj['keywords']

        
        mailing_list = dict()
        for obj in content:
            mailing_list[obj['target']] = obj['mailing_list']
        # mails_set = set()
        # for c in content:
        #     print('M = >> {}'.format(c))
        #     if c['mailing_list'] == '':
        #         continue;
        #     else:
        #         for s in c['mailing_list']:
        #             mails_set.add(s)

        # mails_content = dict()
        # for mail in mails_set:
        #     mails_content[mail] = list()

        # for c in content:
        #     for mail in mails_set:
        #         if c['mailing_list'] != '' and mail in c['mailing_list']:
        #             mails_content[mail].append(c['target'])

        # print('mails after = {}'.format(mails_content))
        # print('\nlinks after : {}'.format(links))
        # print('SPIDER NAME = {}'.format(self.args['spidername']))
        # self.write(json_response('error', None, '{}'.format(e)))
        try:
            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()
            new_content = Content(self.args['spidername'], links, mailing_list)
            project.contents.append(new_content)
            self.request_db.add(project)
            self.request_db.commit()
            flash_message(self, 'success', 'Spider {} successfully created.'.format(self.args['spidername']))
            self.write(json.dumps({'message' : 'OK'}))
        except Exception as e:
            print('Error recording spider in DB : {}'.format(e))
            flash_message(self, 'danger', 'Spider {} failed. Check DB.'.format(self.args['spidername']))
            self.write(json.dumps({'message' : '{}'.format(e)}))


class UserProjectContentFromFile(BaseView):
    SUPPORTED_METHODS = ['POST']
    @login_required
    @gen.coroutine
    def post(self, username, projectname):
        """
        When recording Content, this is how links and mailing_list look like ^^
        links : {'https://www.iliad.fr/fr/finances/2019': ['transactions sur actions propres'], \
        'https://www.schneider-electric.com/en/about-us/investor-relations/regulatory-information/share-buyback.jsp': \
        ['trading in own shares'], 'https://divitarot.com/fr/resultat.php': ['je'], ...}

        mailing_list : {'https://www.iliad.fr/fr/finances/2019': 'simon@electricity.ai',\
        'https://www.schneider-electric.com/en/about-us/investor-relations/regulatory-information/share-buyback.jsp': nan,\
        'https://divitarot.com/fr/resultat.php': 'simon@electricity.ai;sicsim64@gmail.com',\
        'https://www.thalesgroup.com/fr/investor/publications/publications-et-communiques': 'simon@electricity.ai',\
        'https://www.loreal-finance.com/fr/operation-titres-declarations-programme-rachats-actions': 'simon@electricity.ai',\
        'http://www.spie.com/en/finance/regulated-information': 'simon@electricity.ai'}
        """
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
            # if mixed set to True, links with label '<MIX>' are taking all tags of the list
            # temporary solution, does not really make sense yet
            links = replace_mix_option_with_all_existing_keywords(links)

            user = self.request_db.query(User).filter_by(username=username).first()
            project = user.projects.filter_by(name=projectname).first()

            rproject = RProject(project.name, project.data_path, project.config_file)
            rproject._load_units_from_data_path()
            idx = rproject.add_links_to_crawler_logfile(list(links), wait=add_stranger)
            #print('{}/{} links needed to be added to logfile.'.format(idx, len(links)))
            mailing_list = None
            if 'columnMailingListName' in args and args['columnMailingListName'] != '':
                mailing_list = dict(zip(df_links[args['columnLinkName']], df_links[args['columnMailingListName']]))
            new_content = Content(args['inputName'], links, mailing_list)
            project.contents.append(new_content)
            self.request_db.add(project)
            self.request_db.commit()
            flash_message(self, 'success', 'Content {} successfully created.({}/{} links needed to crawled)'.format(args['inputName'], idx, len(links)))
            self.redirect('/api/v1/users/{}/projects/{}/spider'.format(username, projectname))
        except Exception as e:
            print('ERROR -> {}'.format(e))
            flash_message(self, 'danger', 'Content {} failed. Check DB.'.format(args['inputName']))
            self.redirect('/api/v1/users/{}/projects/{}/spider'.format(username, projectname))

