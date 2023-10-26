class Que:
   def __init__(self): 
      self.raw_que = []
      self.batch_que = []
      self.batch_count = 1
   
   def add_que(self, item):
      self.raw_que.append(item)
      
      if(len(self.raw_que) == 50):
         self.batch_que.append(self.raw_que)
         self.batch_count += 1
         self.raw_que = []
         
         return {
            'batch': self.batch_count - 1,
            'index': 50
         }
      
      return {
         'batch': self.batch_count,
         'index': len(self.raw_que)
      }
   
   def deque(self):
      return 
   