# import sys
# import os
# import unittest
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from resources.PickleManager import PickleManager

# class TestPickleManager(unittest.TestCase):

#     def setUp(self):
#         self.token_manager = PickleManager("scraped/tokens.pickle", "scraped/tokens_redundant.pickle", "dict")
#         self.set_manager = PickleManager("scraped/pop.pickle", "scraped/pop2.pickle", "set")
#     def test_validate_token(self):
#         data = {"1": 1, "2": 2, "3": 3}
#         self.token_manager.pickle_tokens(data)
#         data_stored = self.token_manager.unpickle_tokens()
#         self.assertDictEqual(data, data_stored)

#         data = {"1": 1, "2": 2, "3": 3, "4": 4}
#         self.token_manager.pickle_tokens(data)
#         data_stored = self.token_manager.unpickle_tokens()
#         self.assertDictEqual(data, data_stored)
#         self.assertEqual(self.token_manager._class_Last_Saved, self.token_manager._class_File_Path2)

#         data = {"1": 1, "2": 2, "3": 3, "4": 4, "5" : 5}
#         self.token_manager.pickle_tokens(data)
#         data_stored = self.token_manager.unpickle_tokens()
#         self.assertDictEqual(data, data_stored)
#         self.assertEqual(self.token_manager._class_Last_Saved, self.token_manager._class_File_Path)
    
#     def test_failure_passing_empty_dictionary(self):
#         self.assertRaises(RuntimeError, self.token_manager.pickle_tokens, {})
    
#     def test_reading_from_empty(self):
#         self.assertDictEqual(dict(), self.token_manager.unpickle_tokens())
#         self.assertSetEqual(set(), self.set_manager.unpickle_tokens())
        
# if __name__ == '__main__':
#     unittest.main()

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from resources.PickleManager import PickleManager

class TestPickleManager(unittest.TestCase):

    def setUp(self):
        self.token_manager = PickleManager("scraped/tokens.pickle", "dict")
        self.set_manager = PickleManager("scraped/pop.pickle", "set")

    def test_validate_token(self):
        data = {"1": 1, "2": 2, "3": 3}
        self.token_manager.pickle_tokens(data)
        data_stored = self.token_manager.unpickle_tokens()
        self.assertDictEqual(data, data_stored)

        data = {"1": 1, "2": 2, "3": 3, "4": 4}
        self.token_manager.pickle_tokens(data)
        data_stored = self.token_manager.unpickle_tokens()
        self.assertDictEqual(data, data_stored)
    
    def test_failure_passing_empty_dictionary(self):
        self.assertRaises(RuntimeError, self.token_manager.pickle_tokens, {})
    
    def test_reading_from_empty(self):
        self.assertDictEqual(dict(), self.token_manager.unpickle_tokens())
        self.assertSetEqual(set(), self.set_manager.unpickle_tokens())
        
if __name__ == '__main__':
    unittest.main()