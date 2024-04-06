import unittest
from assignment2 import checkWeather


class TestFetchIncidents(unittest.TestCase):
    def test_DowTod(self):
        latlong = {}
        alldata = [('3/1/2024 23:49', '2024-00015049', '901 N PORTER AVE', 'Suspicious', 'OK0140200')]
        latlong['901 N PORTER AVE'] = [35.23015,-97.43915]
        checkWeatherCode = checkWeather(latlong, alldata, [23])
        self.assertEqual(checkWeatherCode['3/1/2024 23:49','901 N PORTER AVE' ], 0.0)

if __name__ == '__main__':
    unittest.main()