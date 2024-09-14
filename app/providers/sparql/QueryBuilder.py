import json

import yaml


def main():
    global counter
    with open('3.1.1-cpsv-ap.jsonld', 'r') as file:
        data = json.load(file)
        data = data['@context']

        with open("3.1.1-config.yaml", 'r') as config_file:
            config = yaml.load(config_file, yaml.FullLoader)

            target = get_uri_from_name(config['queries']['getServiceDetails']['target'][0], data)
            print("CONSTRUCT {")
            print(f"?id a <{target}>.")
            counter = 0
            for triple in generate_triple('id', config['queries']['getServiceDetails']['elements'], data, False):
                print(triple)
            print("} WHERE {")
            print(f"?id a <{target}>.")
            print("FILTER (regex(str(?id),\"917374\")).")
            counter = 0
            for triple in generate_triple('id', config['queries']['getServiceDetails']['elements'], data, True):
                print(triple)
            print("}")


def get_uri_from_name(name, cpsv):
    if name.startswith("CUSTOM="):
        return name.replace("CUSTOM=", "")
    elif isinstance(cpsv[name], dict):
        return cpsv[name]['@id']
    else:
        return cpsv[name]


def get_object():
    global counter
    counter += 1
    return f"property{counter}"


def generate_triple(subject, input_element, cpsv, add_optional):
    if isinstance(input_element, list):
        for item in input_element:
            yield from generate_triple(subject, item, cpsv, add_optional)

    elif isinstance(input_element, dict):
        key = list(input_element.keys())[0]
        predicate = get_uri_from_name(key, cpsv)
        object = get_object()

        if add_optional:
            yield "OPTIONAL {"

        yield f"?{subject} <{predicate}> ?{object}."
        yield from generate_triple(object, input_element[key], cpsv, add_optional)

        if add_optional:
            yield "}."

    elif isinstance(input_element, str):
        predicate = get_uri_from_name(input_element, cpsv)
        object = get_object()
        if add_optional:
            yield f"OPTIONAL {{ ?{subject} <{predicate}> ?{object} }}."
        else:
            yield f"?{subject} <{predicate}> ?{object}."

    else:
        raise Exception(f"Problem constructing triples in request, Element_type: {type(input_element)}")


if __name__ == '__main__':
    main()
