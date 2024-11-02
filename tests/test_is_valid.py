import sys
import os
import unittest
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import is_valid
from resources.helpers import retrieve_obj, store_obj, delete_pickle_files
from resources.Tokenizer import Tokenizer
from StorageManager import StorageManager
class TestIsValid(unittest.TestCase):

    def setUp(self):
        self.db = StorageManager()
        self.db.reset_tables()
        delete_pickle_files()

    def tearDown(self):
        self.db.close_db()

    def test_from_csv(self):
        with open('tests/test_url.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_string, expected_result = row
                expected_result = expected_result.lower() == 'true'
                with self.subTest(test_string=test_string, expected_result=expected_result):
                    self.assertEqual(is_valid(test_string), expected_result)
        
        self.assertEqual(self.db.select_urls_unqiue_count(), 7)

        
if __name__ == '__main__':
    unittest.main()