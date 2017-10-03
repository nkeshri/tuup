import os
import unittest
import sys
from tuupapiutil import TuupPlacesApi

host = "devapi.tuup.fi"
apiNearby = "places/v2/nearby"

class ApiNearbyTest(unittest.TestCase):
    def setUp(self):
        self.client = TuupPlacesApi(host, apiNearby)

    def test01_validLatLong_withplaces(self):
        self.client.addParams(at="61.44,23.8")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['places']), 0, "No places found nearby")

    def test02_validLatLong_withoutplaces(self):
        self.client.addParams(at="61.00,23.0")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['places']), 0, "places found at the location")

    def test03_invalidLatLong(self):
        self.client.addParams(at="test123")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['places']), 0, "places found at the location")

    def test04_eitherLatLong(self):
        self.client.addParams(at="61.44")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 500, "Request Succeeded")
        self.assertEqual(data['errorName'], "TopologyException", "places found at the location")

    def test05_onlyLatitudePair(self):
        """
        In this test scenario the latitude and longitude pair is passed in 
        such a way that there is no value provided for the longitude after
        the comma(,). This request returns an error. On the other hand, the next testcase 
        test06_onlyLongitudePair returns success in a similar scenario where the value of
        latitude is not provided before the comma(,). Both the test scenarios should behave 
        similarly, hence it is a bug in either case as per the specs.
        """
        self.client.addParams(at="61.44,")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 500, "Request Succeeded")
        self.assertEqual(data['errorName'], "TopologyException", "places found at the location")

    def test06_onlyLongitudePair(self):
        self.client.addParams(at=",23.8")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['places']), 0, "places found at the location")

    def test07_validLatLong_validRadius(self):
        self.client.addParams(at="61.44, 23.8", radius=5000)
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['places']), 0, "places found at the location")

    def test08_validLatLong_zeroRadius(self):
        self.client.addParams(at="61.44, 23.8", radius=0)
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['places']), 0, "places found at the location")

    def test09_validLatLong_negetiveRadius(self):
        self.client.addParams(at="61.44, 23.8", radius=-1000)
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['places']), 0, "places found at the location")

    def test10_validLatLong_invalidRadius(self):
        self.client.addParams(at="61.44, 23.8", radius="test123")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        self.assertEqual(status, 500, "Request Succeeded")
        self.assertEqual(data['errorName'], "Error", "places found at the location")

if __name__ == "__main__":
    unittest.main()

