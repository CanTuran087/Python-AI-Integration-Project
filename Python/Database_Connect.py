import os

# Bağlantı bilgilerini döndüren fonksiyon
class ConnectionSQL:
    @staticmethod
    def get_connection_info():
        return {
            "host": os.getenv("DB_HOST"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT")
        }