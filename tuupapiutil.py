#!/usr/bin/env python
__author__ = "Nimika Keshri"
__email__ = "nimika.keshri@gmail.com"

import json
import requests
import urllib
from math import radians, cos, sin, asin, sqrt


class TuupPlacesApi:
    """
    The class that takes care of url requests for places API for tuup.fi
    """

    def __init__(self, host, api):
        self.api = api
        self.host = host
        self.params = {}

    def addParams(self, **kwargs):
        for k, v in kwargs.iteritems():
            self.params[k] = v
        return

    def generateUrlWithParam(self):
        self.url = "https://{}/{}?{}" .format(self.host, self.api, urllib.urlencode(self.params))
        print("The generated Url is : %s" %self.url)
        return

    def generateUrlWithArg(self, arg):
        self.url = "https://{}/{}/{}" .format(self.host, self.api, arg)
        print("The generated Url is : %s" %self.url)
        return

    def getRequest(self):
        self.response = requests.get(self.url)
        return

    def parseJson(self):
        status = self.response.status_code
        content = json.loads(self.response.text)
        return status, content

    def executeRequestWithParams(self, **kwargs):
        self.addParams(**kwargs)
        self.generateUrlWithParam()
        self.getRequest()

    def calcDistanceUsinghaversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km
