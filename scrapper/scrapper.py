from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


from config.app_config import AppConfig
from data.model.listing_model import Listing

'''
Nice to have features

1. Record last scrapped item
    Have a list of items to visit in memory.
    Create log file when application faces error and shuts down.
    Record the list of items and last fetched items index or id.

2. Continue from certain point
    In case the application fails, using the log file to locate where it left off and re-start from there.
    
'''

class Scrapper:
    # config: AppConfig = None

    def __init__(self, config):
        # self.config = config
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        
    def wait_until_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def find_by_xpath(self, xpath):
        try:
           return self.driver.find_element(By.XPATH, xpath)
        except:
            return None
    
    def load_browser(self, url):
        if(url):
            self.driver.get(url)
            self.wait_until_visible('//*[@id="search-results-page-1"]/ol')
            
            if(self.config['filter'] == 'filter'):
                self.set_filters()
            else:
                self.start()

    def locate_listing_container(self):
        return self.find_by_xpath('//*[@id="search-results-page-1"]/ol')

    def get_html_from_target(self, target):
        return BeautifulSoup(target.get_attribute('outerHTML'), 'html.parser')
                
    def scrap_title(self, page):
        return page.find('span', class_='postingtitletext').getText().strip()
    
    def scrap_images(self, page):
        image_container = self.find_by_xpath('/html/body/section/section/section/figure/div[1]')
        if(image_container): 
            self.wait_until_visible('/html/body/section/section/section/figure/div[1]/div/div')

            image_list_container = page.find('div', class_='swipe-wrap')
            image_list = []
            
            for img in image_list_container.find_all('div', class_='slide'):
                image_list.append(img.find_next('img').attrs['src'])   
            
            return image_list
        else:
            return []
    
    def scrap_date(self, page):
        date_container = page.find_element(By.XPATH, '//*[@id="display-date"]/time')
        date_container.click()
        sleep(1)
        return self.get_html_from_target(date_container).getText().strip()
    
    def scrap_desc(self, page):
        return page.find('section', id='postingbody').getText().strip()

    def scrap_listing_info(self):
        self.wait_until_visible('/html/body/section/section')

        page = self.find_by_xpath('/html/body/section/section')
        page_html = self.get_html_from_target(page)
        
        title = self.scrap_title(page_html)
        url = self.driver.current_url
        date = self.scrap_date(page)
        pics = self.scrap_images(page_html)
        desc = self.scrap_desc(page_html)
        
        return Listing(title, url, date, pics, desc)
    
    def start(self):
        list_container = self.locate_listing_container()
        soup = self.get_html_from_target(list_container)
        
        listings_count = len(list_container.find_elements(By.TAG_NAME, 'li'))
        i = 0
        
        while i < listings_count:
            list_container = self.locate_listing_container()
            listings = list_container.find_elements(By.TAG_NAME, 'li')
            listings[i].click()
            result = self.scrap_listing_info()
            print(result.to_dict())
            self.driver.back()
            i += 1
        
        sleep(5)
        pass
    
    def quit(self):
        try:
            if(self.driver):
                self.driver.quit()
                
        except Exception as e:
            print(f"Quit error: {e}")