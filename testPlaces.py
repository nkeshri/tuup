import os
import unittest
import sys
from getplacesutility import TuupPlacesApi

host = "devapi.tuup.fi"
apiNearby = "places/v2/nearby"
apiplaceId = "places/v2/nearby/{}"
apisearch = "places/v2/search"
apistops = "places/v2/stops"
apistopId = "places/v2/stops/{}"

class PlacesTest(unittest.TestCase):
    def setUp(self):
        self.client = TuupPlacesApi(host, apiNearby)

    def test01(self):
        self.client.addParams(at="61.4,23.7")
        self.client.generateUrl()

if __name__ == "__main__":
    unittest.main()

