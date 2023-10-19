from config.app_config import AppConfig
from scrapper.scrapper import Scrapper

app_config = AppConfig()
config = app_config.get_config()

scrapper = Scrapper(config)
scrapper.load_browser('https://losangeles.craigslist.org/search/aos#search=1~gallery~0~0')



print(config)
print(scrapper)