import requests

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
        query = "PREFIX+cpsv%3A%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fcpsv%23%3E+PREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E+SELECT+%3Fid+%3Fname+WHERE+%7B%3Fid+a+cpsv%3APublicService.+%3Fid+dct%3Atitle+%3Fname%7D+ORDER+BY+%3Fname"
        other_options = "&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on"

        data = requests.get(
            f"{self.url}/?default-graph-uri={self.graph_uri}&query={query}{other_options}")

        json = data.json()['results']['bindings']
        for item in json:
            id = item['id']['value']
            item.pop('id')
            item['id'] = id.split('/')[-1]
            name = item['name']['value']
            item.pop('name')
            item['name'] = name
            item['source'] = self.tag
        return json

    def get_service_details(self, id):
        query = f"PREFIX+cpsv%3A<http%3A%2F%2Fpurl.org%2Fvocab%2Fcpsv%23>%0D%0APREFIX+dct%3A+<http%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F>+%0D%0ASELECT+%3Fname+%3Fverb+%3Fobject%0D%0AWHERE+\u007b%0D%0A%3Fid+a+cpsv%3APublicService.%0D%0A%3Fid+dct%3Atitle+%3Fname.%0D%0A%3Fid+%3Fverb+%3Fobject.%0D%0AFILTER+(regex(str(%3Fid)%2C+\"{id}\"+))+%0D%0A\u007d"
        other_options = "&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on"
        data = requests.get(
            f"{self.url}/?default-graph-uri={self.graph_uri}&query={query}{other_options}")
        json = data.json()['results']['bindings']
        p_output = {"name": json[0]["name"]["value"]}
        for item in json:
            verb = item["verb"]["value"].split('/')[-1].split('#')[-1]
            object = item["object"]["value"].split('/')[-1].split('#')[-1]
            if verb in p_output.keys():
                if p_output[verb].__class__ == str:
                    p_output[verb] = [p_output[verb], object]
                elif p_output[verb].__class__ == list:
                    p_output[verb].append(object)
            else:
                p_output[verb] = object
        return p_output
