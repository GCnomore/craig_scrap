from config.app_config import AppConfig
from scrapper.scrapper import Scrapper

# app_config = AppConfig()
# config = app_config.get_config()

scrapper = Scrapper()
scrapper.load_browser('https://losangeles.craigslist.org/search/cta?bundleDuplicates=1&hasPic=1&min_price=1#search=1~gallery~0~0')
