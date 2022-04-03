from abc import ABC, abstractmethod


class Manager(ABC):
    @property
    @abstractmethod
    def ID(self):
        pass
    
    @abstractmethod
    def parse_events(self, events):
        pass