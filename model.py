import mysql.connector
from mysql.connector import pooling
from config import Config
import time
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _pool = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._pool is None:
            required = ['host', 'user', 'password', 'database']
            missing = [key for key in required if not Config.MYSQL_CONFIG.get(key)]
            if missing:
                raise RuntimeError(
                    "Konfigurasi database belum lengkap. Isi DB_HOST, DB_USER, "
                    "DB_PASSWORD, dan DB_NAME pada file .env."
                )
            self._pool = pooling.MySQLConnectionPool(
                pool_name="portfolio_pool",
                pool_size=5,
                pool_reset_session=True,
                **Config.MYSQL_CONFIG
            )
    
    def get_connection(self):
        """Mengambil koneksi dari pool"""
        return self._pool.get_connection()
    
    def execute_query(self, query, params=None, fetch=False):
        """Menjalankan query dengan opsi fetch untuk SELECT"""
        start_time = time.time()
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid if cursor.lastrowid else True
            
            elapsed = time.time() - start_time
            logger.debug(f"Query executed in {elapsed:.3f}s: {query[:50]}...")
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
