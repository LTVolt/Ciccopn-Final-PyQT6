import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig:
    @staticmethod
    def from_env() -> dict:
        return {
            "host": os.getenv("DB_HOST", "172.23.21.121"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER", "6083062"),
            "password": os.getenv("DB_PASSWORD", "Joao6083062"),
            "database": os.getenv("DB_NAME", "imociccopngrupo1"),
        }


@contextmanager
def get_connection():
    conn = mysql.connector.connect(**DatabaseConfig.from_env())
    try:
        yield conn
    finally:
        conn.close()
