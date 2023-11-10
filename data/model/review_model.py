from datetime import datetime

class Review:
    def __init__(self, id: str, title: str, name: str, date: str, rating: str, vp: bool, country: str, review: str, pictures: list[str], video: str = ''):
        self.id = id
        self.title = title
        self.name = name
        self.date = date
        self.rating = rating
        self.vp= vp
        self.country = country
        self.review = review
        self.pictures = pictures
        self.video = video

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'date': self.date,
            'rating': self.rating,
            'vp': self.vp,
            'country' : self.country,
            'review': self.review,
            'pictures': self.pictures,
            'video': self.video,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data.get('id'),
            title = data.get('title'),
            name = data.get('name'),
            date = data.get('date'),
            rating = data.get('rating'),
            vp = data.get('vp'),
            country = data.get('country'),
            review = data.get('review'),
            pictures = data.get('pictures'),
            video = data.get('video'),
            timestamp = data.get('timestamp')
        )
    
    def add_timestamp(self):
        self.timestamp = datetime.now()