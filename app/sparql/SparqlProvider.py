from app.models.Provider import Provider


class SparqlProvider(Provider):

    def __init__(self, type, name, tag, url):
        self.type = type
        self.name = name
        self.tag = tag
        self.url = url

    @classmethod
    def from_dict(cls, dict):
        tag = list(dict.keys())[0]
        data = dict[tag]
        return SparqlProvider(type=data['type'],
                        name=data['name'],
                        tag=tag,
                        url=data["url"]
                        )

    def to_dict(self):
        return {"name": self.name, "type": self.type, "tag": self.tag, "url": self.url}

    def get_services(self):
        pass