import sqlite3

conn = sqlite3.connect("scraper_data.db")


# need to implement a system that will delete the database upon shutting down the program 

url_table_creation = '''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    hostname TEXT NOT NULL,
    ip_address TEXT NOT NULL
); 
'''

url_insert_table = '''
INSERT INTO urls (url, hostname, ip_address) VALUES (?, ?, ?);
'''

url_select_subdomains_by_number_of_pages = '''
SELECT hostname, COUNT(*) as url_count
FROM urls
GROUP BY hostname
ORDER BY hostname DESC;
'''

class Urls:

    def __init__(self, hostname: str, url: str, ip_address: str):
        self.hostname = hostname
        self.url = url 
        self.ip_address = ip_address
    
    def dump(self):
        return self.__dict__
    

class Tokens: 

    def __init__(self, connection: sqlite3.Connection, insertStatement: str, selectStatements: list[str]):
        self.connection = connection
        self.insertStatement = insertStatement
        self.selectStatements = selectStatements

    def dump(self):
        return self.__dict__
    
    def insert(self, values: dict[str: int], ip_address: str):
        cursor = self.connection.cursor()
        try:
            for word, freq in values.items():
                print(f"Inserting {word}: {freq} for URL: {ip_address}")  # Debug print
                cursor.execute(self.insertStatement, ( word, freq, ip_address))
            self.connection.commit()
            return True 
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return False
    
    def report_150_most_common_words(self) -> list[tuple]:
        cursor = self.connection.cursor()
        try:
            
            return cursor.execute(self.selectStatements[0]).fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return []
    
    def report_url_with_most_tokens(self) -> tuple:
        cursor = self.connection.cursor()
        try:
            
            return cursor.execute(self.selectStatements[1]).fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return []


token_table_creation = '''
CREATE TABLE IF NOT EXISTS token (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    frequencies INTEGER NOT NULL,
    url TEXT NOT NULL
); 
'''

token_insert_table = '''
INSERT INTO token (word, frequencies, url) VALUES (?, ?, ?);
'''

token_select_table_url_by_total_token_counts = '''
SELECT url, SUM(frequencies) as total_word_count
FROM token
GROUP BY url
ORDER BY url
LIMIT 1;
'''

token_select_table_word_total_count = '''
SELECT word, SUM(frequencies) as total_frequency
FROM token
GROUP BY word
ORDER BY total_frequency DESC
LIMIT 150;
'''

conn.execute(url_table_creation)

conn.execute(token_table_creation)

conn.execute("""DELETE FROM token;""")

conn.execute("""DELETE FROM urls;""")

conn.commit()

token_table =  Tokens(conn, token_insert_table, [token_select_table_word_total_count, token_select_table_url_by_total_token_counts])