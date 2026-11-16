import sqlite3
DB = "gastos.db"
def conectar():
    conexion = sqlite3.connect(DB)
    conexion.row_factory = sqlite3.Row
    return conexion
def crear_tabla():
    with conectar() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            monto REAL NOT NULL, 
            categoria TEXT NOT NULL, 
            fecha TEXT NOT NULL
            )
            """
                         )
