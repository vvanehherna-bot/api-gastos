from fastapi import FastAPI, HTTPException
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


@app.put("/gastos/{gasto_id}")
def editar_gasto(gasto_id: int, gasto: GastoNuevo):
    with conectar() as conexion:
        cursor = conexion.execute(
            "UPDATE gastos SET monto = ?, categoria = ?, fecha = ? WHERE id = ?",
            (gasto.monto, gasto.categoria, gasto.fecha, gasto_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"id": gasto_id, **gasto.model_dump()}


@app.delete("/gastos/{gasto_id}")
def borrar_gasto(gasto_id: int):
    with conectar() as conexion:
        cursor = conexion.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto eliminado"}


@app.get("/resumen")
def resumen(mes: str | None = None):
    """Total por categoría. Filtro opcional: mes en formato AAAA-MM."""
    consulta = "SELECT categoria, SUM(monto) AS total FROM gastos"
    parametros = []
    if mes:
        consulta += " WHERE fecha LIKE ?"
        parametros.append(f"{mes}%")
    consulta += " GROUP BY categoria ORDER BY total DESC"

    with conectar() as conexion:
        filas = conexion.execute(consulta, parametros).fetchall()

    por_categoria = [dict(fila) for fila in filas]
    total_general = sum(fila["total"] for fila in por_categoria)
    return {"total_general": total_general, "por_categoria": por_categoria}


from fastapi.responses import FileResponse


@app.get("/app", include_in_schema=False)
def pagina():
    return FileResponse("index.html")
