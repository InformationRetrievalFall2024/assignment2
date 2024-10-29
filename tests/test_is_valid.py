import sys
import os
import unittest
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import is_valid
from resources.helpers import retrieve_obj, store_obj, delete_pickle_files
from resources.Tokenizer import Tokenizer

class TestIsValid(unittest.TestCase):

    def setUp(self):
        delete_pickle_files()

    def test_from_csv(self):
        with open('tests/test_url.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_string, expected_result = row
                expected_result = expected_result.lower() == 'true'
                with self.subTest(test_string=test_string, expected_result=expected_result):
                    self.assertEqual(is_valid(test_string), expected_result)
        t = Tokenizer()
        unique_urls = retrieve_obj(0)
        self.assertEqual(len(unique_urls), 7)

        
if __name__ == '__main__':
    unittest.main()