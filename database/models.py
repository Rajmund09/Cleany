import sqlite3
import os
import sys

# Add parent directory to path to import Config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def get_db_connection():
    db_path = os.path.join(Config.BASE_DIR, 'database', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class DatasetModel:
    @staticmethod
    def create(filename, original_name, row_count=0, file_size=0):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO datasets (filename, original_name, row_count, file_size, status)
            VALUES (?, ?, ?, ?, 'uploaded')
        ''', (filename, original_name, row_count, file_size))
        conn.commit()
        dataset_id = cursor.lastrowid
        conn.close()
        return dataset_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        datasets = conn.execute('SELECT * FROM datasets ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(ix) for ix in datasets]

    @staticmethod
    def get_by_id(dataset_id):
        conn = get_db_connection()
        dataset = conn.execute('SELECT * FROM datasets WHERE id = ?', (dataset_id,)).fetchone()
        conn.close()
        return dict(dataset) if dataset else None
        
    @staticmethod
    def update_status(dataset_id, status, quality_score=None):
        conn = get_db_connection()
        if quality_score is not None:
            conn.execute('UPDATE datasets SET status = ?, quality_score = ? WHERE id = ?', 
                         (status, quality_score, dataset_id))
        else:
            conn.execute('UPDATE datasets SET status = ? WHERE id = ?', 
                         (status, dataset_id))
        conn.commit()
        conn.close()
        
    @staticmethod
    def log_cleaning_action(dataset_id, action, details=""):
        conn = get_db_connection()
        conn.execute('INSERT INTO cleaning_logs (dataset_id, action, details) VALUES (?, ?, ?)',
                     (dataset_id, action, details))
        conn.commit()
        conn.close()

    @staticmethod
    def get_logs(dataset_id):
        conn = get_db_connection()
        logs = conn.execute('SELECT * FROM cleaning_logs WHERE dataset_id = ? ORDER BY created_at ASC', (dataset_id,)).fetchall()
        conn.close()
        return [dict(l) for l in logs]
