import yaml
from .sparql.SparqlProvider import SparqlProvider


class ProviderFactory:

    @classmethod
    def _getProvider(cls, provider_dict):
        match provider_dict["type"]:
            case "sparql":
                return SparqlProvider.from_dict(provider_dict)
            case _:
                print("Type not recognised")

    @classmethod
    def read_providers(cls):
        providers = []
        with(open("./config.yaml", 'r')) as file:
            config = yaml.load(file, yaml.FullLoader)
            for item in config['providers']:
                providers.append(ProviderFactory._getProvider(item))
            return providers
