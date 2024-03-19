import os
from urllib.error import HTTPError

import rdflib.term
from SPARQLWrapper import JSON, SPARQLWrapper, Wrapper
from rdflib import RDF, Namespace
import yaml
import json

from .SparqlQueryBuilder import SparqlQueryBuilder
from ..Provider import Provider


class SparqlProvider(Provider):

    def __init__(self, type, name, tag, url, graph_uri, cpsv_version):
        self.type = type
        self.name = name
        self.tag = tag
        self.url = url
        self.graph_uri = graph_uri
        self.cpsv_version = cpsv_version

        current_working_directory = os.getcwd()
        print(current_working_directory)
        with open(f"app/providers/sparql/data/{cpsv_version}-config.yaml") as config_file:
            self.config = yaml.load(config_file, yaml.FullLoader)
        with open(f"app/providers/sparql/data/{cpsv_version}-cpsv-ap.jsonld") as cpsv_file:
            self.cpsv = json.load(cpsv_file)['@context']

        self.sparql = SPARQLWrapper(self.url, self.graph_uri)
        self.sparql.setReturnFormat(JSON)

    @classmethod
    def from_dict(cls, dict):
        return SparqlProvider(type=dict['type'],
                              name=dict['name'],
                              tag=dict['tag'],
                              url=dict["url"],
                              graph_uri=dict["graph_uri"],
                              cpsv_version=dict["cpsv_version"]
                              )

    def to_dict(self):
        return {"name": self.name, "cpsv_version": self.cpsv_version, "type": self.type, "tag": self.tag,
                "url": self.url, "graph-uri": self.graph_uri}

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
        self.sparql.setReturnFormat(JSON)
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
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getServiceDetails').add_filter(id).build()
        self.sparql.addParameter("default-graph-uri", self.graph_uri)
        self.sparql.setReturnFormat(Wrapper.RDFXML)
        self.sparql.setMethod(Wrapper.POST)
        self.sparql.setQuery(query)
        try:
            response = self.sparql.queryAndConvert()
            for publicService in response.triples((None, RDF.type, rdflib.URIRef(query_builder.target))):
                result = self.getAllNestedChildTriples(response, publicService[0])
                return result
        except HTTPError:
            print(f"Failed to query {self.url}")

    @classmethod
    def getAllNestedChildTriples(self, graph, subject):
        if isinstance(subject, rdflib.term.URIRef):
            result_dict = {}
            for triple in graph.triples((subject, None, None)):
                next_level = self.getAllNestedChildTriples(graph, triple[2])
                if next_level == {}:
                    next_level = triple[2]
                predicate = str(triple[1])
                if predicate in result_dict:
                    if isinstance(result_dict[predicate], list):
                        result_dict[predicate].append(next_level)
                    else:
                        result_dict[predicate] = [result_dict[predicate], next_level]
                else:
                    result_dict[predicate] = next_level
            return result_dict
        elif isinstance(subject, rdflib.term.Literal):
            return str(subject)
        else:
            return "this shouldn't ever happen"


    def get_outputs(self):
        query = f"""
            PREFIX cpsv:<http://purl.org/vocab/cpsv#>
            PREFIX m8g:<http://data.europa.eu/m8g/>
            PREFIX dc:<http://purl.org/dc/terms/>
            
            SELECT DISTINCT ?output ?outputTitle ?service ?serviceTitle 
            WHERE {{
                ?service cpsv:produces ?output.
                ?output dc:title ?outputTitle.
                ?service dc:title ?serviceTitle
            }}
        """
        self.sparql.setQuery(query)
        try:
            response = self.sparql.queryAndConvert()['results']['bindings']
            for item in response:
                id = item['output']['value']
                item.pop('output')
                item['id'] = id.split('/')[-1]
                name = item['outputTitle']['value']
                item.pop('outputTitle')
                item['name'] = name
                item['provider'] = self.tag
                service_id = item['service']['value'].split('/')[-1]
                service_name = item['serviceTitle']['value']
                item.pop('service')
                item.pop('serviceTitle')
                item['service'] = {}
                item['service']['id'] = service_id
                item['service']['name'] = service_name
            return response
        except HTTPError:
            print(f"Failed to query {self.url}")
