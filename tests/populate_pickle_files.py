import sys
import os
import unittest
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper import extract_next_links, is_valid, reset_storage

class Raw: 

    def __init__(self, content: str, url: str):
        self.content = content
        self.url = url 

class Response:
    
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    def __init__(self, url: str, status: int, error: str, content: str):
        self.url = url
        self.status = status
        self.error = error
        self.raw_response =  Raw(content, url)

reset_storage()

html_files_content = [
"""
<html>
    <head><title>Test Page 1</title></head>
    <body>
        <p>This is a test page with some links.</p>
        <a href="http://example.com/page1">Link 1</a>
        <a href="http://example.com/page2">Link 2</a>
    </body>
</html>
""",
"""
<html>
    <head><title>Test Page 2</title></head>
    <body>
        <p>Another test page with different links. 14</p>
        <a href="http://example.com/page3">Link 3</a>
        <a href="http://example.com/page4">Link 4</a>
    </body>
</html>
""",
"""
<html>
    <head><title>Test Page 3</title></head>
    <body>
        <p>Yet another test page.</p>
        <a href="http://example.com/page5">Link 5</a>
        <a href="http://example.com/page6">Link 6</a>
    </body>
</html>
"""
]

response_success_1 = Response("http://home.example.com/about", 200, "", html_files_content[0])

response_success_2 = Response("http://explore.example.com/about", 200, "", html_files_content[1])

response_success_3 = Response("http://shop.example.com/listings", 200, "", html_files_content[2])

response_fail = Response("http://home.example.com/about", 204, "", html_files_content[1])

# Test case 1 for some_function
test_number = 0
expected_links = [["http://example.com/page1", "http://example.com/page2"], ["http://example.com/page3", "http://example.com/page4"], ["http://example.com/page5", "http://example.com/page6"], []]
responses = [response_success_1, response_success_2, response_success_3, response_fail]
while (0 <= test_number <= 3):
    actual_links = extract_next_links(responses[test_number].url, responses[test_number])
    test_number += 1 


with open('tests/test_url.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                test_string, expected_result = row
                is_valid(test_string)
# testing report 

