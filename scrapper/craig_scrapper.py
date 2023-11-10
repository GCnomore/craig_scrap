import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from data.db.main import connect_mongodb


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
    listings = []
    listings_dict = []
    main_driver = None
    sub_driver = None

    def __init__(self, config):
        self.config = config
        self.main_driver = webdriver.Chrome()
        # self.main_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.main_wait = WebDriverWait(self.main_driver, 10)
        
    def wait_until_visible(self, wait, xpath):
        return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    
    def find_by_xpath(self, driver, xpath):
        try:
           return driver.find_element(By.XPATH, xpath)
        except:
            return None
    
    def get_html_from_target(self, target):
        return BeautifulSoup(target.get_attribute('outerHTML'), 'html.parser')
    
    def locate_listing_container(self):
        return self.find_by_xpath(self.main_driver, '//*[@id="search-results-page-1"]/ol')

    def load_browser(self, url):
        if(url):
            self.main_driver.get(url)
            self.wait_until_visible(self.main_wait, '//*[@id="search-results-page-1"]/ol')
            
            if(self.config['filter'] == 'filter'):
                self.set_filters()
            else:
                self.start()
                
    def scrap_title(self, card):
        return card.find('a', class_='posting-title').getText().strip()
    
    def scrap_url(self, card):
        return card.find('a', class_='posting-title')['href']
    
    def scrap_price(self, card):
        return card.find('span', class_='priceinfo').text

    def scrap_basic_listing_info(self, listing):
        card = self.get_html_from_target(listing)

        title = self.scrap_title(card)
        url = self.scrap_url(card)
        price = self.scrap_price(card)
        
        return self.listings.append(Listing(title=title, url=url, price=price))
    

    def scrap_pics(self, listing: Listing):
        self.sub_driver.get(listing.url)
        img_container = self.find_by_xpath(self.sub_driver, '//*[@id="thumbs"]')
        sleep(1)
        img_container_html = self.get_html_from_target(img_container)
        imgs_html = img_container_html.find_all('img')

        pics_list = []

        for img in imgs_html:
            if(img.attrs['src']):
                pics_list.append(img.attrs['src'])

        return pics_list



    def scrap_date(self):
        date_container = self.find_by_xpath(self.sub_driver, '//*[@id="display-date"]/time')
        date_container_html = self.get_html_from_target(date_container)
        
        date = ''
        for d in date_container_html.prettify().split(' '):
            if(d.find('datetime') != -1):
                date = d.split('=')[1].strip('"')

        return date
    
    
    def scrap_odo(self):
        info_container = self.find_by_xpath(self.sub_driver, '/html/body/section/section/section/div[1]/p[2]')
        if(info_container):
            info_container_html = self.get_html_from_target(info_container)
            contents = info_container_html.get_text().strip().split(' ')
            odometer = ''

            for i, c in enumerate(contents):
                if(c.find('odometer') != -1):
                    numbers = re.findall(r'\d+', contents[i + 1])
                    odometer = ''.join(numbers)

            return odometer
        


    def start(self):
        self.list_container = self.locate_listing_container()
        # soup = self.get_html_from_target(list_container)
        
        listings_count = len(self.list_container.find_elements(By.TAG_NAME, 'li'))
       
        i = 50
        while i < listings_count:
            list_container = self.locate_listing_container()
            listing = list_container.find_elements(By.TAG_NAME, 'li')
            self.scrap_basic_listing_info(listing[i])
            i += 1
        
        self.sub_driver = webdriver.Chrome()
        self.sub_wait = WebDriverWait(self.sub_driver, 10)

        x = 50
        while x < len(self.listings):
            pics = self.scrap_pics(self.listings[x])
            date = self.scrap_date()
            odo = self.scrap_odo()


            self.listings[x].pics = pics
            self.listings[x].date = date
            self.listings[x].odometer = odo

            self.listings_dict.append(self.listings[x].to_dict())
            print(self.listings[x].to_dict())
            x += 1

        isaac_table = connect_mongodb()
        isaac_table.insert_many(self.listings_dict)


    def quit_main(self):
        try:
            if(self.main_driver):
                self.main_driver.quit()
                
        except Exception as e:
            print(f"Quit error: {e}")

    def quit_sub(self):
        try:
            if(self.sub_driver):
                self.sub_driver.quit()
                
        except Exception as e:
            print(f"Quit error: {e}")