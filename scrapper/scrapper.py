from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from config.app_config import AppConfig

class Scrapper:
    config: AppConfig = None

    def __init__(self, config):
        self.config = config
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 10)
    
    def load_browser(self, url):
        if(url):
            self.driver.get(url)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search-results-page-1"]/ol')))
            
            if(self.config['filter'] == 'filter'):
                self.set_filters()
            else:
                self.start()

    def locate_listing_container(self):
        self.list_container = self.driver.find_element(By.XPATH, '//*[@id="search-results-page-1"]/ol')

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
    
    def start(self):
        self.locate_listing_container()
        soup = self.get_html_from_target(self.list_container)
        sleep(5)
        # print(soup.li)
        pass
    
    def quit(self):
        try:
            if(self.driver):
                self.driver.quit()
                
        except Exception as e:
            print(f"Quit error: {e}")