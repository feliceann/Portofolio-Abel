import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = int(os.getenv('DB_PORT', 4000))
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'felicia_anabel')
    DB_SSL_DISABLED = os.getenv('DB_SSL_DISABLED', 'False').lower() == 'true'
    DB_CA_PATH = os.getenv('DB_CA_PATH', '')

    MYSQL_CONFIG = {
        'host': DB_HOST,
        'port': DB_PORT,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'database': DB_NAME,
        'autocommit': False,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }

    if DB_CA_PATH:
        MYSQL_CONFIG['ssl_ca'] = DB_CA_PATH
    elif not DB_SSL_DISABLED:
        MYSQL_CONFIG['ssl_disabled'] = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', '')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '')

    RESEND_API_KEY = os.getenv('RESEND_API_KEY', '')
    RESEND_FROM_EMAIL = os.getenv('RESEND_FROM_EMAIL', 'Portfolio <onboarding@resend.dev>')
    CONTACT_RECEIVER_EMAIL = os.getenv('CONTACT_RECEIVER_EMAIL', '')
