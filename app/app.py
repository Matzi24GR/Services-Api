from flask import Flask, jsonify, abort, render_template
from models.ProviderFactory import ProviderFactory

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('swaggerui.html')


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
        services = provider.get_services()
        if services is not None:
            merged += services
    return merged


@app.route('/services/<id>')
def get_cpsv_service_details(id):
    output = []
    providers = ProviderFactory.read_providers()
    for provider in providers:
        p_output = provider.get_service_details(id)
        if p_output is not None:
            output.append({"provider": provider.name, "results": p_output})
    if len(output) == 0:
        abort(404)
    return output


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
