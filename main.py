from fastapi import FastAPI
app = FastAPI(title="API de gastos")
@app.get("/")
def inicio():
    return {"mensaje": "API de gastos funcionando"}

