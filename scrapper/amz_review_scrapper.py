from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from data.model.review_model import Review
from service.review_service import ReviewService

class AmzReviewScrapper ():
   target_url: str = ''
   page: int = 1
   max_page: int = 11
   que: list = []

   def __init__(self, target_url: str) -> None:
      self.target_url = target_url
      self.driver = webdriver.Chrome()
      self.wait = WebDriverWait(self.driver, 10)


   def wait_until_visible(self, xpath):
      return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


   def find_by_xpath(self, xpath):
      try:
         return self.driver.find_element(By.XPATH, xpath)
      except:
         return None
   

   def get_html_from_target(self, target):
      return BeautifulSoup(target.get_attribute('outerHTML'), 'html.parser')


   def open_browser(self):
      self.driver.get('https://www.amazon.com/')
      sleep(2)
      self.driver.get(self.target_url)
      self.wait_until_visible('//*[@id="cm_cr-review_list"]')


   def get_list_container(self):
         sleep(2)
         return self.get_html_from_target(self.driver.find_element(By.XPATH, '//*[@id="cm_cr-review_list"]'))
   

   def scrap_data(self):
      reviews = self.get_list_container().find_all(attrs={"data-hook" : 'review'})

      for r in reviews:
         id = r['id']
         title = r.find(attrs={'data-hook': 'review-title'}).find('span', class_='a-letter-space').find_next_sibling('span').get_text()
         rating = r.find(attrs={'data-hook': 'review-title'}).find('i').find('span').get_text()[0:3]
         country = r.find(attrs={'data-hook': 'review-date'}).get_text().split('Reviewed in the ')[-1].split('on')[0].strip()
         date = r.find(attrs={'data-hook': 'review-date'}).get_text().split(' on ')[-1]
         vp = r.find(attrs={'data-hook': 'avp-badge'}).get_text() == 'Verified Purchase' if True else False
         review = r.find(attrs={'data-hook' : 'review-body'}).get_text().strip()
         name = r.find(attrs={'data-hook': 'genome-widget'}).find('span', class_='a-profile-name').get_text().strip()

         images = []

         try:
            imgs = r.find_all('div', class_='review-image-container')
            if(len(imgs) > 0):
               for img in imgs:
                  images.append(img.find('img')['src'])
         except Exception as e: 
            print(e)
            images = []

         try:
            video = r.find('div', id=f'review-video-id-{id}')['data-video-url']
         except Exception as e: 
            print(e)
            video = ''

         print(id)
         print(title)
         print(rating)
         print(country)
         print(date)
         print(vp)
         # print(review)
         print(images)
         print(video)
         print(name)

         review = Review(id=id, review=review, country=country, date=date, pictures=images, rating=rating, vp=vp, title=title, video=video, name=name)
         self.que.insert(0, review)


      sleep(2)
      self.page = self.page + 1

      if(self.page < self.max_page):
         next_page_btn = self.find_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
         next_page_btn.click()
         sleep(1)

         self.scrap_data()
      else:
         return


   def start(self): 
      review_service = ReviewService()
      self.open_browser()

      try:
         self.scrap_data()
      except Exception as e:
         print(f'scrap error {e}')
         review_service.insert_reviews(self.que)

      review_service.insert_reviews(self.que)