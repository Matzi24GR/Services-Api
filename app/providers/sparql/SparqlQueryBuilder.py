import yaml
import json


class SparqlQueryBuilder:
    def __init__(self, config, cpsv):
        self.query = None
        self.target = None
        self._counter = 0
        self.config = config
        self.cpsv = cpsv

    def set_query(self, query_name):
        construct = self.get_segment('CONSTRUCT', query_name)
        construct = '\n'.join(construct)

        where = self.get_segment('WHERE', query_name)
        where = '\n'.join(where)
        self.query = f"{construct}\n{where}"

        return self

    def build(self):
        return self.query

    def get_segment(self, segment, query_name):
        config = self.config['queries'][query_name]
        self.target = self._get_uri_from_name(config['target'], self.cpsv)
        yield f"{segment} {{"
        yield f"?id a <{self.target}>."
        self._counter = 0
        yield from self._generate_triple('id', config['elements'], self.cpsv, segment == 'WHERE')
        yield "}"

    def add_filter(self, id):
        pattern = f"WHERE {{\n?id a <{self.target}>."
        self.query = self.query.replace(pattern, f"{pattern}\nFILTER (regex(str(?id),\"{id}\")).")
        return self

    def _generate_triple(self, subject, input_element, cpsv, add_optional):
        if isinstance(input_element, list):
            for item in input_element:
                yield from self._generate_triple(subject, item, cpsv, add_optional)

        elif isinstance(input_element, dict):
            key = list(input_element.keys())[0]
            predicate = self._get_uri_from_name(key, cpsv)
            object = self._get_object()

            if add_optional:
                yield "OPTIONAL {"

            yield f"?{subject} <{predicate}> ?{object}."
            yield from self._generate_triple(object, input_element[key], cpsv, add_optional)

            if add_optional:
                yield "}."

        elif isinstance(input_element, str):
            predicate = self._get_uri_from_name(input_element, cpsv)
            object = self._get_object()
            if add_optional:
                yield f"OPTIONAL {{ ?{subject} <{predicate}> ?{object} }}."
            else:
                yield f"?{subject} <{predicate}> ?{object}."

        else:
            raise Exception(f"Problem constructing triples in request, Element_type: {type(input_element)}")

    def _get_object(self):
        self._counter += 1
        return f"property{self._counter}"

    def _get_uri_from_name(self, name, cpsv):
        if name.startswith("CUSTOM="):
            return name.replace("CUSTOM=", "")
        elif isinstance(cpsv[name], dict):
            return cpsv[name]['@id']
        else:
            return cpsv[name]

