from flask import Flask, jsonify
import requests
import csv
import urllib.parse

app = Flask(__name__)


class Provider:

    def __init__(self, name, tag, url):
        self.name = name
        self.tag = tag
        self.url = url

    def to_dict(self):
        return {"name": self.name, "tag": self.tag, "url": self.url}


def read_providers():
    providers = []
    with(open("./providers.csv", 'r')) as file:
        reader = csv.reader(file)
        for row in reader:
            providers.append(Provider(row[0], row[1], row[2]))
        return providers


@app.route('/')
def main():
    return 'Default'


@app.route('/providers')
def get_providers():
    providers = read_providers()
    providers_dict = []
    for p in providers:
        providers_dict.append(p.to_dict())
    return jsonify(providers_dict)


@app.route('/services')
def get_cpsv_services():
    providers = read_providers()
    merged = []
    graph_uri = "http://data.dai.uom.gr:8890/CPSV-AP"
    query = "PREFIX+cpsv%3A%3Chttp%3A%2F%2Fpurl.org%2Fvocab%2Fcpsv%23%3E+PREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E+SELECT+%3Fid+%3Fname+WHERE+%7B%3Fid+a+cpsv%3APublicService.+%3Fid+dct%3Atitle+%3Fname%7D+ORDER+BY+%3Fname"
    other_options = "&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on"
    for provider in providers:
        data = requests.get(
            f"{provider.url}/?default-graph-uri={graph_uri}&query={query}{other_options}")
        json = data.json()['results']['bindings']
        for item in json:
            id = item['id']['value']
            item.pop('id')
            item['id'] = id.split('/')[-1]
            name = item['name']['value']
            item.pop('name')
            item['name'] = name
            item['source'] = provider.tag
        merged.append(json)
    return merged


@app.route('/services/<id>')
def get_cpsv_service_details(id):
    providers = read_providers()
    graph_uri = "http://data.dai.uom.gr:8890/CPSV-AP"
    query = f"PREFIX+cpsv%3A<http%3A%2F%2Fpurl.org%2Fvocab%2Fcpsv%23>%0D%0APREFIX+dct%3A+<http%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F>+%0D%0ASELECT+%3Fname+%3Fverb+%3Fobject%0D%0AWHERE+\u007b%0D%0A%3Fid+a+cpsv%3APublicService.%0D%0A%3Fid+dct%3Atitle+%3Fname.%0D%0A%3Fid+%3Fverb+%3Fobject.%0D%0AFILTER+(regex(str(%3Fid)%2C+\"{id}\"+))+%0D%0A\u007d"
    other_options = "&format=application%2Fsparql-results%2Bjson&should-sponge=&timeout=0&signal_void=on"
    output = []
    for provider in providers:
        p_output = {}
        data = requests.get(
            f"{provider.url}/?default-graph-uri={graph_uri}&query={query}{other_options}")
        json = data.json()['results']['bindings']
        p_output["name"] = json[0]["name"]["value"]
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
        output.append({"provider": provider.name, "results": p_output})
    return output


if __name__ == '__main__':
    app.run()
