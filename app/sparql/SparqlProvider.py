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
        query = """
            PREFIX cpsv:<http://purl.org/vocab/cpsv#>
            PREFIX dct: <http://purl.org/dc/terms/>
            
            SELECT ?id ?name
            WHERE {
                ?id a cpsv:PublicService.
                ?id dct:title ?name}
            ORDER BY ?name
        """

        payload = {
            'default-graph-uri': self.graph_uri,
            'query': query,
            'format': 'application/sparql-results+json'
        }
        data = requests.get(self.url, payload)

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

        # Double curly brackets to escape them ( {{, }} )
        query = '''
            PREFIX cpsv:<http://purl.org/vocab/cpsv#>
            PREFIX dct:<http://purl.org/dc/terms/>
            
            SELECT ?name ?verb ?object
            WHERE {{?id a cpsv:PublicService.
                ?id dct:title ?name.
                ?id ?verb ?object.
            FILTER (regex(str(?id),"{id}"))
            }}
        '''.format(id=id)

        payload = {
            'default-graph-uri': self.graph_uri,
            'query': query,
            'format': 'application/sparql-results+json'
        }
        data = requests.get(self.url, payload)

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
