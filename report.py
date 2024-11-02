from StorageManager import StorageManager
# import tests.populate_pickle_files # only uncomment for testing purposes
"""
As a concrete deliverable of this project, besides the code itself, you must submit a report containing answers to the following questions:

How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL, but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL. Even if you implement additional methods for textual similarity detection, please keep considering the above definition of unique pages for the purposes of counting the unique pages in this assignment.
What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)
What are the 50 most common words in the entire set of pages crawled under these domains ? (Ignore English stop words, which can be found, for example, here Links to an external site.) Submit the list of common words ordered by frequency.
How many subdomains did you find in the uci.edu domain? Submit the list of subdomains ordered alphabetically and the number of unique pages detected in each subdomain. The content of this list should be lines containing subdomain, number, for example:
vision.ics.uci.edu, 10 (not the actual number here)

"""

def print_frequencies(dictionary: dict[str, int]):
    for k,v in dictionary:
        print(f"{k:30}:{v}")

sm = StorageManager()
# Get length of unique pages by taking the length of unique urls 
print("\n-----------------------------\n")
print("Report")
print("\n-----------------------------\n")
print(f"Found {sm.select_urls_unqiue_count()} unique pages")
print("\n-----------------------------\n")
url, count = sm.select_tokens_by_url_with_most_frequencies()
print(f"The page with the most tokens is {url} with a token count of {count}")
print("\n-----------------------------\n")
print("Found these subdomains:\t")
token_dictionary = sm.select_tokens_by_frequencies()
print("\n-----------------------------\n")
print("Most common tokens here: ")
print_frequencies(token_dictionary)
print("\n-----------------------------\n")
subdomain_dict = sm.select_urls_by_subdomain()
print_frequencies(subdomain_dict)