import sqlite3

class Urls:

    TABLE_CREATION = '''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL UNIQUE,
        subdomain TEXT NOT NULL,
        purned_url TEXT NOT NULL UNIQUE
    ); 
    '''

    TABLE_INSERTION = '''
    INSERT INTO urls (url, subdomain, purned_url) VALUES (?, ?, ?);
    '''

    TABLE_SELECT_SUBDOMAIN_BY_NUMBER_OF_PAGES = '''
    SELECT subdomain, COUNT(*) as url_count
    FROM urls
    GROUP BY subdomain
    ORDER BY (subdomain) ASC;
    '''

    TABLE_SELECT_Unique_Pages = """
    SELECT count(url) FROM urls"""

    def __init__(self):
        pass
    
    def dump(self):
        return self.__dict__
    
    def insert(self, url: str, subdomain: str, pruned_url: str, db: sqlite3.Connection) -> bool:
        cursor = db.cursor()
        try:
            cursor.execute(self.TABLE_INSERTION, (url, subdomain, pruned_url))
            db.commit()
            return True 
        except Exception as e:
            print(f"An error occurred: {e} with url {url}")
            db.rollback()
            return False
    
    def report_hostname_unique_pages_count(self, db: sqlite3.Connection) -> list[tuple]:
        cursor = db.cursor()
        try:
            return cursor.execute(self.TABLE_SELECT_SUBDOMAIN_BY_NUMBER_OF_PAGES).fetchall() # get a generator 
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()
            return []

    def report_unique_pages(self, db: sqlite3.Connection) -> str:
        cursor = db.cursor()
        try:
            return cursor.execute(self.TABLE_SELECT_Unique_Pages).fetchone() # get a generator 
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()
            return ""
class Tokens: 

    TABLE_CREATION = '''
    CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL,
    frequencies INTEGER NOT NULL,
    url TEXT NOT NULL
); 
'''

    TABLE_INSERTION = '''
    INSERT INTO tokens (word, frequencies, url) VALUES (?, ?, ?);
    '''

    TABLE_SELECTION_URL_BY_TOKEN_COUNT = '''
    SELECT url, SUM(frequencies) as total_word_count
    FROM tokens
    GROUP BY url
    ORDER BY url
    LIMIT 1;
    '''

    TABLE_SELECTION_WORD_FREQUENCIES = '''
    SELECT word, SUM(frequencies) as total_frequency
    FROM tokens
    GROUP BY word
    ORDER BY total_frequency DESC
    LIMIT 150;
    '''

    def __init__(self):
        pass

    def dump(self):
        return self.__dict__
    
    def insert(self, values: dict[str: int], ip_address: str, db: sqlite3.Connection):
        cursor = db.cursor()
        try:
            for word, freq in values.items():
                cursor.execute(self.TABLE_INSERTION, ( word, freq, ip_address))
            db.commit()
            return True 
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()
            return False
    
    def report_150_most_common_words(self, db: sqlite3.Connection) -> list[tuple]:
        cursor = db.cursor()
        try:
            
            return cursor.execute(self.TABLE_SELECTION_WORD_FREQUENCIES).fetchall()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()
            return []
    
    def report_url_with_most_tokens(self, db: sqlite3.Connection) -> tuple:
        cursor = db.cursor()
        try:
            
            return cursor.execute(self.TABLE_SELECTION_URL_BY_TOKEN_COUNT).fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            db.rollback()
            return []


class Database:

    DATABASE_URL_PATH = "scraper_data.db"
    Scrapping = True

    def __init__(self):
        self.conn = sqlite3.connect(self.DATABASE_URL_PATH)
        self.urls = Urls()
        self.tokens = Tokens()
        
        self.conn.execute(self.urls.TABLE_CREATION)
        self.conn.execute(self.tokens.TABLE_CREATION)
        self.conn.commit()
        if self.Scrapping:
            user_input = input("You are scrapping data. If you continue, you will delete any data in the database. Do you want to proceed? Y/n\t")
            if user_input != "Y":
                return
            self.conn.execute("""DELETE FROM tokens;""")

            self.conn.execute("""DELETE FROM urls;""")

            self.conn.commit()
        return

db = Database()