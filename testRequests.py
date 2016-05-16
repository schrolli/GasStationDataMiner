# Modul: testRequests
# Date: 03.07.2015
# Author: dtonal - Torben Mueller <dtonal@posteo.de>
# Summary: Modul to do first request testing.
from apiRequests import apiRequests
import utils

import requests
import json
import doctest

utils.loggingMode=3

try:
    api = apiRequests('00000000-0000-0000-0000-000000000002')
    utils.logMessage("Testing detail request for gasstation with fix id")
    jsonData=api.detail("13e6cbc0-a11d-4b81-a3d1-ae048c14aaea")
    print(type(jsonData))
    utils.logMessage("Requesting details finished.")
    if jsonData is None:
        utils.logMessage("Error while requesting details.")
    else:
        utils.logMessage("Requesting details succeded.")
        utils.logRequestResponse(jsonData)
        
    utils.logMessage("Testing list request for gasstation with fix parameters")
    jsonData=api.list("49.56825", "10.96341", "10", "price", "diesel")
    utils.logMessage("Requesting list finished.")
    if jsonData is None:
        utils.logMessage("Error while requesting list.")
    else:
        utils.logMessage("Requesting list succeded.")
        utils.logRequestResponse(jsonData)
except Exception as exc:
        utils.logMessage("Exception while testing Requests: ", exc)
        raise SystemExit
