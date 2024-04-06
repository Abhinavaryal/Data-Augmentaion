import unittest
from assignment2 import fetchincidents
from assignment2 import extractincidents

class TestFetchIncidents(unittest.TestCase):
    def test_dowloded_data(self):
        url="https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf"
        
        incidents_data = fetchincidents(url)
        # test 1 to check it the data is being fetched
        self.assertEqual(len(incidents_data), 188256)

        incidents= extractincidents(incidents_data)
        # test 2 to check if the data is being extracted properly
        self.assertEqual(len(incidents),328)

if __name__ == '__main__':
    unittest.main()