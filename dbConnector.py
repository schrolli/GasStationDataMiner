from abc import ABCMeta, abstractmethod



class dbConnector(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config):
        pass
        
    @abstractmethod
    def getAllStationIds(self):
        pass
        
    @abstractmethod
    def updatePrice(self, id, type, price):
        pass
        
    @abstractmethod
    def updateStation(self, values):
        pass
