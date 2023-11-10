import pymongo
from data.db.main import connect_mongodb
from pymongo.collection import Collection
from data.model.amz_listing_model import AmzListing

class AmzListingService:
   db: Collection

   def __init__(self) -> None:
      try:
         self.db = connect_mongodb()
      except Exception as e:
         print(f'db connect error {e}')
   


   def insert_listing(self, listing:AmzListing): 
      try:
         if self.db is not None:
            listing.add_timestamp()
            return self.db.insert_one(listing.to_dict())
      except Exception as e:
         print(f'insert error {e}')
