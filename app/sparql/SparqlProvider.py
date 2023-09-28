from app.models.Provider import Provider


class SparqlProvider(Provider):

    def __init__(self, type, name, tag, url, graph_uri):
        self.type = type
        self.name = name
        self.tag = tag
        self.url = url
        self.graph_uri = graph_uri

    @classmethod
    def from_dict(cls, dict):
        tag = list(dict.keys())[0]
        data = dict[tag]
        return SparqlProvider(type=data['type'],
                              name=data['name'],
                              tag=tag,
                              url=data["url"],
                              graph_uri=data["graph_uri"]
                              )

    def to_dict(self):
        return {"name": self.name, "type": self.type, "tag": self.tag, "url": self.url, "graph-uri": self.graph_uri}

    def get_services(self):
        pass
