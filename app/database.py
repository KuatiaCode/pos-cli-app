import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "/app/data/pos.db")


def obtener_conexion() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)
