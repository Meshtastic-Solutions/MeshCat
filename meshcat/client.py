import os
import typer
import requests
from .utils import start_socat_client, stop_socat
import yaml

app = typer.Typer()

config = {}
if os.path.exists("./client.yaml"):
    with open("./client.yaml", "r") as file:
        config = yaml.safe_load(file)
else:
    print("No client.yaml file found, defaulting to localhost:6900")

MESHCAT_HOST = config.get("MESHCAT_HOST", "localhost")
MESHCAT_PORT = config.get("MESHCAT_PORT", 6900)

SERVER_URL = f"http://{MESHCAT_HOST}:{MESHCAT_PORT}"

@app.command()
def list():
    response = requests.get(f"{SERVER_URL}/")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failure status code: {response.status_code}")


@app.command()
def connect(port: str):
    response = requests.post(f"{SERVER_URL}/connect?port={port}")
    if response.status_code == 200:
        print(f"Device started on port {port}")
        print(response.json())
    else:
        print(f"Failure status code: {response.status_code}")

if __name__ == "__main__":
    app()
