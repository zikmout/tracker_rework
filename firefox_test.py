import os
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

browser = webdriver.Firefox()
browser.implicitly_wait(10)
browser.get('https://www.adidas-group.com/en/investors/share/share-buyback/')
browser.save_screenshot(os.path.join(os.getcwd(), 'test.png'))
print(browser.title)

browser.quit()

display.stop()
