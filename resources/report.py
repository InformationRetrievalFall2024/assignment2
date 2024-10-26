

def main():
    user_input = input("Did you database parameters for testing and scraping are set to False before. Not doing so will delete all information. Y/n:\t")
    if user_input != "Y":
        return 
    from database import db
    print("\n----------\n")
    print("This is the report below:")
    print("\n----------\n")
    
    print("How many unique pages did you find?")
    number = db.urls.report_unique_pages(db.conn)[0]
    print(number)
    
    print("\n----------\n")
    
    print("What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)")
    url, tokens_count = db.tokens.report_url_with_most_tokens(db.conn)
    print(f"{url:30}: {tokens_count}")
    
    print("\n----------\n")
    
    print("What are the 50 most common words in the entire set of pages crawled under these domains ? (Ignore English stop words, which can be found, for example, here Links to an external site.)")
    for word_info in db.tokens.report_150_most_common_words(db.conn):
        word, freq = word_info
        # need to add a stop word check here (most likely a set that will be loaded to compare string hashes)
        print(f"{word:<50}\t{freq}")
    
    print("\n----------\n")
    
    print("How many subdomains did you find in the uci.edu domain? ")
    for result in db.urls.report_hostname_unique_pages_count(db.conn):
        subdomain, freq = result
        print(f"{subdomain:50}: {freq}")
    
    print("\n----------\n")
    print("Report is completed")
if __name__ == "__main__":
    main()