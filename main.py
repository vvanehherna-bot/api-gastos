from fastapi import FastAPI
from pydantic import BaseModel
from database import conectar, crear_tabla
app = FastAPI(title="API de gastos")
crear_tabla()
class GastoNuevo(BaseModel):
   monto: float
   categoria: str
   fecha: str #formato AAAA-MM-DD
@app.get("/")
def inicio():
    return {"mensaje": "API de gastos funcionando"}
@app.post("/gastos")
def crear_gasto(gasto: GastoNuevo):
    with conectar() as conexion:
        cursor = conexion.execute(
           "INSERT INTO gastos(monto, categoria, fecha) VALUES (?, ?, ?)",
           (gasto.monto, gasto.categoria, gasto.fecha),
       )
        nuevo_id = cursor.lastrowid
    return {"id": nuevo_id, **gasto.model_dump()}
@app.get("/gastos")
def listar_gastos():
    with conectar() as conexion:
        filas = conexion.execute("SELECT * FROM gastos").fetchall()
    return [dict(fila) for fila in filas]
