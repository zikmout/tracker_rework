import os
import re
import datetime
import random
import time
from pintell.core.user_agent_list import USER_AGENTS

def rh():
    """ Return a random header with random User-Agent """
    random.seed(time.time())
    random_nb = random.randint(0, len(USER_AGENTS) - 1)
    header = {'User-Agent': USER_AGENTS[random_nb]}
    return header

def print_links(links):
    """ Print a list """
    for link in links:
        print(link)

def walktree_dir(input_path):
    """ Gets full path of all directories on specified directory
        arg:
            input_path (str): Directory where to look for directories
        return:
            r (list): List of all directories found
    """
    r = []
    for path, dname, fname in os.walk(input_path):
        r.extend([os.path.join(path, x).replace(input_path, '') for x in dname])
    return r

def walktree_files(input_path):
    """ Get full path of all files on specified directory
        arg:
            input_path (str): Directory where to look for files
        return:
            r (list): List of all files found
    """
    r = []
    to_exclude = ['.DS_Store']
    for path, dname, fname in os.walk(input_path):
        r.extend([os.path.join(path, x).replace(input_path, '') for x in fname if x not in to_exclude])
    return r

def clean_local_tree(local_tree):
    """ Cleans the local arborescence which has been found locally.
        Since the only difference between local files names and remote files
        are 'unknown__' named files and files names ending with '___', function
        gets rid of these files.
        arg:
            local_tree (list): List of links found locally
        return:
            local_tree (list): List of links found locally cleaned
    """
    return [x[:-10] if x.endswith('unknown___') else x[:-3] if x.endswith('___') else x for x in local_tree]

def find_internal_links(lines):
    """ Get rid of <PDF>, <EXCEL> tags in logfile links.
        arg:
            lines (list): List of links (e.g. '<PDF> /link/to/path')
        return:
            r (list) : List of links cleaned (e.g. '/link/to/path')
    """
    regex_internal_links = r"(\/.*)"
    r = [re.findall(regex_internal_links, x)[0] for x in lines]
    return r

def find_internal_link(line):
    """ Get rid of <PDF>, <EXCEL> tags in logfile links.
        arg:
            line (str): Link to clean (e.g. '<PDF> /link/to/path')
        return:
            r (str) : Cleaned link (e.g. '/link/to/path')
    """
    regex_internal_links = r"(\/.*)"
    r = re.findall(regex_internal_links, line)
    return r[0]

def print_lines(df_stocks):
    """ Quick and dirty function to make some stats on .xlsx config file
        arg:
            df_stocks (pd.DataFrame): input dataframe load from .xslx file
    """
    ok = 0
    trap = 0
    error = 0
    mp = 0
    for index, rows in df_stocks.iterrows():
        res = rows['Result Clean']
        print('Name : {}, Result : {}\n'.format(rows['Name'], res))

        if res == 'trap':
            trap += 1
        elif res == 'ok':
            ok += 1
        elif res == 'error':
            error += 1
        elif res == 'marche pas':
            mp += 1

    print('Traps = {}\n'.format(trap))
    print('Ok = {}\n'.format(ok))
    print('Errors = {}\n'.format(error))
    print('Marche pas = {}\n'.format(mp))
    print('TOTAL = {}\n'.format(mp + error + ok + trap))

def convert_filenametime_to_logfilename_time(logtime):
    ''' input has to be formated %Y%m%d%H%M
        output will be formated %Y%m%d%H%M '''
    datetime_object = datetime.datetime.strptime(logtime, '%Y%m%d%H%M')
    return datetime_object.strftime("%Y-%m-%d %H:%M")

def get_directories_list(path):
    """ Get a list o all directories in path provided
        arg:
            path (str): Path where to look for directories
        return:
            dirs (list): List of all directories found
    """
    dirs = os.listdir(path)
    dirs = [file for file in dirs if os.path.isdir(os.path.join(path, file))]
    return dirs