import os
from urllib.error import HTTPError

import rdflib.term
from SPARQLWrapper import SPARQLWrapper, Wrapper
from rdflib import RDF
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
        self.sparql.addParameter("default-graph-uri", self.graph_uri)
        self.sparql.setReturnFormat(Wrapper.RDFXML)
        self.sparql.setMethod(Wrapper.POST)

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
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getServices').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_service_details(self, id):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getServiceDetails').add_filter(id).build()
        self.sparql.setQuery(query)
        response = self.get_response(query_builder.target)
        return response

    def get_outputs(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getOutputs').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_organizations(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getOrganizations').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_evidences(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getEvidences').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_requirements(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getRequirements').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_rules(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getRules').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)


    def get_legal_resources(self):
        query_builder = SparqlQueryBuilder(self.config, self.cpsv)
        query = query_builder.set_query('getLegalResources').build()
        self.sparql.setQuery(query)
        return self.get_response(query_builder.target)

    def get_response(self, target):
        try:
            response = self.sparql.queryAndConvert()
            for item in response.triples((None, RDF.type, rdflib.URIRef(target))):
                result = self.get_all_nested_child_triples(response, item[0])
                yield result
        except HTTPError:
            print(f"Failed to query {self.url}")

    def get_all_nested_child_triples(self, graph, subject):
        if isinstance(subject, rdflib.term.URIRef):
            result_dict = {'id': subject.replace(self.graph_uri, '')}
            for triple in graph.triples((subject, None, None)):
                next_level = self.get_all_nested_child_triples(graph, triple[2])
                if next_level == {}:
                    next_level = triple[2]
                predicate = str(triple[1])
                if predicate == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                    continue
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
