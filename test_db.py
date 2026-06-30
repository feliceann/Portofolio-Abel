import mysql.connector
from config import Config

print("Mencoba konek dengan config berikut:")
print("HOST:", Config.MYSQL_CONFIG['host'])
print("USER:", repr(Config.MYSQL_CONFIG['user']))
print("PASSWORD:", repr(Config.MYSQL_CONFIG['password']))
print("DATABASE:", Config.MYSQL_CONFIG['database'])

try:
    conn = mysql.connector.connect(**Config.MYSQL_CONFIG)
    print("BERHASIL KONEK!")
    conn.close()
except Exception as e:
    print("GAGAL:", e)