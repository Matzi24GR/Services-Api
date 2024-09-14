from abc import abstractmethod, ABC


class Provider(ABC):

    @abstractmethod
    def from_dict(cls, dict):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def get_services(self):
        pass

    @abstractmethod
    def get_service_details(self, id):
        pass

    @abstractmethod
    def get_outputs(self):
        pass

    @abstractmethod
    def get_organizations(self):
        pass

    @abstractmethod
    def get_evidences(self):
        pass

    @abstractmethod
    def get_requirements(self):
        pass

    @abstractmethod
    def get_rules(self):
        pass

    @abstractmethod
    def get_legal_resources(self):
        pass