import os
import traceback
import datetime
import re
import shutil
import pintell.core.crawler as crawler
import pintell.core.downloader as downloader
import pintell.core.utils as utils

class Unit:
    """ A Unit is all parameters associated with one website monitoring,
        such as url (primary key to find unit), logfile, etc.
        args:
            path (str): full path where project data is stored
            url (str): full url of the website (e.g. https://www.airfranceklm.com)
    """
    def __init__(self, path, url):
        self.path = os.path.join(path, url.split('//')[-1].split('/')[0])
        self.download_path = os.path.join(self.path, 'website_content')
        self.url = url
        self.logfile = os.path.join(self.path, url.split('//')[-1].split('/')[0]) + '.txt'
        self._load_units_parameters()

    def __str__(self):
        return 'UNIT : path = {}, download_path = {}, url = {}, logfile = {}\n'.format(self.path,\
            self.download_path, self.url, self.logfile)

    def _load_units_parameters(self):
        # this function has to be called after integrity is checked in project
        self.is_downloaded = False
        self.is_base_crawled = False
        self.total = self.pages = self.pdfs = self.excels = self.errors = 0
        # check if website has been downloaded
        if os.path.isdir(self.download_path):
            self.is_downloaded = True
        # check if website has been crawled
        if os.path.isfile(self.logfile):
            self.is_base_crawled = True
        # check if unit exist in the project. If not, create directory
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        # if website has been crawled, get statistics
        if self.is_base_crawled:
            last_line = self.crawling_stats(self.logfile)
            numbers = [int(n) for n in last_line.split() if n.isdigit()]
            self.total = numbers[0]
            self.pages = numbers[1]
            self.pdfs = numbers[2]
            self.excels = numbers[3]
            self.errors = numbers[4]

    def download(self, provided_links=None):
        """ Download all content from given links
            kwarg:
                provided_links (list): List of websites to download (str)
        """
        # if nothing downloaded before, create directory to put content
        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)
            # if no particular links specified, load all crawled links
            if provided_links is None:
                links = self._remote_tree()
            else:
                links = provided_links
            print('***** Downloading website {} ({} links) *****\n'.format(self.url, len(links)))
            # download loaded links
            downloader.download_website(links, self.download_path, self.url, random_header=True)
        else:
            # if some of the links are already downloaded, download only the remainder
            print('A directory named {} already exists !\n'.format(self.download_path))
            if provided_links is None:
                links = self._tree_diff()
            else:
                links = self._tree_diff(links=provided_links)
            if len(links) != 0:
                print('***** Downloading website {} ({} links) *****\n'.format(self.url, len(links)))
                downloader.download_website(links, self.download_path, self.url, random_header=True)
            else:
                # no remaining links to download
                print('Website links have already been downloaded.\n')

    def delete_downloaded(self):
        """ Deletes all website content that has been downloaded
        """
        if not os.path.isdir(self.download_path):
            print('There is nothing downloaded for website {}.\n'.format(self.url))
        else:
            shutil.rmtree(self.download_path)
            print('All downloaded content from website \'{}\' has been deleted.'.format(self.url))

    def _remote_tree(self):
        first_line, middle, last_line = self._load_urls()
        # get rid of <PDF> and <EXCEL> tags in list of links
        r = utils.find_internal_links(middle)
        return sorted(r, reverse=True)

    def _local_tree(self):
        r = utils.walktree_files(self.download_path)
        return sorted(r, reverse=True)

    def _tree_diff(self, links=None):
        remote_tree = list()
        if links is not None:
            [remote_tree.append(x) for x in links]
        else:
            [remote_tree.append(x) for x in self._remote_tree()]
        local_tree = list()
        [local_tree.append(x) for x in self._local_tree()]
        # ignore differences due to storage issues tricks
        local_tree = utils.clean_local_tree(local_tree)
        diff = set(set(remote_tree) ^ set(local_tree))
        #print('\nlocal_tree : {}'.format(set(local_tree)))
        #print('\nremote_tree : {}'.format(set(remote_tree)))

        if links is not None:
            diff = set(remote_tree) - (set(local_tree))
            #print('\ndiff : {}'.format(diff))
        return sorted(diff)

    def get_regex_remote_tree(self, regex):
        """ Get list of crawled links matching regex
            arg:
                regex (list): List of patterns links must match
        """
        return [x for x in self._remote_tree() if regex in x]

    def crawling_stats(self, logfile):
        """ Returns logfile statistics information (last line of logfile)
            arg:
                logfile (str): Logfile of crawler
            return:
                last_line (str): Last line of logfile
        """
        first_line, middle, last_line = self.load_urls(logfile)
        return last_line

    def crawl(self, max_depth=1):
        """ Crawl website links and store them in logfile
            kwarg:
                max_depth (int): Max depth of the crawl bot (default: 1)
        """
        if os.path.isfile(self.logfile, max_depth):
            print('A logfile named {} already exists !\n'.format(self.logfile))
            return
        try :
            log_debut = '[{}] {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), self.url)
            pages, files, log_fin = crawler.link_crawler(self.url, '/', user_agent='wsgt', max_depth=max_depth)
            self._save_urls(pages, files, log_debut, log_fin)
        except Exception as e:
            print('Error with website : {}. Error = {}\n'.format(self.url, traceback.format_exc()))

    def download_changed_files(self, regex, force=False):
        local_tree = utils.clean_local_tree(self._local_tree())
        partial_remote_tree = self.get_regex_remote_tree(regex)

        #print('partial_remote_tree : \n{}'.format(partial_remote_tree))
        #print('local_tree : \n{}'.format(local_tree))

        if not set(partial_remote_tree).issubset(local_tree):
            print('\nYou are trying to download changed files that have never been downloaded before !')
            if force:
                available_links = list(set(partial_remote_tree).intersection(set(local_tree)))
                print('Force option will only download links that are available. i.e : {}'.format(available_links))
                partial_remote_tree = available_links
            else:
                exit(0)
        x = datetime.datetime.now()
        filename_time = x.strftime("%Y%m%d%H%M")
        '''
        if os.path.isdir(self.download_path + filename_time):
            shutil.rmtree(self.download_path + filename_time)
        os.mkdir(self.download_path + filename_time)
        '''
        downloader.download_website_diff(partial_remote_tree, self.download_path, self.download_path + filename_time, self.url)


    def _save_urls(self, pages, files, log_debut, log_fin):
        """ Saves freshly crawled links in the logfile
            args:
                pages (list): List of crawled html pages
                files (list): List of crawled Excel and pdf files
                log_debut (str): First line of logfile (e.g. '[2018-12-07 15:09] https://www.airliquide.com')
                log_fin (str): Last line of logfile
        """
        # check if urls have been already crawled and logfile exists
        if os.path.isfile(self.logfile):
            print('A file named {} already exists !\n'.format(self.logfile))
            return
        # Creates new logfile with all informations above
        fd = open(self.logfile, 'w+')
        fd.write(log_debut)
        pages_len = len(pages)
        idx = 0
        for page in pages:
            idx += 1
            fd.write(page)
            if idx != len(pages):
                fd.write('\n')
        for file in files:
            fd.write(file)
            fd.write('\n')
        fd.write(log_fin)
        fd.close()

    def load_urls(self, logfile):
        """ Loads urls stored in logfile and return them.
            return:
                first_line (str): First line of the logfile
                middle (list): All links in logfile with tags (<PDF>, <EXCEL>)
                last_line (str): Last line of logfile with links statistics
        """
        with open(logfile, 'r') as fd:
            ret = fd.readlines()
        first_line = ret[0].replace('\n', '')
        last_line = ret[-1].replace('\n', '')
        middle = [x.replace('\n', '') for x in ret[2:-2]]
        middle = [x for x in middle if x != '']
        middle = sorted(middle)
        return first_line, middle, last_line