import sys
import os
import unittest
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import is_valid
from resources.PickleManager import unique_urls_manager, subdomain_manager
from resources.Tokenizer import Tokenizer

class TestIsValid(unittest.TestCase):

    def test_from_csv(self):
        with open('tests/cases/urls.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_string, expected_result = row
                expected_result = expected_result.lower() == 'true'
                with self.subTest(test_string=test_string, expected_result=expected_result):
                    self.assertEqual(is_valid(test_string, subdomain_manager, unique_urls_manager), expected_result)
        t = Tokenizer()
        unique_urls = unique_urls_manager.unpickle_tokens()
        print(len(unique_urls))
        for url in unique_urls:
            print(url)
        print()
        t.print_frequencies(subdomain_manager.unpickle_tokens()) 
        
if __name__ == '__main__':
    unittest.main()