import unittest
from assignment2 import emssat


class TestFetchIncidents(unittest.TestCase):
    def test_DowTod(self):

        alldata =[('3/1/2024 23:42', '2024-00003367', '529 BUCHANAN AVE', 'Assault EMS Needed', '14005'), ('3/1/2024 23:42', '2024-00004448', '529 BUCHANAN AVE', 'Assault EMS Needed', 'EMSSTAT')]
        emssatVal = emssat(alldata)
        self.assertEqual(emssatVal[0], 'True')
        self.assertEqual(emssatVal[1], 'True')

if __name__ == '__main__':
    unittest.main()