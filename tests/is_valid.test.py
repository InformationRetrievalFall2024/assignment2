import unittest
import csv
from scraper import is_valid


class TestIsValid(unittest.TestCase):

    def setUp(self):
        # Setup code, if needed
        pass

    def tearDown(self):
        # Teardown code, if needed
        pass

    def test_from_csv(self):
        with open('tests/test_cases/dumby_urls.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_string, expected_result = row
                expected_result = expected_result.lower() == 'true'
                with self.subTest(test_string=test_string, expected_result=expected_result):
                    self.assertEqual(is_valid(test_string), expected_result)

if __name__ == '__main__':
    unittest.main()