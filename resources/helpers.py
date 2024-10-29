import pickle
import os




class PickleStorage:

    _TOKEN_DICT = "storage/td.pickle"
    _SUBDOMAIN_URLS_DICT = "storage/sud.pickle"
    _UNIQUE_URLS_SET = "storage/uus.pickle"
    _MAX_URL = "storage/max.pickle"
    _BAD_URLS = "storage/bad_urls.pickle"
    
def store_obj(obj_to_store: dict[str: int] | set[str], key: int | tuple) -> int | AssertionError:
    """Stores obj depending on name. Options include 0 = unique set, 1 = subdomain, 2 = token, 3 url tokens, 4 bad urls """
    file_path = 0
    if key == 0:
        file_path = PickleStorage._UNIQUE_URLS_SET
    elif key == 1:
        file_path = PickleStorage._SUBDOMAIN_URLS_DICT
    elif key == 2:
        file_path = PickleStorage._TOKEN_DICT
    elif key == 3:
        file_path = PickleStorage._MAX_URL
    elif key == 4:
        file_path = PickleStorage._BAD_URLS
    else:
        assert False
    with open(file_path, "wb") as outfile:
        pickle.dump(obj_to_store, outfile, pickle.HIGHEST_PROTOCOL)
    return 1 

def retrieve_obj(key: int) -> dict[str: int] | set[str]:
    """Retrieves obj depending on name. Options include 0 = unique set, 1 = subdomain, 2 = token, 3 url tokens, 4 bad urls """
    try: 
        file_path = 0
        if key == 0:
            file_path = PickleStorage._UNIQUE_URLS_SET
        elif key == 1:
            file_path = PickleStorage._SUBDOMAIN_URLS_DICT
        elif key == 2:
            file_path = PickleStorage._TOKEN_DICT
        elif key == 3:
            file_path = PickleStorage._MAX_URL
        elif key == 4:
            file_path = PickleStorage._BAD_URLS
        else:
            assert False
        with open(file_path, "rb") as infile:
           return pickle.load(infile)
    except FileNotFoundError:
        if key == 0 or key == 4:
            return set()
        elif key == 3:
            return ("", 0)
        else: 
            return dict()

def delete_pickle_files():
    """Erases pickle files in case of a restart of the crawler"""
    files = [
        PickleStorage._TOKEN_DICT,
        PickleStorage._SUBDOMAIN_URLS_DICT,
        PickleStorage._UNIQUE_URLS_SET,
        PickleStorage._MAX_URL
    ]
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)

class MaxUrlTokens: 

    def __init__(self):
        self.url = ""
        self.token_count = 0
    
    def compare_tokens(self, other_url, other_token_count):
        if self.token_count > other_token_count:
            return 
        store_obj((other_url, other_token_count), 3)
        self.url = other_url
        self.token_count = other_token_count

class BadUrls:

    def __init__(self):
        pass

    def store_bad_urls(self, url: str):
        bad_urls = retrieve_obj(4)
        bad_urls.add(url)
        store_obj(bad_urls, 4)
        del bad_urls
        return 

max_url_tokens = MaxUrlTokens()
bad_urls = BadUrls()