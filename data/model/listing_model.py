class Listing:
    def __init__(self, title: str, url: str, date: str, pics: list[str], desc: str):
        self.title = title
        self.url = url
        self.date = date
        self.pics = pics
        self.desc = desc

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'date': self.date,
            'pics': self.pics,
            'desc': self.desc
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title = data.get('title'),
            url = data.get('url'),
            date = data.get('date'),
            pics = data.get('pics'),
            desc = data.get('desc')
        )