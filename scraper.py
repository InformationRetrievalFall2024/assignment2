import re
import tempfile
from tokenizer import Tokenizer
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from database import token_table

scanner = Tokenizer()

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url: str, resp):
    
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    
    # Check if response status is 200 
    if resp.status != 200:
        print("Response status code is not equivalent to 200!")
        return []# may want to do something else to handle errors 
    
    # Parse while nt having an error 
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'lxml')

        # get the links 
        links = [x["href"] for x in soup.find_all("a", href=True)]


        # create a temporary file to write the text into so that I can slowly load the file back into memory
        with tempfile.NamedTemporaryFile(delete_on_close=False, mode="w+", encoding="utf-8") as temp_file:
            
            # parse the text with a Tokenizer 
            text = soup.get_text()

            temp_file.write(text)

            temp_file.flush()

            del text 

            tokenFrequenciesDict = scanner.compute_word_frequencies([x for x in scanner.tokenize(temp_file.name)])

            storedTokens = token_table.insert(tokenFrequenciesDict, url)
            if not storedTokens:
                print(f"Failed to store tokens for url: {url}")
            del tokenFrequenciesDict

        return links 
    except Exception as e:
        print(f"\n Something went wrong with the extracting links should as {e} \n")
        return [] # may want to do something else to handle the errors 

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        urlFlag = False
        extensionFlag = False
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        niche_domain_pattern = r"^.*(stat|ics|informatics|cs)\.uci\.edu$"  # any character or zero characters before it (.*), first capture group of ors (|), and must end in uci.edu ($)

        niche_path_pattern = r"^/department/information_computer_sciences/.*$"
        
        
        if re.match(niche_domain_pattern, parsed.hostname):  
            urlFlag = True 
        
        if parsed.hostname == "today.uci.edu" and re.match(niche_path_pattern, parsed.path): # doesn't work if www. is in front 
            urlFlag = True

        if not re.match(
        r".*\.(css|js|bmp|gif|jpe?g|ico"
        + r"|png|tiff?|mid|mp2|mp3|mp4"
        + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
        + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
        + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
        + r"|epub|dll|cnf|tgz|sha1"
        + r"|thmx|mso|arff|rtf|jar|csv"
        + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            extensionFlag = True
        return urlFlag and extensionFlag

    except TypeError:
        print ("TypeError for ", parsed)
        raise

