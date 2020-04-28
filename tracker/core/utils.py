import os
import re
import datetime
import random
import time
import shutil
from tracker.utils import erase_link_from_hd
from tracker.core.user_agent_list import USER_AGENTS

def clean_link_from_hd(rproject, domain_link, full_link, initial_links):
    """ Delete an entire link under unit """
    del_unit = rproject.get_unit_from_url(domain_link)
    print('Del Unit = {}'.format(del_unit))
    del_link = {k:[v] for k, v in initial_links.items() if k == full_link}
    internal_link = full_link.replace(domain_link, '')
    # should not happen, but as a measure of precaution
    if internal_link.startswith('/'):
        internal_link = internal_link[1:]
    base_dir_path = os.path.join(del_unit.download_path, internal_link.rpartition('/')[0])
    filename = internal_link.rpartition('/')[2]

    print('\ninternal_link = {}'.format(internal_link))
    print('\nbase_dir_path = {}'.format(base_dir_path))
    print('\nfilename = {}'.format(filename))

    del_unit.remove_crawler_link(full_link)
    len_files, link_on_hd = erase_link_from_hd(full_link, base_dir_path, filename)

    # If file was alone on directory, no need to keep directory, so delete it
    # But if file could not be downloaded on HD, it does not exist so just notice the user in this case
    if len_files == 1:
        if not os.path.isdir(base_dir_path):
            print('[WARNING] Directory \'{}\' was supposed to exist and be deleted but was not found on HD ! '.format(base_dir_path))
        else:
            shutil.rmtree(base_dir_path)
            print('[SUCCESS] Directory \'{}\' successfully deleted on HD'.format(base_dir_path))
    else:
        if not os.path.isfile(link_on_hd):
            print('[WARNING] File \'{}\' was supposed to exist and be deleted but was not found on HD ! '.format(link_on_hd))
        else:
            os.remove(link_on_hd)
            print('File \'{}\' successfully deleted on HD'.format(link_on_hd))

def rh():
    """ Return a random header with random User-Agent """
    random.seed(time.time())
    random_nb = random.randint(0, len(USER_AGENTS) - 1)
    header = {'User-Agent': USER_AGENTS[random_nb]}
    return header

def ua():
    """ Return a random User-Agent """
    random.seed(time.time())
    random_nb = random.randint(0, len(USER_AGENTS) - 1)
    user_agent = USER_AGENTS[random_nb]
    return user_agent

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

def get_formated_units(units):
    """ Formats the remote_tree structure so that it can be used by hummingbird 
        see : https://github.com/hummingbird-dev/hummingbird-treeview
        args:
            units (Unit object): List of units to be formated
        return:
            d (dict): key = url, value = [formated_link, real_link]
    """
    d = {}
    for unit in units:
        links = unit._remote_tree()
        formated_links = _format_output_hummingbird(links)
        formated_unit = { unit.url : formated_links }
        d.update(formated_unit)
    return d

def _format_output_hummingbird(links):
    """ Function used by get_formated_units only
        Meant to format output for hummingbird treeview 
    """
    depth = 0
    full_link = []
    final_links = []
    def get_obj(d1, key):
        dd = d1
        keys = key.split('/')
        latest = keys.pop()
        for k in keys:
            dd = dd.setdefault(k, {})

    root_nodes = {}
    for _ in links:
        get_obj(root_nodes, _[1:])

    def go_depth_recursive(depth, full_link, final_links, d):
        for k, v in d.items():
            full_link.append(k)
            final_links.append(['-' * depth + k, '/'+'/'.join(full_link)])
            if '/'+'/'.join(full_link) in links:
                links.remove('/'+'/'.join(full_link))
            if isinstance(v, dict):
                depth += 1
                go_depth_recursive(depth, full_link, final_links, v)
            lst = [x for x in links if '/'+'/'.join(full_link) in x]
            if lst != []:
                for l in lst:
                    if l.count('/') > 1:
                        name = l.rpartition('/')[2]
                        if name != '':
                            final_links.append(['-' * depth + name, '/'+'/'.join(full_link) + '/' + name])
                    links.remove(l)
            depth -= 1
            full_link.pop()
            
    go_depth_recursive(depth, full_link, final_links, root_nodes)
    return final_links

def from_links_to_dict(links):
    # print('************************ LINKS ******************************************** \n')
    # print('links before = {}'.format(links))
    for k, v in links.copy().items():
        #print('k = {}'.format(k))
        if k.count('/') == 2 and not k.endswith('/'):
            #print('entered add')
            del links[k]
            links[k + '/'] = v
            # links[k] = links[k] + '/'
    # print('links after = {}'.format(links))
    domains = set()
    for link in links:
        splited = link.split('/', 3)
        first_part = re.search('((.*?\/.*?)){3}', link).group(0)
        domains.add(first_part[:-1])
    
    first_parts = dict()
    for domain in domains:
        first_parts[domain] = list()    

    for link, keywords in links.items():
        if keywords == '':
            keywords = []
        first = re.search('((.*?\/.*?)){3}', link).group(0)
        splited = link.split('/', 3)
        second = splited[3]
        first_parts[first[:-1]].append(['/' + second, keywords])
        # print('keyworDS = {}'.format(keywords))
    return first_parts

def is_valid_url(url):
    to_exclude = ['.xlsx', '.xls', '.m4a', 'vimeo.com', 'www.youtube', 'www.facebook', 'www.linkedin', 'www.instagram',\
    '.jpg', '.jpeg', '.png', '.wmv', '.ics', '.mp3', '.zip', '.rtf', '.mov', '.mp4', '.mpg',\
     '@', '.doc', '#', ';', 'amp%3B', '.gif', '.vcf', '.exe', '.xml', '&amp', '.tif', '.JPG', '.pptx', '.ppt']
    for _ in to_exclude:
        if _ in url or _.upper() in url:
            # print('Found {} IN {} : URL is NOT VALID'.format(_, url))
            return False
    return True

def is_valid_cleaned_content(cleaned_content, already_seen_content):
    if cleaned_content is None:
        return False
    if len(cleaned_content) == 0:
        return False
    if cleaned_content in already_seen_content:
        return False
    return True