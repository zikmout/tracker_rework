import json
import string
import tornado
import math
import re
from celery.task.control import discard_all
from tracker.base import Session, Base, engine, meta

def check_valid_mail(email):  
    # Make a regular expression 
    # for validating an Email 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        return True
    else:  
        return False

def is_project_name_well_formated(projectname):
    if not all(x.isalnum() or x.isspace() or x == '_' for x in projectname):
        return False
    return True

def make_session_factory():
    # generate database schema  
    Base.metadata.create_all(engine)

    # create a new session
    session = Session()
    return session, meta

def flash_message(self, type, message):
    """ Flash messages to user:
        type correspond to twitter bootstrap alerts type:
        see : https://getbootstrap.com/docs/4.0/components/alerts/
        primary -> blue
        secondary -> grey
        success -> green
        danger -> red
        warning -> yellow
        info -> light blue
        light -> white      
        dark -> black
    """
    message = dict(type=type, message=message)
    self.set_secure_cookie("flash", tornado.escape.json_encode(message))

def login_required(f):
    def _wrapper(self, *args, **kwargs):
        logged = self.get_current_user()
        if logged is None:
            self.redirect('/api/v1/auth/login')
        else:
            ret = f(self, *args, **kwargs)
    return _wrapper

def admin_required(f):
    def _wrapper(self, *args, **kwargs):
        is_admin = self.session['is_admin']
        if is_admin is False:
            self.redirect('/api/v1/auth/login')
        else:
            ret = f(self, *args, **kwargs)
    return _wrapper

def get_url_from_id(units, uid):
    for _, details in units.items():
        if _ == uid:
            return details['url']
    return None

def get_id_from_url(units, url):
    for uid, details in units.items():
        if details['url'] == url:
            return uid
    return None

def json_response(status, data, message):
    """ return a well formated json object for JSON API responses """
    response = {
        "status": status,
        "data": data,
        "message": message
    }
    return json.dumps(response)

def get_celery_task_state(task):
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'url': '',
            'current': 0,
            'total': 1,
            'status': 'Pending ...'
        }
    elif task.info is not None and task.state != 'FAILURE':
        response = {
            'state': task.state,
            'url': task.info.get('url'),
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in background job
        response = {
            'state': task.state,
            'url': task.info.get('url'),
            'current': task.info.get('current', 1),
            'total': task.info.get('total', 1),
            'status': str(task.info)
        }
    #print('response : {}'.format(response))
    return response

def revoke_chain(last_result): 
    print('[CALLER] Revoking: {}'.format(last_result.task_id))
    last_result.revoke()
    if last_result.parent is not None:
        revoke_chain(last_result.parent)

def revoke_all_tasks(app, task_func, ids):
    res = 0
    task_ids_to_stop = list()

    for id in ids:
        #print('pass id')
        task_ids_to_stop.append(id)
        task = task_func.AsyncResult(id)
        revoke_chain(task)
    res = app.control.revoke(task_ids_to_stop, terminate=True, signal='SIGKILL')
    print('Purging task ids now ...')
    app.control.purge()
    discard_all()
    print('\nAll task ids succesfully purged and discarded.')
    return res

def replace_mix_option_with_all_existing_keywords(links):
    all_words = set()
    if '<MIX>' in list(links.values()):
        # create set of all keywords
        for key_word in list(links.values()):
            if key_word != '<MIX>':
                if ';' in key_word:
                    for _ in key_word.split(';'):
                        all_words.add(_)
                        # not case sensitive
                        #all_words.add(_.upper())
                        #all_words.add(_.lower())
                else:
                    #print('key word = {}'.format(key_word))
                    # Add condition for l'Oréal
                    if key_word not in ['le', 'la', 'les', 'du', 'au', 'de', 'des']:
                        all_words.add(key_word)
                    # not case sensitive
                    #all_words.add(key_word.upper())
                    #all_words.add(key_word.lower())
        # if <MIX> in the column, apply all key words matching
        for k, v in links.copy().items():
            if v == '<MIX>':
                links[k] = list(all_words)
            else:
                links[k] = [v]
    else:
        links = {k:[v] for k, v in links.items()}
    for k, v in links.copy().items():
        if isinstance(v[0], float) and math.isnan(v[0]):
            links[k] = [];
        elif len(v) == 1 and ';' in v[0]:
            links[k] = v[0].split(';')
    return links

def highlight_keywords(keywords, content):
    for kw in keywords:
        regx = re.compile('{}'.format(kw), re.I)
        ret = regx.findall(content)
        if isinstance(ret, list) and ret != []:
            if len(ret) > 1:
                for r in ret:
                    content = content.replace(r, '<mark>{}</mark>'.format(r))
            else:
                content = content.replace(ret[0], '<mark>{}</mark>'.format(ret[0]))
                break;
    return content

def format_all_nearest_links(input_dict, base_url):
    
    output_dict = dict()
    
    if input_dict is None:
        return None
    
    for k, v in input_dict.items():
        print('k = {}, v = {}'.format(k, v))
        if k != '\n' and k != '' and v is not None:
            t = str.maketrans('\n', ' ')
            l = k.translate(t)
            t = str.maketrans('\t', ' ')
            l = l.translate(t)
            t = str.maketrans('\r', ' ')
            l = l.translate(t)
            l = ' '.join(l.split())
            m = v
            if not v.startswith('http'):
                if v.startswith('//'):
                    m = 'http:' + v
                elif v.startswith('/'):
                    m = base_url + v
            output_dict[l] = m
    return output_dict

def trim_text(key):
    if key != '\n' and key != '':
        t = str.maketrans('\n', ' ')
        l = key.translate(t)
        t = str.maketrans('\t', ' ')
        l = l.translate(t)
        t = str.maketrans('\r', ' ')
        l = l.translate(t)
        l = ' '.join(l.split())
        return l
    else:
        return ''