from abc import ABC, abstractmethod


class Driver(ABC):

    @abstractmethod
    def get_project_services(self) -> dict:
        pass

    @abstractmethod
    def get_service_by_name(self, name: str) -> dict:
        pass

    @abstractmethod
    def run(self):
        pass