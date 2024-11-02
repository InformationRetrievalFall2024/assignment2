import sqlite3
from typing import Optional

class StorageManager:
    def __init__(self, db_name='storage_manager.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subdomain TEXT,
                    defragged_url TEXT UNIQUE,
                    url TEXT UNIQUE
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT,
                    freq INTEGER,
                    url TEXT
                )
            ''')
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS BadUrl (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNQIUE);""")

    def insert_url(self, subdomain: str, defragged_url: str, url: str) -> Optional[sqlite3.IntegrityError]:
        """Insert into table url. Throws sqlite3.IntegrityError"""
        with self.conn:
            self.conn.execute('''
                INSERT INTO urls (subdomain, defragged_url, url)
                VALUES (?, ?, ?)
            ''', (subdomain, defragged_url, url))

    def insert_token(self, token_dictionary: dict[str, int], url: str) -> Optional[sqlite3.IntegrityError]:
        """Insert into table tokens. Throws sqlite3.IntegrityError"""
        with self.conn as conn:
            for word, freq in token_dictionary.items():
                conn.execute("""INSERT INTO tokens (word, freq, url) VALUES (?, ?, ?)""", (word, freq, url))
    
    def insert_bad_url(self, bad_url: str) -> None:
        try: 
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO BadUrl (url) VALUES (?)""", (bad_url,))
            cursor.close()
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
    
    def select_tokens_by_frequencies(self):
        with self.conn:
            tokens = self.conn.execute("""
                SELECT word, SUM(freq) as total FROM tokens GROUP BY word ORDER BY total DESC, word ASC""")
            for token in tokens:
                yield token
    
    def select_urls_unqiue_count(self) -> int:
        with self.conn:
            return self.conn.execute("""
                SELECT COUNT(*) FROM urls""").fetchone()[0]
    
    def select_tokens_by_url_with_most_frequencies(self) -> tuple: 
        with self.conn:
            return self.conn.execute("""
                                     SELECT url, SUM(freq) FROM tokens GROUP BY url ORDER BY SUM(freq) DESC""").fetchone()
        
    def select_urls_by_subdomain(self):
        with self.conn:
            return self.conn.execute("""
                SELECT subdomain, COUNT(url) FROM urls GROUP BY subdomain ORDER BY subdomain ASC
            """).fetchall()

    def check_if_bad_url(self, bad_url: str) -> Optional[tuple]:
        with self.conn:
            return self.conn.execute("""SELECT count(*) FROM BadUrl WHERE url = ?""", (bad_url,)).fetchone()[0]

    def reset_tables(self):
        with self.conn as conn: 
            conn.execute("""DROP TABLE IF EXISTS tokens;""")
            conn.execute("""DROP TABLE IF EXISTS urls""")
            self.create_tables()
    
    def close_db(self):
        self.conn.close()




# Example usage:
# try:

#     storage_manager = StorageManager()
#     storage_manager.reset_tables()
#     storage_manager.insert_bad_url("http://example.com/Not_Found")
#     storage_manager.insert_token('example', 5, 'http://example.com/page')
#     storage_manager.insert_token('example', 5, 'http://example.com/page2')
#     for token in storage_manager.select_tokens_by_frequencies():
#         print(token)
#     storage_manager.insert_url('example.com', 'http://example.com/page', 'http://example.com/page')
#     storage_manager.insert_url('example.com', 'http://example.com/page#home', 'http://example.com/page')
# except sqlite3.IntegrityError:
#     print(storage_manager.select_urls_unqiue_count())
# except Exception as e:
#     print("Error occured with bad url insert")
#     print(e)
