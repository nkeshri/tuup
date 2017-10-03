#!/usr/bin/env python
__author__ = "Nimika Keshri"
__email__ = "nimika.keshri@gmail.com"

import json
import requests
import urllib

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

    def generateUrl(self):
        self.url = "https://{}/{}?{}" .format(self.host, self.api, urllib.urlencode(self.params))
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
        self.generateUrl()
        self.getRequest()
