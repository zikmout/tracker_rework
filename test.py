# Taken from : https://codereview.stackexchange.com/questions/167327/scraping-the-full-content-from-a-lazy-loading-webpage
from pprint import pprint

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AdidasScraper:
    def __init__(self, url):
        from selenium import webdriver

        self.url = url
        # binary = FirefoxBinary('/Users/xxx/')
        # self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        #self.wait = WebDriverWait(self.driver, 10)

    # def get_last_line_number(self):
    #     """Get the line number of last company loaded into the list of companies."""
    #     return int(self.driver.find_element_by_css_selector("ul.company-list > li:last-child > a > span:first-child").text)

    def get_links(self):#, max_company_count=1000):
        """Extracts and returns company links (maximum number of company links for return is provided)."""
        self.driver.implicitly_wait(15)
        self.driver.get(self.url)
        elements = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/article/section/div/section[2]')))
        text = elements.text
        # elements = self.driver.find_element_by_class_name("events future visible")
        # element = WebDriverWait(self.driver, 15).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "events future visible"))
        # )

        self.driver.close()
        return text

def wait_for_element(self, by, arg, visibiliy=True, timeout=15):
    self.driver.get(self.url)
    try:
        if visibiliy:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, arg)))
            # r = self.driver.find_element_by_class_name('details')
            # print('len books ≠ {}'.format(len(r)))
        else:
            element = WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, arg)))

    except selenium.common.exceptions.TimeoutException:
        print("wait_for_element timeout: " + arg)
        return None
    return element

scraper = AdidasScraper('https://www.adidas-group.com/en/investors/investor-events/')
elems = scraper.get_links()
# elems = wait_for_element(scraper, By.CLASS_NAME, 'item   visible', visibiliy=True, timeout=15)
print(elems)
# scraper.driver.close()
print('elem = {}'.format(elems))
#print('page source = {}'.format(scraper.driver.page_source()))