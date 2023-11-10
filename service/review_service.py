import pymongo
from data.db.main import connect_mongodb
from pymongo.collection import Collection
from data.model.review_model import Review

class ReviewService:
   db: Collection

   def __init__(self) -> None:
      try:
         self.db = connect_mongodb()
      except Exception as e:
         print(f'db connect error {e}')
   


   def insert_reviews(self, reviews: list[Review]): 
      que = []

      for r in reviews:
         r.add_timestamp()
         que.append(r.to_dict())

      try:
         if self.db is not None:
            return self.db.insert_many(que)
      except Exception as e:
         print(f'insert error {e}')



   def get_most_recent_review(self):
      try:
         return self.db.find().sort([("timestamp_field", pymongo.DESCENDING)]).limit(1)
      except Exception as e:
         print(f'get_most_recent_review error ${e}')