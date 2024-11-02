import re
from sqlite3 import IntegrityError as sqlite3_IntegrityError
from urllib.parse import urlparse, urlunparse, parse_qs
from resources.helpers import retrieve_obj, store_obj, max_url_tokens, delete_pickle_files, bad_urls
from resources.Tokenizer import Tokenizer
from bs4 import BeautifulSoup 
from StorageManager import StorageManager
import lxml 

def reset_storage():
    delete_pickle_files()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    db = StorageManager()
    # return []
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    try: 
    # check if the response status is 200
        if resp.status != 200:
            if resp.status in [600, 608, 607]:
                db.insert_bad_url(url)
            return list()


        # create the soup
        parsed_content = BeautifulSoup(resp.raw_response.content, 'lxml')

        # check to see if there is a meta tag with no index
        meta_tag = parsed_content.find("meta", attrs={'name': 'robots', 'content': 'noindex,nofollow'})
        if meta_tag:
            db.insert_bad_url(url)
            return []

        # check to see if there is a div with error-content class for dead pages hopefully
        error_div = parsed_content.find("div", class_="error-content")
        if error_div:
            db.insert_bad_url(url)
            return []
        
        #check if you have calendar elements (may be overkill)
        calendar = parsed_content.find(class_=re.compile(r'\bcalendar\b', re.IGNORECASE))
        if calendar:
            db.insert_bad_url(url)
            return []

        parsed_content_text = parsed_content.get_text().lower()

        # extract tokens while updating the previous dictionary
        s = Tokenizer()
        
        token_dictionary = dict()
        for token in s.get_token(parsed_content_text):
            try:
                token_dictionary[token] = token_dictionary[token] + 1 
            except KeyError:
                token_dictionary[token] = 1

        db.insert_token(token_dictionary, url)
        
        del parsed_content_text
        del token_dictionary
        # extract all links on the page
        return [x["href"] for x in parsed_content.find_all("a", href=True)]

    except Exception as e:
        print(f"Error occured when extracting links. {e}")
        return list()

    finally:
        db.close_db()

def is_valid(url):
    # return True
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    db = StorageManager()
    try:
        result = db.check_if_bad_url(url)
        if result:
            return False 
        hostname_matched = False 
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if parsed.query: # stops from clicking log in button
            if parse_qs(parsed.query).get("action"):
                return False 
            
        login_redirect_pattern = r"(login|redirect_to|auth|signin|signup|logout|filter|calendar)"
        if re.search(login_redirect_pattern, parsed.path, re.IGNORECASE) or re.search(login_redirect_pattern, parsed.query, re.IGNORECASE):
            return False
        
        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False
        
        hostname_split = parsed.hostname.split(".")[-3:]
        if not hostname_split: # something went wrong once but don't have time to fix it in time
            return False 
        if ".".join(hostname_split) in ["stat.uci.edu", "ics.uci.edu", "cs.uci.edu", "informatics.uci.edu"]:
            hostname_matched = True

        niche_path_pattern = r"^/department/information_computer_sciences/.*$"
        
        if parsed.hostname == "today.uci.edu" and re.match(niche_path_pattern, parsed.path): # doesn't work if www. is in front 
            hostname_matched = True

        if not hostname_matched:
            return False 
        
        # store url with fragment in unique set if not in there else return
        defragged_url = urlunparse(parsed._replace(fragment=''))
        db.insert_url(parsed.hostname, defragged_url, url)
        return True

    except sqlite3_IntegrityError:
        # inserting into the database didn't work as url or subdomain is not unique
        return False
    except TypeError:
        print ("TypeError for ", parsed)
        return False 
    
    finally:
        db.close_db()