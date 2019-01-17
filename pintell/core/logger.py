import os
import datetime
import random
import time
import pandas as pd
import re
import pintell.core.scrapper as scrapper

def save_urls(logfile, pages, files, log_debut, log_fin):
    """ Saves freshly crawled links in the logfile
        args:
            logfile (str): Full path of logfile where to record logs
            pages (list): List of crawled html pages
            files (list): List of crawled Excel and pdf files
            log_debut (str): First line of logfile (e.g. '[2018-12-07 15:09] https://www.airliquide.com')
            log_fin (str): Last line of logfile
    """
    # check if urls have been already crawled and logfile exists
    if os.path.isfile(logfile):
        print('A file named {} already exists !\n'.format(logfile))
        return
    # Creates new logfile with all informations above
    fd = open(logfile, 'w+')
    fd.write(log_debut)
    fd.write('\n')
    for link in (pages + files):
        fd.write(link)
        fd.write('\n')
    fd.write(log_fin)
    fd.close()

def get_logfilename_dirname_path(filename):
    logfilename = filename + '_logs.txt'
    dirname_path = os.getcwd() + '/data/' + filename + '/'
    return logfilename, dirname_path

def save_robots(rp, filename, url):
    to_exclude = ['aholddelhaize']
    if url in to_exclude:
        return None
    logfilename, dirname_path = get_logfilename_dirname_path(filename)
    robots_path = dirname_path + url.split('//')[-1].split('/')[0] + '_robots.txt'
    if os.path.isfile(robots_path):
        print('Robots.txt for \'{}\' already exists.\n'.format(robots_path))
        return
    if not os.path.exists(dirname_path):
        os.makedirs(dirname_path)
    robots_file = open(robots_path, 'w+')
    robots_file.write(rp)
    robots_file.close()

def read_logs(logs, filename):
    logfilename, dirname_path = get_logfilename_dirname_path(filename)
    if not os.path.exists(dirname_path):
        print('Logfile directory \'{}\' does not exist.\n'.format(logfilename_path))
    logfilename_path = dirname_path + logfilename
    if not os.path.isfile(logfilename_path):
        print('Logfile \'{}\' does not exist.\n'.format(logfilename_path))
    else:
        logfile = open(logfilename_path, 'r')
        print(logfile.read())
        logfile.close()

def save_logs(logs, filename):
    print('Here are the logs : \n{}\n'.format(logs))
    logfilename, dirname_path = get_logfilename_dirname_path(filename)
    if not os.path.exists(dirname_path):
        os.makedirs(dirname_path)
    logfilename_path = dirname_path + logfilename
    if os.path.isfile(logfilename_path):
        os.remove(logfilename_path)
    logfile = open(logfilename_path, 'w+')
    logfile.write('[' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + ']\n\n')
    nb_errors = 0
    for key, value in logs.items():
        logfile.write(str(value) + ' => ' + str(key) + '\n')
        if str(value) != 'OK':
            nb_errors += 1
    logfile.write('\n' + str(nb_errors) + ' error(s) found on ' + str(len(logs)) + ' websites URL.\n')
    logfile.close()

def get_site_map(rp, url):
    to_exclude = ['aholddelhaize']
    if url in to_exclude:
        return None
    rp = rp.split('\n')
    rp = [x for x in rp if 'Sitemap:' in x]
    if rp == []:
        return None, None
    rp = rp[0].replace('Sitemap:', '').strip()
    if 'http' not in rp:
        rp = url + rp
    try:
        content = scrapper.get_url_content(rp)
        name = rp.split('/')[-1]
        return name, content
    except ValueError:
        return None, None
'''
def save_web_content_list(content, name, path, mode):
    if content is None:
        return
    if not os.path.isdir(path):
        if os.path.isfile(path):
            os.rename(path, path + '___')
        os.makedirs(path)
    if name == '':
        name = 'unknown___'
    full_path = os.path.join(path, name)
    if os.path.isfile(full_path):
        print('\'{}\' already exists.\n'.format(full_path))
        return
    fd = open(full_path, mode)
    for _ in content:
        fd.write(_)
    fd.close()
'''
def save_web_content(content, name, path):
    if os.path.isfile(path + name):
        print('\'{}\' already exists.\n'.format(path + name))
        return
    if not os.path.exists(path):
        os.makedirs(path)
    fd = open(path + name, 'w+')
    fd.write(content)
    fd.close()

'''
def run(df, filename, data_dir):
    filename = filename.replace('.xlsx', '')
    logs = dict()
    for index, rows in df.iterrows():
        if not pd.isnull(rows['Website']):
            url = rows['Website']
            regex = r"^https?://[^/]+"
            url = re.findall(regex, url)[0]
            print('-> Name : {} ({})\n   Link: {} \n'.format(rows['Name'], rows['Code'], url))
            log = scrapper.try_reach_url(url)
            rp = scrapper.get_robots_parser(url + '/robots.txt')
            #print(rp)
            if rp is not None:
                save_robots(rp, filename, url)
                name, content = get_site_map(rp, url)
                if content is not None:
                    domain_url = url.split('//')[-1].split('/')[0]
                    path = os.getcwd() + '/' + data_dir + '/' + filename + '/'
                    save_web_content(content, domain_url + '_sitemap_' + name, path)
                    print('-->{}<--\n'.format(name))
            logs.update(log)
        idx += 1
    logger.save_logs(logs, filename)
    #logger.read_logs(logs, filename)
'''
