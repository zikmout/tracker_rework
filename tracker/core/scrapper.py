import urllib
import urllib.request
import ssl
import time
import requests
# from socket import timeout

def get_url_content(url, header, verbose=True):
    """ Open remote website content
        args:
            url (str): Full url of remote content to access
            header (dict): Header to use when accessing content
        return:
            remote_content: Binary content decoded
    """
    error = None
    # Faking User-Agent to avoid forbidden requests
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=gcontext) as response: # TODO: Handle timeout errors
            if verbose:
                print('[{}] {}\n'.format(response.getcode(), url))
            remote_content = response.read().decode('utf-8')
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError,\
        UnicodeDecodeError, TimeoutError) as e:
            remote_content = None
            msg = '{}'.format(e)
            error = { url: msg }
            print('ERROR : url = {}, message => {}'.format(url, msg))
    return remote_content, error

def get_local_content(path, mode):
    """ Open local file content
        args:
            path (str): Full path of file to open
            mode (str): Mode of file opening (e.g. 'rb')
        return:
            local_content: Binary content decoded
    """
    try:
        fd = open(path, mode)
        local_content = fd.read().decode('utf-8')
        fd.close()
        return local_content
    except Exception as e:
        print('Problem reading local content : {}'.format(e))
        return None


def get_robots_parser(robots_url):
    response = get_url_robots(robots_url)
    '''
    response = [x for x in response if 'Disallow:' in x]
    response = [x.replace('Disallow: ', '') for x in response]
    response = [x for x in response if x.count('/') > 1]
    '''
    return response

def try_reach_url(url, header):
    logs = dict()
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=gcontext) as response:
            print('[{}] {}\n'.format(response.getcode(), url))
            logs.update({url: 'OK'})
    except urllib.error.HTTPError as e:
        if hasattr(e,'code'):
            print('[{}] UNABLE TO REACH URL : {}\n'.format(e.code, url))
        if hasattr(e,'reason'):
            print('Reason : {}\n'.format(e.reason))
        logs.update({url:e.reason})
    except urllib.error.URLError as e:
        print('Reason : {}\n'.format(e.reason))
        logs.update({url:e.reason})
    return logs

def get_url_robots(url, header):
    req = urllib.request.Request(url, data=None, headers=header)
    # Faking SSL certificate to avoid unauthorized requests
    gcontext = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=gcontext) as response:
            print('[{}] {}\n'.format(response.getcode(), url))
            return response.read().decode('utf-8')#.split('\n')
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
            return None