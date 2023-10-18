import os
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
                ?id dct:title ?name
            }} 
            ORDER BY ?name
        """
        self.sparql.setQuery(query)
        try:
            response = self.sparql.queryAndConvert()['results']['bindings']
            for item in response:
                id = item['id']['value']
                item.pop('id')
                item['id'] = id.split('/')[-1]
                name = item['name']['value']
                item.pop('name')
                item['name'] = name
                item['provider'] = self.tag
            return response
        except HTTPError:
            print(f"Failed to query {self.url}")

    def get_service_details(self, id):

        f = open("app/models/sparql/query.sparql", "r")
        query = f.read().format(graph_uri=self.graph_uri, id=id)

        self.sparql.setQuery(query)
        try:
            response = self.sparql.queryAndConvert()['results']['bindings']

            if len(response) == 0:
                return None

            p_output = {}
            for item in response:
                field = item["field"]["value"].split('/')[-1].split('#')[-1]
                data = item["data"]["value"].split('/')[-1].split('#')[-1]
                if field in p_output.keys():
                    if p_output[field].__class__ == str:
                        p_output[field] = [p_output[field], data]
                    elif p_output[field].__class__ == list:
                        p_output[field].append(data)
                else:
                    p_output[field] = data
            return p_output
        except HTTPError:
            print(f"Failed to query {self.url}")
