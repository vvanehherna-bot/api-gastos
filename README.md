# API de gastos

API REST para llevar el control de gastos personales. Permite registrar gastos, consultarlos, editarlos, borrarlos y ver cuánto se gastó por categoría.

## Tecnologías

- Python 3
- FastAPI
- SQLite
- Uvicorn

## Instalación

```bash
git clone https://github.com/vvanehherna-bot/api-gastos.git
cd api-gastos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn main:app --reload
```

La documentación interactiva (Swagger) queda en http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /gastos | Crear un gasto |
| GET | /gastos | Listar todos los gastos |
| PUT | /gastos/{id} | Editar un gasto |
| DELETE | /gastos/{id} | Borrar un gasto |
| GET | /resumen | Total por categoría (filtro opcional `?mes=AAAA-MM`) |

## Ejemplo

Crear un gasto:

```json
{"monto": 150.5, "categoria": "comida", "fecha": "2026-11-15"}
```

## Autora

Vanessa Hernández, estudiante de Desarrollo de Software Multiplataforma.
