import re
from urllib.parse import urlparse, urlunparse, parse_qs
from resources.helpers import retrieve_obj, store_obj, max_url_tokens, delete_pickle_files, bad_urls
from resources.tokenizer import Tokenizer
from bs4 import BeautifulSoup 
import lxml 

def reset_storage():
    delete_pickle_files()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
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

    # check if the response status is 200
    if resp.status != 200:
        if resp.status in [600, 608, 607]:
            bad_urls.store_bad_urls(url)
        return list()

    # check for "?filter%" in the url to prevent infinite loops with filters
    if '?filter%' in resp.url:
        bad_urls.store_bad_urls(url)
        return []
        
    # check for "#comment-" in the url to prevent comment section loops
    if '#comment-' in resp.url:
        bad_urls.store_bad_urls(url)
        return []

    # check for "#respond" in the url to prevent respond section loops
    if '#respond' in resp.url:
        bad_urls.store_bad_urls(url)
        return []
    
    # check for these in the url; they break the crawl
    if '~aalshayb' in resp.url:
        bad_urls.store_bad_urls(url)
        return []
    
    if "20-icde-crypto_encryption_secret-sharing_sgx_tutorial.ppsx" in resp.url:
        bad_urls.store_bad_urls(url)
        return []

    if 'https://grape.ics.uci.edu/wiki/public/wiki/cs122b' in resp.url:
        bad_urls.store_bad_urls(url)
        return []

    try: 
        # create the soup
        parsed_content = BeautifulSoup(resp.raw_response.content, 'lxml')

        # check to see if there is a meta tag with no index
        meta_tag = parsed_content.find("meta", attrs={'name': 'robots', 'content': 'noindex,nofollow'})
        if meta_tag:
            bad_urls.store_bad_urls(url)
            return []

        # check to see if there is a div with error-content class for dead pages hopefully
        error_div = parsed_content.find("div", class_="error-content")
        if error_div:
            bad_urls.store_bad_urls(url)
            return []
        
        #check if you have calendar elements (may be overkill)
        calendar = parsed_content.find(class_=re.compile(r'\bcalendar\b', re.IGNORECASE))
        if calendar:
            bad_urls.store_bad_urls(url)
            return []

        parsed_content_text = parsed_content.get_text().lower()

        # extract tokens while updating the previous dictionary
        s = Tokenizer()
        token_count = 0
        
        token_dictionary = retrieve_obj(2)
        for token in s.get_token(parsed_content_text):
            token_count += 1
            try:
                token_dictionary[token] = token_dictionary[token] + 1 
            except KeyError:
                token_dictionary[token] = 1

        assert token_count # make sure the we are getting tokens

        del parsed_content_text
        max_url_tokens.compare_tokens(url, token_count)
        # unpickle the previous token dictionary and update it using the new dictionary
        store_obj(token_dictionary, 2)

        del token_dictionary
        # extract all links on the page
        return [x["href"] for x in parsed_content.find_all("a", href=True)]

    except Exception as e:
        print(f"Error occured when extracting links. {e}")
        return list()

def is_valid(url):
    # return True
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        bad_urls = retrieve_obj(4)
        if url in bad_urls:
            return False 
        hostname_matched = False 
        parsed = urlparse(url)

        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if parsed.query: # stops from clicking log in button
            if parse_qs(parsed.query).get("action"):
                return False 
            
        login_redirect_pattern = r"(login|redirect_to|auth|signin|signup|logout)"
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
        unique_urls_set = retrieve_obj(0)
        defragged_url = urlunparse(parsed._replace(fragment=''))
        if defragged_url in unique_urls_set:
            return False 
        
        unique_urls_set.add(defragged_url)

        store_obj(unique_urls_set, 0)
        del unique_urls_set

        # store a count with subdomains being the key and count being the value

        mapped_subdomains: dict[str: int] = retrieve_obj(1)
        previous_value = 0

        try:
            previous_value = mapped_subdomains[parsed.hostname]
        except KeyError:
            pass 

        mapped_subdomains[parsed.hostname] = previous_value + 1
        store_obj(mapped_subdomains, 1)
        del mapped_subdomains

        return True

    except TypeError:
        print ("TypeError for ", parsed)
        raise