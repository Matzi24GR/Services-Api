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
