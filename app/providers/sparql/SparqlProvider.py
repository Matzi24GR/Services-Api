from urllib.error import HTTPError
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
        non_list_fields = ["identifier", "processing time", "status"]
        passed_sub_ids = []

        f = open("app/providers/sparql/service_details.sparql", "r")
        query = f.read().format(graph_uri=self.graph_uri, id=id)

        self.sparql.setQuery(query)
        self.sparql.setMethod("POST")
        try:
            response = self.sparql.queryAndConvert()['results']['bindings']

            if len(response) == 0:
                return None

            p_output = {}
            for item in response:
                field = item["field"]["value"]
                data = item["data"]["value"]
                sub_field = item.get("subField", {}).get("value", None)
                sub_id = item.get("subId", {}).get("value", None)
                if field in non_list_fields:
                    p_output[field] = data
                else:
                    if sub_field is not None:
                        if field not in p_output:
                            passed_sub_ids.append(sub_id)
                            p_output[field] = [{sub_field: data}]
                        else:
                            if sub_id in passed_sub_ids:
                                p_output[field][-1][sub_field] = data
                            else:
                                p_output[field].append({sub_field: data})
                    else:
                        if field not in p_output:
                            p_output[field] = [data]
                        else:
                            p_output[field].append(data)
            return p_output
        except HTTPError:
            print(f"Failed to query {self.url}")

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