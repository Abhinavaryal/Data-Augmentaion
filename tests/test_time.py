import unittest
from assignment2 import DowTod


class TestFetchIncidents(unittest.TestCase):
    def test_DowTod(self):

        alldata = [('3/1/2024 23:49', '2024-00015049', '901 N PORTER AVE', 'Suspicious', 'OK0140200')]
        DoW, ToD = DowTod(alldata)
        self.assertEqual(DoW[0], 6)
        self.assertEqual(ToD[0], 23)

if __name__ == '__main__':
    unittest.main()