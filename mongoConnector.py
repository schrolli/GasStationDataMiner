import os
import datetime
import logging
import logging.config

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from dbConnector import dbConnector

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig('logging.conf')

class mongoConnector(dbConnector):

    def __init__(self, config):
        logger = logging.getLogger('database')
        """ Connect to MongoDB """
        try:
            self.client = MongoClient(config['host'], config['port'])
            logger.info("Connected successfully")
        except ConnectionFailure as e:
            logger.exception("Could not connect to MongoDB.")
            raise
        # getting a datebase handle to the db
        self.handle = self.client[config['db']]
    
    def getAllStationIds(self):
        return self.handle.stations.find()
    
    def updatePrice(self, id, type, price):
        try:
            logger = logging.getLogger('miner')
            filteredResult = dict()
            filteredResult["dateTime"] = datetime.datetime.now()
            filteredResult["stationId"] = id
            filteredResult["price"] = price
            if type == "diesel":
                self.handle.dieselPrices.insert_one(filteredResult)
                logger.info("diesel added")
            if type == "e5":
                self.handle.e5Prices.insert_one(filteredResult)
                logger.info("e5 added")
            if type == "e10":
                self.handle.e10Prices.insert_one(filteredResult)
                logger.info("e10 added")
        except Exception as e:
            logger = logging.getLogger('database')
            logger.exception("Exception while trying to add Price. id: %s, type: %s, price: %s, exception-message: %s" % (id, type, price, e))
            return False
        return True
    
    def updateStation(self, values):
        logger = logging.getLogger('miner')
        logger.info("Preparing data of " + values["name"] + " for insertion")
        values["_id"] = values["id"]
        del values["id"]
        del values["dist"]
        del values["price"]
        logger.info("Inserting station data of " + values["name"] + " to db")
        try:
            #If data for this station already exists replace, else insert
            self.handle.stations.replace_one({"_id" : values["_id"]},  values, upsert=True)
            logger.info("Station " + values["name"] + " added")
        except Exception as exc:
            logger = logging.getLogger('database')
            logger.exception("Exception while inserting station data in db.")
            return False
        return True
