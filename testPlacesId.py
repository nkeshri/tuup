import os
import unittest
import sys
from tuupapiutil import TuupPlacesApi

host = "devapi.tuup.fi"
apiplaceId = "places/v2/nearby"

class ApiPlaceIdTest(unittest.TestCase):
    def setUp(self):
        self.client = TuupPlacesApi(host, apiplaceId)

    def test01_validPlaceId(self):
        self.client.generateUrlWithArg("24rent:166")
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(data['id'], "24rent:166", "No places found nearby")

    def test02_validStopId(self):
        self.client.generateUrlWithArg("digitransitStop:tampere:3611")
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 404, "Request Succeeded")
        self.assertEqual(data['errorName'], "NotFoundError", "places found at the location")

    def test03_invalidPlaceId(self):
        self.client.generateUrlWithArg("3611")
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 404, "Request Succeeded")
        self.assertEqual(data['errorName'], "NotFoundError", "places found at the location")

if __name__ == "__main__":
    unittest.main()

