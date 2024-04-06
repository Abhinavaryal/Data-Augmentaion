import unittest
from assignment2 import incidentRank
from assignment2 import locationRank


class TestFetchIncidents(unittest.TestCase):
    def test_DowTod(self):
        alldata =[('3/1/2024 23:49', '2024-00015049', '901 N PORTER AVE', 'Suspicious', 'OK0140200'), ('3/1/2024 23:42', '2024-00003367', '529 BUCHANAN AVE', 'Assault EMS Needed', '14005'), ('3/1/2024 23:42', '2024-00004448', '529 BUCHANAN AVE', 'Assault EMS Needed', 'EMSSTAT'),  ('3/1/2024 12:34', '2024-00014922', '1226 CLASSEN BLVD', 'Suspicious', 'OK0140200'), ('3/1/2024 23:59', '2024-00015050', '3450 CHAUTAUQUA AVE', 'Alarm', 'OK0140200')]
        incidentRanks = incidentRank(alldata)
        locationRanks = locationRank(alldata)
        self.assertEqual(locationRanks['529 BUCHANAN AVE'], 1)
        self.assertEqual(incidentRanks['Assault EMS Needed'], 1)
        self.assertEqual(incidentRanks['Suspicious'], 1)
        self.assertEqual(incidentRanks['Alarm'], 3)
        self.assertEqual(locationRanks['901 N PORTER AVE'], 2)
        self.assertEqual(locationRanks['3450 CHAUTAUQUA AVE'], 2)

if __name__ == '__main__':
    unittest.main()