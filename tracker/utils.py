import tornado
import json
from celery.task.control import discard_all
from tracker.base import Session, Base, engine, meta

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
            'current': 0,
            'total': 1,
            'status': 'Pending ...'
        }
    elif task.info is not None and task.state != 'FAILURE':
        response = {
            'state': task.state,
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
            'current': 1,
            'total': 1,
            'status': str(task.info)
        }
    print('response : {}'.format(response))
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
        task_ids_to_stop.append(id)
        task = task_func.AsyncResult(id)
        revoke_chain(task)
    res = app.control.revoke(task_ids_to_stop)
    print('Purging task ids now ...')
    app.control.purge()
    discard_all()
    print('\nAll task ids succesfully purged and discarded.')
    return res