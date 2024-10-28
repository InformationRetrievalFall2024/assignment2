import pickle

# class PickleManager:

#     def __init__(self, pickle_file_path, pickle_file_path_2, type):
#             self._class_File_Path = pickle_file_path # "scraped/tokens_data.pickle"
#             self._class_File_Path2 = pickle_file_path_2 # "scraped/tokens_data_pickle_redundancy.pickle"
#             self._class_Last_Saved = ""
#             self.type = type 

#     def pickle_tokens(self, mapped_or_hashed_values: dict[str, int] | set[str]) -> None:
        
#         try: 
#             if not mapped_or_hashed_values:
#                 assert False
#             file_path = self._class_File_Path if self._class_File_Path != self._class_Last_Saved else self._class_File_Path2
#             with open(file_path, 'wb') as infile:
#                 pickle.dump(mapped_or_hashed_values, infile, pickle.HIGHEST_PROTOCOL) 
#             self._class_Last_Saved = file_path
#         except AssertionError:
#             error_message = "Last saved in {self._class_Last_Saved}" if self._class_Last_Saved else "There is no previous pickle file with tokens."
#             raise RuntimeError(f"Token Manager pickle tokens function was passed an empty dictionary. {error_message}")
#         except Exception as e:
#             raise RuntimeError(f"Tokens was unable to be pickled. Last saved data in {self._class_Last_Saved}.") from e
    
#     def unpickle_tokens(self):
#         try:
#             if not self._class_Last_Saved:
#                return set() if self.type == "set" else dict()
#             with open(self._class_Last_Saved, 'rb') as infile:
#                 return pickle.load(infile)
#         except AssertionError as e:
#             raise RuntimeError(f"Tokens were never pickled. May have been called before pickling tokens.")
#         except Exception as e:
#             raise RuntimeError(f"Tokens were unable to be loaded from {self._class_Last_Saved}")
    
#     def find_last_saved_values(self) -> set[str] | dict[str, int]:
#         self._class_Last_Saved = self._class_File_Path
#         mapped_or_hashed_file_1 = self.unpickle_tokens()
#         self._class_Last_Saved = self._class_File_Path2
#         mapped_or_hashed_file_2 = self.unpickle_tokens()
#         if self.type == "set":
#             return mapped_or_hashed_file_1 if len(mapped_or_hashed_file_1) > len(mapped_or_hashed_file_2) else mapped_or_hashed_file_2
#         else:
#             return mapped_or_hashed_file_1 if len(mapped_or_hashed_file_1.keys()) > len(mapped_or_hashed_file_2.keys()) else mapped_or_hashed_file_2

# token_manager = PickleManager("scraped/tokens.pickle", "scraped/tokens_redundant.pickle", "dict")
# subdomain_manager = PickleManager("scraped/subdomain.pickle", "scraped/subdomain_redundant.pickle", "dict")
# unique_urls_manager = PickleManager("scraped/unique_urls.pickle", "scraped/unique_urls_redundant.pickle", "set")

class PickleManager:

    def __init__(self, pickle_file_path, type, reporting):
            self._file_path = pickle_file_path # "scraped/tokens_data.pickle"
            # self._class_File_Path2 = pickle_file_path_2 # "scraped/tokens_data_pickle_redundancy.pickle"
            self.type = type 
            self._packed_before = True if reporting else False
            self._starting_value = dict()
            if type == "set":
                self._starting_value = set()


    def pickle_tokens(self, mapped_or_hashed_values: dict[str, int] | set[str]) -> None:
        try: 
            if not mapped_or_hashed_values:
                assert False
            with open(self._file_path, 'wb') as infile:
                pickle.dump(mapped_or_hashed_values, infile, pickle.HIGHEST_PROTOCOL) 
            self._packed_before = True
        except AssertionError:
            raise RuntimeError(f"Token Manager pickle tokens function was passed an empty dictionary.")
        except Exception as e:
            raise RuntimeError(f"Tokens were unable to be pickled to {self._file_path}.") from e
    
    def unpickle_tokens(self):
        if not self._packed_before:
            return self._starting_value
        try:
            with open(self._file_path, 'rb') as infile:
                return pickle.load(infile)
        except Exception as e:
            raise RuntimeError(f"Tokens were unable to be loaded from {self._file_path}.") from e


token_manager = PickleManager("scraped/tokens.pickle", "dict", False)
subdomain_manager = PickleManager("scraped/subdomain.pickle", "dict", False)
unique_urls_manager = PickleManager("scraped/unique_urls.pickle", "set", False)