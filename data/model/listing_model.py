class Listing:
    def __init__(self, id: str = '', title: str = '', url: str = '', date: str = '', pics: list[str] = [], price: str = '', odometer: str = ''):
        self.id = id
        self.title = title
        self.url = url
        self.date = date
        self.pics = pics
        self.price = price
        self.odometer = odometer

    def to_dict(self):
        return {
            'id': self.trim,
            'title': self.title,
            'url': self.url,
            'date': self.date,
            'pics': self.pics,
            'price': self.price,
            'odometer': self.odometer
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id = data.get('id'),
            title = data.get('title'),
            url = data.get('url'),
            date = data.get('date'),
            pics = data.get('pics'),
            price = data.get('price'),
            odomoeter = data.get('odometer')
        )