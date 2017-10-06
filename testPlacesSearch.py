import os
import unittest
import sys
from tuupapiutil import TuupPlacesApi

host = "devapi.tuup.fi"
apisearch = "places/v2/search"

class ApiSearchTest(unittest.TestCase):
    def setUp(self):
        self.client = TuupPlacesApi(host, apisearch)

    def test01_onlyCharacters(self):
        self.client.executeRequestWithParams(text="act")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['search']), 0, "No places found with the given search text")

    def test02_onlynumbersWithExistingPlaces(self):
        self.client.executeRequestWithParams(text="787")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['search']), 0, "No places found with the given search text")

    def test03_onlynumbersWithNoExistingPlaces(self):
        self.client.executeRequestWithParams(text="7282626")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['search']), 0, "places found with the given search text")

    def test04_specialCharctes(self):
        self.client.executeRequestWithParams(text="%&")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['search']), 0, "places found with the given search text")

    def test05_textAndLocation(self):
        self.client.executeRequestWithParams(text="nimika", at="61.44, 23.8")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['search']), 0, "No places found with the given search text")


if __name__ == "__main__":
    unittest.main()

