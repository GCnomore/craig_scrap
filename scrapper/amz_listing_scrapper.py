from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
from data.model.amz_listing_model import AmzListing
from service.amz_listing_service import AmzListingService

class AmzListingScrapper ():
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
      self.driver.get(self.target_url)
      self.driver.execute_script("document.body.style.zoom='10%'")


   def get_container(self):
         self.wait.until(EC.visibility_of_element_located((By.ID, 'dp')))
         return self.get_html_from_target(self.driver.find_element(By.ID, 'dp'))
   
   

   def scrap_data(self):
      self.wait_until_visible('//*[@id="productTitle"]')
      self.wait_until_visible('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]')
      self.wait_until_visible('//*[@id="videoCount"]')
      # Variation
      self.wait_until_visible('//*[@id="twister-plus-inline-twister-container"]')
      self.wait_until_visible('//*[@id="feature-bullets"]')
      self.wait_until_visible('//*[@id="prodDetails"]/div/div[1]')

      container = self.get_container()
      img_cont = self.get_html_from_target(self.find_by_xpath('//*[@id="altImages"]'))
      video_cont = container.find('div', id='main-video-container')
      video = video_cont.find('video')['src']
      pictures = []

      try: 
         for img in img_cont.find_all('li', attrs={ "data-csa-c-element-type": 'navigational' }):
            pictures.append(img.find('img')['src'])
      except Exception as e:
         print(f'img_cont::: {e}')

      title = container.find('span', id='productTitle').get_text().strip()
      company_name = container.find('a', id='sellerProfileTriggerId').get_text().strip()
      rating = container.find('span', id='acrPopover').find('span', class_='a-size-base').get_text().strip()
      price_box = container.find('div', id='corePriceDisplay_desktop_feature_div')
      price = f"{price_box.find('span', class_='a-price-whole').get_text()}{price_box.find('span', class_='a-price-fraction').get_text()}"
      # sleep(2)

      try:
         temp = self.get_html_from_target(self.find_by_xpath('//*[@id="twister-plus-inline-twister-container"]'))
         # sleep(5)
         variation_cont = temp.find_all('div', attrs={ 'data-csa-c-type': 'widget' })

      except Exception as e:
         print(f'varationcont::::::: {e}')

      variation_types = set()
      for variation in variation_cont:
         variation_types.add(variation.find('span').get_text().strip().split(':')[0])
      variation_types = list(variation_types)
   
      detail_cont = container.find('table', id='productDetails_detailBullets_sections1')
      try:
         keys = detail_cont.find_all('th')
         vals = detail_cont.find_all('td')
      except Exception as e:
         print(f'key val:::: {e}')

      detail = {}

      for i, key in enumerate(keys):
         detail[key.get_text().strip()] = vals[i].get_text().strip()

      date_first_available = detail['Date First Available']
      package_dimensions = detail['Package Dimensions']
      weight = detail['Item Weight']
      asin = detail['ASIN']
      review_count = detail['Customer Reviews'].split('stars')[1].replace('\n', '').replace(' ', '').split('ratings')[0]

      try:
         bullet_list = container.find('div', id='feature-bullets').find_all('li')
      except Exception as e:
         print(f'bullleeettt:::::: {e}')
      about = []

      for b in bullet_list:
         about.append(b.find('span').get_text().strip())


      print(title)
      print(company_name)
      print(rating)
      print(price)
      print(variation_types)
      print(detail)
      print(date_first_available)
      print(package_dimensions)
      print(weight)
      print(about)
      print(pictures)
      print(video)
      print(asin)
      print(review_count)

      listing = AmzListing(
         asin=asin,
         title=title,
         company_name=company_name,
         variation_types=variation_types,
         rating=rating,
         price=price,
         package_dimensions=package_dimensions,
         review_count=review_count,
         weight=weight,
         date_first_available=date_first_available,
         about=about,
         pictures=pictures,
         video=video,
      )

      self.listing = listing


   def start(self): 
      amz_listing_service = AmzListingService()
      self.open_browser()

      try:
         self.scrap_data()
         amz_listing_service.insert_listing(self.listing)
      except Exception as e:
         print(f'scrap error {e}')