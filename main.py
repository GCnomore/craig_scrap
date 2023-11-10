from config.app_config import AppConfig
from scrapper.amz_review_scrapper import AmzReviewScrapper
from scrapper.craig_scrapper import Scrapper
from scrapper.amz_listing_scrapper import AmzListingScrapper

# app_config = AppConfig()
# config = app_config.get_config()

# scrapper = Scrapper(config)
# # Default options - Hide duplicates, has images, has price
# scrapper.load_browser('https://losangeles.craigslist.org/search/cta?bundleDuplicates=1&hasPic=1&min_price=1#search=1~gallery~0~0')


# print(config)
# print(scrapper)

# https://losangeles.craigslist.org/search/bbb?query=7680244613

# amz_scrapper = AmzReviewScrapper('https://www.amazon.com/Apple-iPhone-11-64GB-Black/product-reviews/B07ZPKN6YR/ref=cm_cr_arp_d_viewopt_mdrvw?ie=UTF8&reviewerType=all_reviews&pageNumber=1&mediaType=media_reviews_only')
# amz_scrapper = AmzReviewScrapper('https://www.amazon.com/Apple-iPhone-11-64GB-Black/product-reviews/B07ZPKN6YR/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=2&mediaType=media_reviews_only')
amz_scrapper = AmzListingScrapper('https://www.amazon.com/TAURI-iPhone-15-Pro-Not-Yellowing/dp/B0CBBKM879/ref=sr_1_3?crid=1F0QBW1XL4H0G&keywords=iphone%2B15%2Bpro%2Bcase&qid=1699386911&sprefix=ipohone15%2Caps%2C263&sr=8-3&th=1')

amz_scrapper.start()