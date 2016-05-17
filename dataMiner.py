# Modul: dataMiner
# Date: 13.07.2015
# Author: dtonal - Torben Mueller <dtonal@posteo.de>, Eugen Geist
# Summary: Modul to do first request testing.
import sys
import os
import logging
import logging.config

from apiRequests import apiRequests
from mongoConnector import mongoConnector

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
    try:
        db = mongoConnector(config['mongo'])
    except Exception as e:
        logger.critical("Cannot connect to db, exiting")
        sys.exit("Cannot connect to db.")
    for station in stationList:
        if db.updateStation(station) is False:
            sys.exit("Cannot update Station in database. See logs for details.")

if __name__ == "__main__":
    logger = logging.getLogger('miner')
    logger.info("Start mining")
    logger.info("Establishing DB connection")
    try:
        db = mongoConnector(config['mongo'])
    except Exception as e:
        logger.critical("Cannot connect to db, exiting")
        sys.exit("Cannot connect to db.")
    logger.info("Connect DB - getting handle successfully")
    api = apiRequests(config['apikey'])
    try:
        #Getting a list of all stations in in the db
        stations= db.getAllStationIds()
        for i in stations:
            #iterate trough all stations and do a detailRequest
            logger.info("Getting details for stationId = " + i)
            detailRequestResult = api.detail(i)
            if detailRequestResult is not None:
                for type in ['diesel','e5','e10']:
                    if type in detailRequestResult["station"]:
                        db.updatePrice(i,type,detailRequestResult["station"][type])
        logger.info("Finished mining at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    except Exception as exc:
        logger = logging.getLogger('database')
        logger.exception("Exception while trying to act on db.")
        raise SystemExit
