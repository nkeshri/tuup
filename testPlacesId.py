import os
import unittest
import sys
from tuupapiutil import TuupPlacesApi

host = "devapi.tuup.fi"
apiplaceId = "places/v2/nearby/{}"

class ApiPlaceIdTest(unittest.TestCase):
    def setUp(self):
        self.client = TuupPlacesApi(host, apiNearby)

    def test01(self):
        self.client.addParams(at="61.44,23.8")
        self.client.generateUrl()
        self.client.getRequest()
        status, data = self.client.parseJson()
        print("The status is %s and the content is %s" %(status,data))

if __name__ == "__main__":
    unittest.main()

