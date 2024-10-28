import pickle

class PickleManager:

    _RESET = True

    def __init__(self, pickle_file_path, type):
            self._file_path = pickle_file_path
            self.type = type


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
    
    def unpickle_object(self):
        if self._RESET:
            return dict() if self.type == "dict" else set()
        try:
            with open(self._file_path, 'rb') as infile:
                return pickle.load(infile)
        except Exception as e:
            raise RuntimeError(f"Tokens were unable to be loaded from {self._file_path}.") from e


token_manager = PickleManager("scraped/tokens.pickle", "dict")
subdomain_manager = PickleManager("scraped/subdomain.pickle", "dict")
unique_urls_manager = PickleManager("scraped/unique_urls.pickle", "set")