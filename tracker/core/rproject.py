import os
import shutil
import re
import pandas as pd
import time
import datetime
import tracker.core.utils as utils
import tracker.core.loader as loader
import tracker.core.logger as logger
import tracker.core.downloader as downloader
from tracker.core.unit import Unit
import tracker.workers.continuous.continuous_worker as continuous_worker
from redbeat import RedBeatSchedulerEntry as Entry
import math
import threading


class RProject:
    """ A project consists of a list of websites to monitor,
        and parameters associated with each of these websites.
        args:
            name : project name (e.g. share_buyback)
            data_path : full path where project data is stored
            inputs_path : full path of .xlsx file containing list of websites
    """
    # list of websites objects
    units = list()
    lines = list()

    def __init__(self, name, data_path, inputs_path=None):
        """ Constructor of Project object """
        print('\nCreating new project : name = {}\n'.format(name))
        self.name = name
        self.data_path = os.path.join(data_path, name)
        print('Poject input path ->{}<-'.format(inputs_path))
        if inputs_path != '' and inputs_path is not None and len(inputs_path) != 0:
            self.config_df = loader.get_df_from_excel(inputs_path)
        else:
            self.config_df = None
        # If project does not exist, creates it
        if not self._exist(inputs_path):
            self._create_project()

    def __str__(self):
        """ Method called when asking conversion of the object in chain """
        return 'Project() : name = {}, data_path = {}, config_df = {}'.format(self.name, self.data_path, self.config_df)

    def _check_integrity(self, minimum_links=0):
        """ Method called if project directly loaded from folder.
            It checks whether the project folder called has an appropriate architecture.
            If not, it cleans the project folder by :
                - removing website folder when logfile (crawling links) is empty (no first crawl, nothing possible)
                - removing website folder when crawling has aborded (no last_line in logfile)
                - removing website folder when minimum links crawled has not been reached in logfile
            kwargs:
                minimum_links (int): minimum crawled links to keep website directory alive (default: 0)
        """
        # need to take care of difference between accorhotels.group and www.accorhotels.group (actually removing folder)
        print('\n-> Checking integrity of the project ...\n')
        idx = 0
        # listing directories in project directory
        project_directories = utils.get_directories_list(self.data_path)
        # walking through each website directory to make sure its approprietly formated
        for subdirname in project_directories:
            subdirname_files = os.listdir(os.path.join(self.data_path, subdirname))
            if subdirname + '.txt' in subdirname_files:
                with open(os.path.join(self.data_path, subdirname, subdirname + '.txt')) as fd:
                    file_content = fd.readlines()
                    if file_content == []:
                        print('Removing : {} because logfile is empty.'.format(os.path.join(self.data_path, subdirname)))
                        shutil.rmtree(os.path.join(self.data_path, subdirname))
                    elif file_content[-1][0] != '[':
                        print('Removing : {} because logfile crawler has aborded.'.format(os.path.join(self.data_path, subdirname)))
                        shutil.rmtree(os.path.join(self.data_path, subdirname))
                    else:
                        last_line = file_content[-1]
                        numbers = [int(n) for n in last_line.split() if n.isdigit()]
                        if numbers[0] < minimum_links:
                            print('Removing : {} because {} shows that less than {} links have been crawled.'.format(os.path.join(self.data_path, subdirname), subdirname + '.txt', minimum_links))
                            shutil.rmtree(os.path.join(self.data_path, subdirname))
                        else:
                            idx += 1
            else:
                pass
                #print('Removing {} because {} does not exist'.format(subdirname, subdirname + '.txt'))
                #print('Trying to remove {} for {}'.format(os.path.join(self.data_path, subdirname), subdirname))
                #shutil.rmtree(os.path.join(self.data_path, subdirname))
        print('\n->Checking integrity of {} units, DONE.\n'.format(idx))
        return False

    def _exist(self, inputs_path):
        """ Verify if the project already exists and directory name is ok """
        # make sure .xlsx config file with list of websites ---> NEED TO CHANGE IN CONSTRUCTOR
        if not os.path.isfile(inputs_path):
            print(('\nThe inputs path file \'{}\' does not exist.'
            ' Please provide a file that exists if you want to use config file.\n').format(inputs_path))
        # make sure project directory exist
        if not os.path.isdir(self.data_path):
            print(('\nThe data path directory \'{}\' does not exist.'
            ' Creating project \'{}\'.\n').format(self.data_path, self.name))
            return False
        else:
            print('Project {} already exists.'.format(self.name))
            # verify if project is properly architectured
            self._check_integrity()
            return True

    def _create_project(self):
        """ Method to create project directory """
        print('\nProject does not exist yet, creating project directory.\n')
        os.mkdir(self.data_path)
        # NEED TO MAKE IF CONDITION IF CONSTRUCTOR
        print(self.config_df)
        print('\n')

    def units_stats(self, units=None, verbose=False):
        """ Print Project statistics (sum, average, total) of all websites.
            And websites list statistics (Total Links scrapped, total pages, total
            pdf files, total excel files, total errors).
            kwargs:
                units (list): list of Unit object
                verbose (bool): Print stats for every Unit
        """
        if self.units == []:
            print('[ERROR] Units Statistics : There are no units loaded in this project yet. Use _load_units function(s) to do so.\n')
            return None
        if units == []:
            print('[ERROR] Units Statistics : There are no units matching filtered criterias.\n')
            return None
        if verbose:
            print('------------ Units Statistics ------------\n')
        total = pages = pdfs = excels = errors = total_downloaded_files = 0
        # if units list passed to the function take the list. Otherwise, take self.units (all project units)
        if units is not None:
            all_units = units
        else:
            all_units = self.units
        # for every unit, get first line and last line of logfile to read it
        # also count number of downloaded files from local_tree
        uid = 1
        units_dict = dict()
        for unit in all_units:
            total_downloaded_files += unit.downloaded_files
            total += unit.total
            pages += unit.pages
            pdfs += unit.pdfs
            excels += unit.excels
            errors += unit.errors
            unit_dict = { 
                uid : {
                    'url': unit.url,
                    'total': unit.total,
                    'pages': unit.pages,
                    'pdfs': unit.pdfs,
                    'excels': unit.excels,
                    'errors': unit.errors,
                    'downloaded_files': unit.downloaded_files,
                    'date': unit.date,
                    'duration': unit.duration,
                    'is_base_crawled': unit.is_base_crawled
                }
            }
            units_dict.update(unit_dict)
            uid += 1
        nb_items = len(all_units)
        if verbose:
            print('-> Statistics on {}/{} available unit(s).\n'.format(nb_items, len(self.units)))
            print('-> SUM     : Total: {}, Pages: {}, PDFS : {}, EXCEL(s) : {}, Errors : {}\n'.format(total, pages, pdfs, excels, errors))
            print('-> AVERAGE : Total: {}, Pages: {}, PDFS : {}, EXCEL(s) : {}, Errors : {}\n'.format(int(total / nb_items), int(pages / nb_items), int(pdfs / nb_items), int(excels / nb_items), int(errors / nb_items)))
            print('-> TOTAL FILES DOWNLOADED: {}'.format(total_downloaded_files))
            print('-------------------------------------------\n')
        return units_dict

    def filter_units(self, minimum_total=False, minimum_pages=False, minimum_pdfs=False, minimum_excels=False, minimum_erros=False):
        """ Take all Project units matching various criterias : total, pages, pdf, excels, errors.
            kwargs:
                minimum_total (int): minimum total links scrapped
                minimum_pages (int): minimum html pages scrapped
                minimum_pdfs (int): minimum pdfs files scrapped
                minimum_excels (int): minimum excel files scrapped
                minimum_erros (int): minimum errors on websites
        """
        filtered = list()
        if minimum_total is False and minimum_pages is False and minimum_pdfs is False \
        and minimum_excels is False and minimum_erros is False:
            for unit in self.units:
                filtered.append(unit)
            return filtered 
        for unit in self.units:
            if minimum_total and unit.total >= minimum_total:
                filtered.append(unit)
            elif minimum_pages and unit.pages >= minimum_pages:
                filtered.append(unit)
            elif minimum_pdfs and unit.pdfs >= minimum_pdfs:
                filtered.append(unit)
            elif minimum_excels and unit.excels >= minimum_excels:
                filtered.append(unit)
            elif minimum_erros and unit.errors >= minimum_erros:
                filtered.append(unit)
        return filtered

    def load_units_from_list(self, units_url):
        """ Load project units from project self.data_path (full path where project data is stored)
        """
        print('Loading websites list from list \'{}\' ....\n'.format(units_url))
        #project_directories = utils.get_directories_list(self.data_path)
        if self.units != []:
            del self.units[:]
        for url in units_url:
            self.units.append(Unit(self.data_path, url))
        print('\n {} units successfuly loaded from list.\n'.format(len(self.units)))





    def add_links_to_crawler_logfile(self, links_list, wait=True):

        url_errors = list()
        def run_downloads(unit, unit_url):
            if unit is None or unit.is_base_crawled is False:
                print('Unit url : {} does not exist.'.format(unit_url))
            else:
                internal_link = link.replace(unit_url, '')
                #print('len remote tree before = {}'.format(len(unit._remote_tree())))
                if unit.add_crawler_link(internal_link) is True:
                    rets = downloader.download_website([internal_link], unit.download_path, unit.url, random_header=True)
                    for ret in rets:
                        for k, v in ret.items():
                            if v == 'OK':
                                print('->Page {} successfuly downloaded'.format(k))
                            else:
                                print('->Unable to download page {} (Reason : {})'.format(k, v))
                                url_errors.append({k:v})
                    # if ret is True:
                    #     print('->Page {} successfuly downloaded'.format(unit_url + internal_link))
                    # else:
                    #     print('->Unable to download page {}'.format(unit_url + internal_link))
                    #     url_errors.append(err)
                else:
                    print('-> No need to download: {}'.format(unit_url + internal_link))

        print('Loading websites list to add crawled links in data_path \'{}\' ....\n'.format(self.data_path))
        project_directories = utils.get_directories_list(self.data_path)
        if self.units == []:
            print('No Units loaded !')
            return 0

        threads = []
        idx = 0
        for link in links_list:
            idx += 1
            regex = r"^https?://[^/]+"
            unit_url = re.findall(regex, link)[0]
            unit = self.get_unit_from_url(unit_url)
            if wait and idx % 10 == 0:
                time.sleep(wait)
            my_thread = threading.Thread(target=run_downloads, args=(unit, unit_url))
            threads.append(my_thread)
            my_thread.start()

        for x in threads:
            x.join()

        print('All THREADS ARE DONE !!!!')
        return idx, url_errors

    def _load_units_from_data_path(self):
        """ Load project units from project self.data_path (full path where project data is stored)
        """
        print('Loading websites list from data_path \'{}\' ....\n'.format(self.data_path))
        project_directories = utils.get_directories_list(self.data_path)
        if self.units != []:
            del self.units[:]
        # loop on all unit directory and instanciate Units with their url
        for subdirname in project_directories:
            try:
                with open(os.path.join(self.data_path, subdirname, subdirname + '.txt')) as fd:
                    file_content = fd.readlines()
                    url = file_content[0].split(' ')[2].replace('\n', '')
                    self.units.append(Unit(self.data_path, url))
            except Exception as e:
                print('No crawler logfile for dirname : {}'.format(subdirname))
        print('\n {} units successfuly loaded from data_path.\n'.format(len(self.units)))

    def _load_units_from_excel(self):
        """ Load project units from excel file.
            Excel file must contain a column named 'Website' with the url of wesite to monitor
        """
        print('Loading websites list from file \'{}\' ....\n'.format(self.data_path))
        if self.units != []:
            del self.units[:]
        for index, rows in self.config_df.iterrows():
            if not pd.isnull(rows['Website']):
                url = rows['Website']
                regex = r"^https?://[^/]+"
                url = re.findall(regex, url)[0]
                print('-------------------------------------------------------------------------------------------')
                print('\n-> New Unit loaded : {} \n'.format(url))
                self.units.append(Unit(self.data_path, url))
        print('-------------------------------------------------------------------------------------------')
        print('\n {} units successfuly loaded from excel.\n'.format(len(self.units)))

    def _load_tracking_config_excel(self):
        """ Load Name, target website, keywords, etc from excel config file.
            Excel file must contain a column named 'Website', 'Name', 'target' and 'target_label'
        """
        print('Loading tracking excel config from file \'{}\' ....\n'.format(self.data_path))
        if self.lines != []:
            del self.lines[:]
        for index, rows in self.config_df.iterrows():
            if not pd.isnull(rows['Website']):
                name = rows['Name']
                website = rows['Website']
                target = rows['target']
                # can be one or multiple keywords
                if isinstance(rows['target_label'], float):
                    target_label = ''
                elif ';' in rows['target_label']:
                    target_label = rows['target_label'].split(';')
                # elif rows['target_label'] == '':
                #     target_label = ''
                else:
                    target_label = [rows['target_label']]

                # can be one or multiple email addresses
                if isinstance(rows['mailing_list'], float):
                    mailing_list = ''
                elif ';' in rows['mailing_list']:
                    mailing_list = rows['mailing_list'].split(';')
                # elif rows['target_label'] == '':
                #     target_label = ''
                else:
                    mailing_list = [rows['mailing_list']]
                line = {
                    'name': name,
                    'website': website,
                    'target': target,
                    'keywords': target_label,
                    'mailing_list' : mailing_list
                }
                self.lines.append(line)

    def update_unit(self, url):
        idx = 0
        for unit in self.units:
            if unit.url == url:
                self.units.pop(idx)
                updated_unit = Unit(self.data_path, url)
                self.units.append(updated_unit)
                break;
            idx += 1
        print('Unit successfully updated')
        return updated_unit

    def get_unit_from_url(self, url):
        """ Get Unit object from its url which is unique
            arg:
                url (str): url of website (e.g. 'http://www.airfranceklm.com')
            return:
                unit (Unit): Unit of the asked website, or None if not found
        """
        for unit in self.units:
            if unit.url == url:
                return unit
        return None

    def delete_downloaded_units(self, units_urls):
        """ Method that delete all downloaded content for provided urls
            arg:
                units_urls (list): List of urls to delete
        """
        if units_urls == [] or units_urls is None:
            print('[ERROR] delete_download_units : No urls specified.\n')
        else:
            for unit_url in units_urls:
                unit = self.get_unit_from_url(unit_url)
                if unit is not None:
                    unit.delete_downloaded()
                else:
                    print('There is no Unit found for url : {}'.format(unit_url))

    def crawl_units(self, units_urls):
        tasks = dict()
        for url, details in units_urls.items():
            print('url -> {}'.format(url))
            unit  = self.get_unit_from_url(url)
            starting_path = details['starting_path']
            depth = details['depth']
            print('received: unit = {}, starting_path = {}, depth = {}'.format(unit, starting_path, depth))
            task = unit.crawl(starting_path=starting_path, max_depth=depth)
            tasks.update({ url : task })
        return tasks

    def generate_crawl_logfile(self, units_urls):
        base_urls = set()
        for url in units_urls:
            regex = r"^https?://[^/]+"
            base_url = re.findall(regex, url)[0]
            base_urls.add(base_url)

        for base_url in base_urls:
            unit = Unit(self.data_path, base_url)
            # minimal data for logfile
            pages = ['/index.html']
            logfile = unit.logfile
            files = []
            log_debut = '[{}] {}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), base_url)
            log_fin = '\n[{}] Duration: {} / Total: 1 / Page(s): 1 / PDF(s): 0 / EXCEL(s): 0 / Errors: 0'.format(\
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), time.strftime("%H:%M:%S", time.gmtime(0)))
            logger.save_urls(logfile, pages, files, log_debut, log_fin)

    def download_units(self, units_urls):
        """ If units_urls is a list, download all content form websites provided in list
            according to what crawled links have been found.
            If units_url is a dict, key is the website, val is the uri regex, content downloaded
            is only the one matching regex.
            arg:
                units_urls (list or dict): if dict(), content is downloaded according to regex
            return:
                tasks (list): list of downloading task created
        """
        tasks = list()
        if isinstance(units_urls, dict) and bool(units_urls):
            for key, val in units_urls.items():
                unit = self.get_unit_from_url(key)
                if unit:
                    for _ in val:
                        # unit.add_crawler_link(unit.get_regex_remote_tree(_))
                        # unit.add_crawler_link()
                        task = unit.download(provided_links=unit.get_regex_remote_tree(_))
                        tasks.append(task)
        else:
            if units_urls == [] or units_urls is None:
                print('[ERROR] _download_units : No urls specified.\n')
            else:
                for unit_url in units_urls:
                    task = self.get_unit_from_url(unit_url).download()
                    tasks.append(task)
        return tasks

    def delete_unit(self, url):
        idx = 0
        for unit in self.units:
            print('unit = {}, compare to url = {}'.format(unit.url, url))
            if url.startswith(unit.url):
                self.units.pop(idx)
                unit.delete_all()
                print('Unit successfully deleted')
                return True
            idx += 1
        print('Unit NOT successfully deleted')
        return False

    def update_units_links(self, units_urls):
        """ If units_urls is a list, download all content form websites provided in list
            according to what crawled links have been found.
            If units_url is a dict, key is the website, val is the uri regex, content downloaded
            is only the one matching regex.
            arg:
                units_urls (list): list of units to update (i.e. delete former version and save new file) 
        """
        for url in units_urls:
            regex = r"^https?://[^/]+"
            base_url = re.findall(regex, url)[0]
            unit = self.get_unit_from_url(base_url)
            #unit.delete_downloaded
            internal_link = url.replace(base_url, '')
            print('URL : {}, internal_link : {}'.format(base_url, internal_link))
            nb = unit.update_downloaded([internal_link])
            print('Nb of unit updated for url {} : {}'.format(nb, base_url))

    def download_units_diff(self, template_type, links, save=False):
        if links == {} or links is None:
            print('[ERROR] delete_download_units : No urls specified.\n')
            return None
        #print('links before = {}'.format(links))
        dict_links = utils.from_links_to_dict(links)
        #print('links after = {}'.format(dict_links))
        #exit(0)

        if template_type == 'share buy back':
            keywords_diff = True
            detect_links = True
            links_algorithm = 'http://localhost:5567/api/v1/predict/is_sbb'
        elif template_type == 'diff':
            keywords_diff = False
            detect_links = False
            links_algorithm = False
        elif template_type == 'diff with keywords':
            keywords_diff = True
            detect_links = False
            links_algorithm = False
        else:
            # This must not happen
            return False

        tasks = list()
        if isinstance(dict_links, dict) and bool(dict_links):
            counter = 0
            for key, val in dict_links.items():
                unit = self.get_unit_from_url(key)
                if unit is not None:
                    counter += 1
                    #print('VAL = {}'.format(val))
                    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
                    task = unit.download_changed_files_from_links(val, keywords_diff, detect_links, links_algorithm, counter)
                    tasks.append(task)
                else:
                    print('Unit {} not found'.format(key))
            return tasks
        else:
            print('Dict() of units url is not OK.')
            return None



    def download_units_diff_delayed_with_email(self, alert_name, template_type,\
        schedule, links, mailing_list, user_email, project_name, save=False):
        if links == {} or links is None:
            print('[ERROR] delete_download_units : No urls specified.\n')
            return None
        print('links before = {}'.format(links))
        dict_links = utils.from_links_to_dict(links)
        print('links after = {}'.format(dict_links))

        # If asked to send mail but no mailing_list provided, return False
        if mailing_list is None:
            print('PB : No mailing_list !!')
            return False
        # Rework mailing_list excel matrix (translate)
        # At the moment, mails are like this : (mailing_list)
        #       target1 --> mail1 mail2 mail3
        #       target2 --> mail2 mail3
        print('Mailing list ==> {}'.format(mailing_list))
        mails_set = set()
        for t, m in mailing_list.items():
            print('M = {}'.format(m))
            if isinstance(m, float) and math.isnan(m):
                continue;
            if isinstance(m, float) and ';' not in str(m):
                mails_set.add(str(m))
            elif isinstance(m, list):
                for s in m:
                    mails_set.add(s)
            else:
                for s in m.split(';'):
                    mails_set.add(s)
        
        print('mail set = {}'.format(mails_set))
        mails_content = dict()
        for mail in mails_set:
            mails_content[mail] = list()

        for t, m in mailing_list.items():
            if isinstance(m, float) and math.isnan(m):
                continue;
            elif isinstance(m, float) and ';' not in str(m):
                if mail != str(m):
                    mails_content[mail].append(t)
            else:
                for mail in mails_set:
                    if mail in m:
                        mails_content[mail].append(t)
        print('MAIL CONTENT = {}'.format(mails_content))
        # Now, mails are like this: (mails_content)
        #       mail1 --> target1
        #       mail2 --> target1 target2
        #       mail3 --> target2

        if template_type == 'share buy back':
            keywords_diff = True
            detect_links = True
            # send_error_to_user = True
            links_algorithm = 'http://localhost:5567/api/v1/predict/is_sbb'
        elif template_type == 'diff':
            keywords_diff = False
            detect_links = False
            # send_error_to_user = True
            links_algorithm = False
        elif template_type == 'diff with keywords':
            keywords_diff = True
            detect_links = False
            # send_error_to_user = True
            links_algorithm = False
        else:
            # This must not happen
            return False

        # Tasks are of type celery chords, so one argument per task
        task_args = list()
        # filename_time = datetime.datetime.now().strftime("%Y%m%d")
        if isinstance(dict_links, dict) and bool(dict_links):            
            for key, val in dict_links.items():
                unit = self.get_unit_from_url(key)

                if unit is not None:
                    print('VAL = {}'.format(val))
                    # VAL = [['/en/investors/stock-and-shareholder-corner/buyback-programs', ['DAILY DETAILS FOR THE PERIOD']]]
                    #print('filename_time = {}'.format(filename_time))
                    task_args.append((val,
                        unit.download_path,
                        unit.download_path,
                        unit.url,
                        keywords_diff,
                        detect_links,
                        links_algorithm))
                else:
                    print('Unit {} not found'.format(key))

            print('Task args ====> {}'.format(task_args))
            print('SCHEDULED = {}'.format(schedule))
            if template_type == 'share buy back':
                entry = Entry(alert_name, 'continuous_worker.share_buy_back_task',\
                    schedule, args=(task_args, mails_content, user_email, project_name), app=continuous_worker.app)
            elif template_type == 'diff':
                entry = Entry(alert_name, 'continuous_worker.diff_task',\
                    schedule, args=(task_args, mails_content, user_email, project_name), app=continuous_worker.app)
            elif template_type == 'diff with keywords':
                entry = Entry(alert_name, 'continuous_worker.diff_with_keywords_task',\
                    schedule, args=(task_args, mails_content, user_email, project_name), app=continuous_worker.app)
            entry.save()
            print('ENTRY IS DUE = {}'.format(entry.is_due()))
            return entry
        else:
            print('Dict() of units url is not OK.')
            return False
