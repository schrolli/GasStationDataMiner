# Modul: dataMiner
# Date: 13.07.2015
# Author: dtonal - Torben Mueller <dtonal@posteo.de>, Eugen Geist
# Summary: Modul to do first request testing.
import sys
import os
import datetime
import requests
import doctest
import logging
import logging.config

from apiRequests import apiRequests
import connectDb

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig('logging.conf')

config = {}
exec(open("main.conf").read(), config)

def addStationsInLocationToDb(lat, lng, rad):
    logger = logging.getLogger('miner')
    logger.info("Requesting station list for lat: " + "{:.9f}".format(lat) + "long: " + "{:.9f}".format(lng) +  " and rad: " + "{:.9f}".format(rad))
    #Get Station data
    api = apiRequests(config['apikey'])
    stationList = api.list(lat, lng, rad)["stations"]
    dbHandle = connectDb.connect()
    if dbHandle is None:
        logger.critical("Cannot connect to db, exiting")
        sys.exit("Cannot connect to db.")
    for station in stationList:
        #Format for Database
        logger.info("Preparing data of " + station["name"] + " for insertion")
        station["_id"] = station["id"]
        del station["id"]
        del station["dist"]
        del station["price"]
        logger.info("Inserting station data of " + station["name"] + " to db")
        try:
            #If data for this station already exists replace, else insert
            dbHandle.stations.replace_one({"_id" : station["_id"]},  station, upsert=True)
            logger.info("Station " + station["name"] + " added")
        except Exception as exc:
            logger = logging.getLogger('database')
            logger.exception("Exception while inserting station data in db.")
            raise SystemExit

if __name__ == "__main__":
    logger = logging.getLogger('miner')
    logger.info("Start mining")
    logger.info("Establishing DB connection")
    dbHandle = connectDb.connect()
    if dbHandle is None:
        logger.critical("Cannot connect to db, exiting")
        sys.exit("Cannot connect to db.")
    logger.info("Connect DB - getting handle successfully")
    api = apiRequests(config['apikey'])
    try:
        #Getting a list of all stations in in the db
        stations= dbHandle.stations.find()
        for i in stations:
            #iterate trough all stations and do a detailRequest
            logger.info("Getting details for stationId = " + i["_id"])
            detailRequestResult = api.detail(i["_id"])
            if detailRequestResult is not None:
                #build and add generally data to filtered result dict
                filteredResult = dict()
                filteredResult["dateTime"] = datetime.datetime.now()
                filteredResult["stationId"] = i["_id"]
                if "diesel" in detailRequestResult["station"]:
                    #create a diesel price document
                    filteredResult["price"] =  detailRequestResult["station"]["diesel"]
                    dbHandle.dieselPrices.insert_one(filteredResult)
                    logger.info("diesel added")
                if "e5" in detailRequestResult["station"]:
                    #reuse diesel price document for e5 doc
                    filteredResult["price"] =  detailRequestResult["station"]["e5"]
                    dbHandle.e5Prices.insert_one(filteredResult)
                    logger.info("e5 added")
                if "e10" in detailRequestResult["station"]:
                    #reuse e5 price document for e10 doc
                    filteredResult["price"] =  detailRequestResult["station"]["e10"]
                    dbHandle.e10Prices.insert_one(filteredResult)
                    logger.info("e10 added")
        logger.info("Finished mining at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    except Exception as exc:
        logger = logging.getLogger('database')
        logger.exception("Exception while trying to act on db.")
        raise SystemExit
        
        
