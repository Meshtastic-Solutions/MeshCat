import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

def start():
    """Launched with `poetry run start` at root directory"""
    # trunk-ignore(bandit/B104)
    uvicorn.run("meshcat.main:app", host="0.0.0.0", port=6900, reload=True)
