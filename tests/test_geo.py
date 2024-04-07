import unittest
from assignment2 import getSoT


class TestFetchIncidents(unittest.TestCase):
    def test_DowTod(self):
        latlong = {}
        alldata = [('3/1/2024 23:49', '2024-00015049', '901 N PORTER AVE', 'Suspicious', 'OK0140200')]
        latlong['901 N PORTER AVE'] = [35.23015,-97.43915]
        latlong, SoT = getSoT(alldata)
        self.assertEqual(SoT['901 N PORTER AVE'], 'N')
        self.assertEqual(latlong['901 N PORTER AVE'],[35.2301496, -97.43914960000001])

if __name__ == '__main__':
    unittest.main()