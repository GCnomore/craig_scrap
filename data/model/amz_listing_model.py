from datetime import datetime

class AmzListing:
    def __init__(
            self, 
            asin: str, 
            title: str, 
            company_name: str, 
            variation_types: list[str], 
            rating: str,
            price: str,
            package_dimensions: str, 
            review_count: int,
            weight: str,
            date_first_available: str,
            about: list[str],
            pictures: list[str],
            video: str = ''
         ):
        self.asin = asin
        self.title = title
        self.company_name = company_name
        self.variation_types = variation_types
        self.rating = rating
        self.price = price
        self.package_dimensions = package_dimensions
        self.review_count = review_count
        self.weight = weight
        self.date_first_available = date_first_available
        self.about = about
        self.pictures = pictures
        self.video = video

    def to_dict(self):
        return {
            'asin': self.asin,
            'title': self.title,
            'company_name': self.company_name,
            'variation_types': self.variation_types,
            'rating': self.rating,
            'price': self.price,
            'package_dimensions' : self.package_dimensions,
            'review_count': self.review_count,
            'weight': self.weight,
            'date_first_available': self.date_first_available,
            'about': self.about,
            'pictures': self.pictures,
            'video': self.video,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            asin = data.get('asin'),
            title = data.get('title'),
            company_name = data.get('company_name'),
            variation_types = data.get('variation_types'),
            rating = data.get('rating'),
            price = data.get('price'),
            package_dimensions = data.get('package_dimensions'),
            review_count = data.get('review_count'),
            weight = data.get('weight'),
            date_first_available = data.get('date_first_available'),
            about = data.get('about'),
            pictures = data.get('pictures'),
            video = data.get('video'),
            timestamp = data.get('timestamp')
        )
    
    def add_timestamp(self):
        self.timestamp = datetime.now()