import sqlite3
import os
import sys

# Add parent directory to path to import Config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def init_db():
    db_dir = os.path.join(Config.BASE_DIR, 'database')
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Datasets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        original_name TEXT NOT NULL,
        row_count INTEGER,
        file_size INTEGER,
        status TEXT DEFAULT 'uploaded',
        quality_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Cleaning Logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cleaning_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id INTEGER,
        action TEXT NOT NULL,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(dataset_id) REFERENCES datasets(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
