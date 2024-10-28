import re
from urllib.parse import urlparse, urlunparse
from resources.PickleManager import PickleManager
from resources.Tokenizer import Tokenizer
from bs4 import BeautifulSoup 
import lxml 

token_manager = PickleManager("scraped/tokens.pickle", "dict")
subdomain_manager = PickleManager("scraped/subdomain.pickle", "dict")
unique_urls_manager = PickleManager("scraped/unique_urls.pickle", "set")

def scraper(url, resp):
    links = extract_next_links(url, resp, token_manager)
    return [link for link in links if is_valid(link, subdomain_manager, unique_urls_manager)]

def extract_next_links(url, resp, token_manager: PickleManager):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # check if the response status is 200
    if resp.status != 200:
        return list()
    
    try: 
        # create the soup
        parsed_content = BeautifulSoup(resp.raw_response.content, 'lxml')

        # check to see if there is a meta tag with no index
        meta_tag = parsed_content.find("meta", attrs={'name': 'robots', 'content': 'noindex,nofollow'})
        if meta_tag:
            return []
        
        #check if you have calendar elements (may be overkill)
        calendar = parsed_content.find(class_=re.compile(r'\bcalendar\b', re.IGNORECASE))
        if calendar:
            return []

        parsed_content_text = parsed_content.get_text()

        # extract tokens while updating the previous dictionary
        s = Tokenizer()
        
        
        token_dictionary = token_manager.unpickle_tokens()
        for token in s.get_token(parsed_content_text):
            try:
                token_dictionary[token] = token_dictionary[token] + 1 
            except KeyError:
                token_dictionary[token] = 1
 
        del parsed_content_text

        # unpickle the previous token dictionary and update it using the new dictionary
        token_manager.pickle_tokens(token_dictionary)

        del token_dictionary
        # extract all links on the page
        return [x["href"] for x in parsed_content.find_all("a", href=True)]

        


    except Exception as e:
        print(f"An error has occured here. {e}")
        pass 
    
    return list()

def is_valid(url, subdomain_manager: PickleManager, unique_urls_manager: PickleManager):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        url_matched = False 
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
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
        
        niche_domain_pattern = r"^.*(stat|ics|informatics|cs)\.uci\.edu$"  # any character or zero characters before it (.*), first capture group of ors (|), and must end in uci.edu ($)

        niche_path_pattern = r"^/department/information_computer_sciences/.*$"
        
        
        if re.match(niche_domain_pattern, parsed.hostname):  
            url_matched = True 
        
        if parsed.hostname == "today.uci.edu" and re.match(niche_path_pattern, parsed.path): # doesn't work if www. is in front 
            url_matched = True

        if not url_matched:
            return False 
        
        # store url with fragment in unique set if not in there else return
        unique_urls_set = unique_urls_manager.unpickle_tokens()
        defragged_url = urlunparse(parsed._replace(fragment=''))
        if defragged_url in unique_urls_set:
            return False 
        
        unique_urls_set.add(defragged_url)
        print(unique_urls_set)
        unique_urls_manager.pickle_tokens(unique_urls_set)
        del unique_urls_set

        # store a count with subdomains being the key and count being the value

        mapped_subdomains: dict[str: int] = subdomain_manager.unpickle_tokens()
        previous_value = 0

        try:
            previous_value = mapped_subdomains[parsed.hostname]
        except KeyError:
            pass 

        mapped_subdomains[parsed.hostname] = previous_value + 1
        subdomain_manager.pickle_tokens(mapped_subdomains)
        del mapped_subdomains

        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise
