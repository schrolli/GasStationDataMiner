# Modul: apiRequests
# Date: 03.07.2015
# Author: dtonal - Torben Mueller <dtonal@posteo.de>
# Summary: Modul to do detail- or list-requests on the tankerkoenig api.
import os
import requests
import doctest
import logging
import logging.config
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig('logging.conf')

class apiRequests:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.listRequestUrl = "https://creativecommons.tankerkoenig.de/json/list.php"
        self.detailRequestUrl = "https://creativecommons.tankerkoenig.de/json/detail.php"
        self.pricesRequestUrl = "https://creativecommons.tankerkoenig.de/json/prices.php"
        self.logger = logging.getLogger('apiRequests')
        
    def detail(self, gasStationId):
        '''Request detail information for a gasstation.
        
        Keyword arguments:
        gasStationId -- api id of the gasstation
        
        Returns: json or None
        
        '''
        try:
            self.logger.info("Building parameter for detail request")
            payload = {'id': gasStationId, 'apikey': self.apiKey}
            #logger.debug("Payload: " + payload)
            self.logger.info("Requesting details in progress...")
            self.logger.info("url: %s" % self.detailRequestUrl)
            self.logger.info("payload.id: %s" % payload["id"])
            self.logger.info("payload.apikey: %s" % payload["apikey"])
            response = requests.get(self.detailRequestUrl, params=payload)
            self.logger.info("request done")
            return self._checkResponseAndReturnJson(response)
        except Exception as e:
            self.logger.exception("Exception when requesting details for station with id %s:" % gasStationId)
            self.logger.exception("%s" % e)
            return None
            
    def prices(self, gasStationIds):
        '''Request prices for up to 10 gasstations.
        
        Keyword arguments:
        gasStationIds -- list of api ids of the gasstations, up to 10 items
        
        Returns: json or None
        
        '''
        try:
            self.logger.info("Building parameter for detail request")
            stationString = json.dumps(gasStationIds)
            payload = {'ids': stationString, 'apikey': self.apiKey}
            #self.logger.debug("Payload: " + payload)
            self.logger.info("Requesting details in progress...")
            self.logger.info("url: %s" % self.pricesRequestUrl)
            self.logger.info("payload.ids: %s" % payload["ids"])
            self.logger.info("payload.apikey: %s" % payload["apikey"])
            response = requests.get(self.pricesRequestUrl, params=payload)
            self.logger.info("request done")
            return self._checkResponseAndReturnJson(response)
        except Exception as e:
            self.logger.exception("Exception when requesting prices for stations with ids %s:" % gasStationIds)
            self.logger.exception("%s" % e)
            return None
            
    def list(self, lat, lng, rad, sort="price", type="e10"):
        '''Request nearby gasstations.
        
        Keyword arguments:
        lat -- Latitude of location
        lng -- Longitude of location
        rad -- Radius of request
        sort -- "distance" or "price"
        type -- "e10", "e5", "diesel" or "all"
        
        Returns: json or None
         
        '''
        try:
            self.logger.info("Building parameter for list request")
            payload = {'lat': lat, 'lng': lng,'rad': rad,'sort': sort,'type': type, 'apikey': self.apiKey}
            self.logger.info("Requesting nearby list")
            response = requests.get(self.listRequestUrl, params=payload)
            self.logger.info("request done")
            return self._checkResponseAndReturnJson(response)
        except Exception as e:
            self.logger.exception("Exception when requesting nearby stations:")
            self.logger.exception("%s" % e)
            return None
            
    def _checkResponseAndReturnJson(self, response):
        try:
            response.raise_for_status()
        except Exception as e:
            logger.error("Response was not ok: %s" % e)
            return None
        data = response.json()
        if (data['ok'] == True):
            return data
        else:
            self.logger.error("Api Error: " + data['message'])
            return None
            
