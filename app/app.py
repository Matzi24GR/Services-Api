from flask import Flask, jsonify
from .ProviderFactory import ProviderFactory

app = Flask(__name__)


@app.route('/')
def main():
    return 'Default'


@app.route('/providers')
def get_providers():
    providers = ProviderFactory.read_providers()
    providers_dict = []
    for p in providers:
        providers_dict.append(p.to_dict())
    return jsonify(providers_dict)


@app.route('/services')
def get_cpsv_services():
    providers = ProviderFactory.read_providers()
    merged = []
    for provider in providers:
        json = provider.get_services()
        merged.append(json)
    return merged


@app.route('/services/<id>')
def get_cpsv_service_details(id):
    output = []
    providers = ProviderFactory.read_providers()
    for provider in providers:
        p_output = provider.get_service_details(id)
        output.append({"provider": provider.name, "results": p_output})
    return output


if __name__ == '__main__':
    app.run()
