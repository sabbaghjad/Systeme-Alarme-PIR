import sqlite3
from modele import Evenement

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS evenements (
                id INTEGER PRIMARY KEY,
                type TEXT,
                description TEXT,
                date TEXT
            )
        """)
        
    
    def ajouter_evenement(self, evenement):
        self.cur.execute("INSERT INTO evenements VALUES (NULL, ?, ?, ?)", (evenement.dateHeureEvenement, evenement.typeEvenement, evenement.valeurEvenement))
        self.conn.commit()
        
    
    def close(self):
        self.conn.close()
        
    def recuperer_evenements(self):
        self.cur.execute("SELECT * FROM evenements")
        rows = self.cur.fetchall()
        return [Evenement(*row[1:]) for row in rows] 