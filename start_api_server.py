import uvicorn

from app.api.app import app  # noqa: F401 (representing for command below)

if __name__ == "__main__":
    uvicorn.run(app="app.api.app:app", host="localhost", port=8000, reload=True)
