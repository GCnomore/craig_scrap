from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from lxml import html

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
    config: AppConfig = None

    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
        
    def __wait_until_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def __create_xpath(self, element):
        return html.tostring(element, with_tail=False, method="html", pretty_print=True).decode('utf-8')
    
    def load_browser(self, url):
        if(url):
            self.driver.get(url)
            self.__wait_until_visible('//*[@id="search-results-page-1"]/ol')
            
            if(self.config['filter'] == 'filter'):
                self.set_filters()
            else:
                self.start()

    def locate_listing_container(self):
        return self.driver.find_element(By.XPATH, '//*[@id="search-results-page-1"]/ol')

    def get_html_from_target(self, target):
        return BeautifulSoup(target.get_attribute('outerHTML'), 'html.parser')
                
    def set_filters(self):
        if(self.config['hide_dup']):
            hide_dup_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[3]/div[2]/div[1]/label[4]/input')
            hide_dup_btn.click()
            sleep(5)
        
        if(self.config['has_image']):
            has_image_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[3]/div[2]/div[1]/label[2]/input')
            has_image_btn.click()
            sleep(5)
            
        if(self.config['is_location_filter'] and self.config['miles_from_location'] and self.config['zip_code']):
            miles_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[3]/div[2]/div[2]/div[2]/input[1]')
            zip_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[3]/div[2]/div[2]/div[2]/input[2]')
            apply_btn = self.driver.find_element(By.XPATH, '/html/body/div[1]/main/form/div[3]/div[4]/button[3]')
            
            miles_input.send_keys(self.config['miles_from_location'])
            zip_input.send_keys(self.config['zip_code'])

            sleep(1)
            
            apply_btn.click()
            
            sleep(5)
    
    def scrap_title(self, page):
        return page.find('span', class_='postingtitletext').getText().strip()
    
    def scrap_images(self, page):
        image_list_container = page.find('div', class_='swipe-wrap')
        image_list = []
        
        for img in image_list_container.find_all('div', class_='slide'):
            image_list.append(img.find_next('img').attrs['src'])   
        
        return image_list
    
    def scrap_date(self, page):
        date_container = page.find_element(By.XPATH, '//*[@id="display-date"]/time')
        date_container.click()
        sleep(1)
        return self.get_html_from_target(date_container).getText().strip()
    
    def scrap_desc(self, page):
        return page.find('section', id='postingbody').getText().strip()

    def scrap_listing_info(self):
        page = self.driver.find_element(By.XPATH, '/html/body/section/section')
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
        sleep(2)
        
        listings_count = len(list_container.find_elements(By.TAG_NAME, 'li'))
        i = 0
        
        while i < listings_count:
            list_container = self.locate_listing_container()
            listings = list_container.find_elements(By.TAG_NAME, 'li')
            listings[i].click()
            sleep(2)
            result = self.scrap_listing_info()
            print(result.to_dict())
            self.driver.back()
            sleep(2)
            i += 1
        
        sleep(5)
        pass
    
    def quit(self):
        try:
            if(self.driver):
                self.driver.quit()
                
        except Exception as e:
            print(f"Quit error: {e}")