import os
import shutil
import re
import pandas as pd
import pintell.core.utils as utils
import pintell.core.loader as loader
from pintell.core.unit import Unit

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

    def __init__(self, name, data_path, inputs_path=None):
        """ Constructor of Project object """
        print('\nCreating new project : name = {}\n'.format(name))
        self.name = name
        self.data_path = os.path.join(data_path, name)
        print('Poject input path ->{}<-'.format(len(inputs_path)))
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
                #print('Removing {} because {} does not exist'.format(subdirname, subdirname + '.txt'))
                #print('Trying to remove {} for {}'.format(os.path.join(self.data_path, subdirname), subdirname))
                shutil.rmtree(os.path.join(self.data_path, subdirname))
        print('\n->{} units has been loaded successfuly.\n'.format(idx))
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
            first_line, middle, last_line = unit.load_urls(unit.logfile)
            downloaded_files = len(unit._local_tree())
            if verbose:
                print('{}:'.format(first_line.split(' ')[2].replace('\n', '')))
                print('{}'.format(last_line))
                print('{} downloaded file(s)\n'.format(downloaded_files))
            numbers = [int(n) for n in last_line.split() if n.isdigit()]
            regex_date = r"(?<=\[)(.*?)(?=\])"
            date = re.findall(regex_date, last_line)[0]
            regex_duration = r"(?<=Duration.).[0-9:]*"
            duration = re.findall(regex_duration, last_line)[0]
            duration = duration.strip()
            total_downloaded_files += downloaded_files
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
                    'downloaded_files': downloaded_files,#,
                    'date': date,
                    'duration': duration
                    #'arborescence': unit.remote_arborescence(unit.logfile)
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

    def _load_units_from_data_path(self):
        """ Load project units from project self.data_path (full path where project data is stored)
        """
        print('Loading websites list from data_path \'{}\' ....\n'.format(self.data_path))
        project_directories = utils.get_directories_list(self.data_path)
        if self.units != []:
            del self.units[:]
        # loop on all unit directory and instanciate Units with their url
        for subdirname in project_directories:
            with open(os.path.join(self.data_path, subdirname, subdirname + '.txt')) as fd:
                file_content = fd.readlines()
                url = file_content[0].split(' ')[2].replace('\n', '')
                self.units.append(Unit(self.data_path, url))
        print('\n {} units successfuly loaded.\n'.format(len(self.units)))

    def _load_units_from_excel(self):
        """ Load project units from excel file.
            Excel file must contain a column named 'Website' with the url of wesite to monitor
        """
        print('Loading websites list from file \'{}\' ....\n'.format(self.data_path))
        for index, rows in self.config_df.iterrows():
            if not pd.isnull(rows['Website']):
                url = rows['Website']
                regex = r"^https?://[^/]+"
                url = re.findall(regex, url)[0]
                print('-------------------------------------------------------------------------------------------')
                print('\n-> New Unit loaded : {} \n'.format(url))
                self.units.append(Unit(self.data_path, url))
        print('-------------------------------------------------------------------------------------------')
        print('\n {} units successfuly loaded.\n'.format(len(self.units)))

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

    def download_units_diff(self, links):
        if links == [] or links is None:
            print('[ERROR] delete_download_units : No urls specified.\n')
            return None
        dict_links = utils.from_links_to_dict(links)
        tasks = list()
        if isinstance(dict_links, dict) and bool(dict_links):
            for key, val in dict_links.items():
                unit = self.get_unit_from_url(key)
                task = unit.download_changed_files_from_links(val)
                tasks.append(task)
            return tasks
        else:
            print('Dict() of units url is not OK.')
            return None








