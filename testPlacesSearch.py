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
        """
        In this test scenario the search criteria is taking location along with
        the search text, but looks like it is not taking into account the location because
        this is returning values matching all over the world. This API should either have 
        a third argument as radius, or there is a bug in the implementation. It is right now
        showing places 5000 kms away from the given location, hence the test is failing.
        """
        lat1 = 61.44
        long1 = 23.8
        loc = str(lat1) + ","+ str(long1)
        self.client.executeRequestWithParams(text="nimika", at=loc)
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertGreater(len(data['search']), 0, "No places found with the given search text")

        #Get the list of location of all the places
        locationList = []
        for p in data['search']:
            locationList.append(p['location'])

        #calculate the arial distance between two points
        distanceList = []
        for i, loc in enumerate(locationList):
            lat2 = float(locationList[i]['lat'])
            long2 = float(locationList[i]['lon'])
            distance = self.client.calcDistanceUsinghaversine(lat1, long1, lat2, long2)
            distanceList.append(distance)
        print("The maximum distance of the locations: %f " %max(distanceList))
        self.assertLessEqual(max(distanceList), 5, "diatance is greater than the radius")

    def test06_searchTextAndEitherLatOrLong(self):
        self.client.executeRequestWithParams(text="nimika", at="23.8")
        status, data = self.client.parseJson()
        self.assertEqual(status, 200, "Request Failed")
        self.assertEqual(len(data['search']), 0, "places found with the given search text")

if __name__ == "__main__":
    unittest.main()

