from urllib.error import HTTPError

import requests
from SPARQLWrapper import SPARQLWrapper, JSON

from ..Provider import Provider


class SparqlProvider(Provider):

    def __init__(self, type, name, tag, url, graph_uri):
        self.type = type
        self.name = name
        self.tag = tag
        self.url = url
        self.graph_uri = graph_uri

        self.sparql = SPARQLWrapper(self.url, self.graph_uri)
        self.sparql.setReturnFormat(JSON)

    @classmethod
    def from_dict(cls, dict):
        return SparqlProvider(type=dict['type'],
                              name=dict['name'],
                              tag=dict['tag'],
                              url=dict["url"],
                              graph_uri=dict["graph_uri"]
                              )

    def to_dict(self):
        return {"name": self.name, "type": self.type, "tag": self.tag, "url": self.url, "graph-uri": self.graph_uri}

    def get_services(self):
        query = f"""
            PREFIX cpsv:<http://purl.org/vocab/cpsv#>
            PREFIX dct: <http://purl.org/dc/terms/>
            
            WITH <{self.graph_uri}>
            SELECT DISTINCT ?id ?name
            WHERE {{
                ?id a cpsv:PublicService.
                ?id dct:title ?name}}
            ORDER BY ?name
        """
        self.sparql.setQuery(query)
        try:
            response = self.sparql.queryAndConvert()
            data = response['results']['bindings']
            for item in data:
                id = item['id']['value']
                item.pop('id')
                item['id'] = id.split('/')[-1]
                name = item['name']['value']
                item.pop('name')
                item['name'] = name
                item['provider'] = self.tag
            return data
        except HTTPError:
            print(f"Failed to query {self.url}")

    def get_service_details(self, id):

        # Double curly brackets to escape them ( {{, }} )
        query = f"""
            PREFIX cpsv:<http://purl.org/vocab/cpsv#>
            PREFIX dct:<http://purl.org/dc/terms/>
            
            SELECT ?name ?verb ?object
            WHERE {{?id a cpsv:PublicService.
                ?id dct:title ?name.
                ?id ?verb ?object.
            FILTER (regex(str(?id),"{id}"))
            }}
        """

        payload = {
            'default-graph-uri': self.graph_uri,
            'query': query,
            'format': 'application/sparql-results+json'
        }
        response = requests.get(self.url, payload)

        if response.status_code != 200:
            print(f"Can't reach {self.url}, Status Code: [{response.status_code}]'")
            return

        json = response.json()['results']['bindings']

        if len(json) == 0:
            return None

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
