import json
import os
import typer
import requests
from .socat import start_socat_client, stop_socat

app = typer.Typer()

MESHCAT_HOST = os.environ.get("MESHCAT_HOST", "localhost")
MESHCAT_PORT = os.environ.get("MESHCAT_PORT", 6900)

SERVER_URL = f"http://{MESHCAT_HOST}:{MESHCAT_PORT}"

@app.command()
def list():
    response = requests.get(f"{SERVER_URL}/")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failure status code: {response.status_code}")

@app.command()
def ports():
    response = requests.get(f"{SERVER_URL}/ports")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failure status code: {response.status_code}")

@app.command()
def connect(port: str):
    response = requests.post(f"{SERVER_URL}/connect?port={port}")
    if response.status_code == 200:
        start_socat_client(MESHCAT_HOST, response.json()["tcp_port"])
        print(f"Device started on port {port}")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failure status code: {response.status_code}")

@app.command()
def reconnect(port: str):
    response = requests.get(f"{SERVER_URL}")
    if response.status_code == 200:
        for devices in response.json():
            if devices.get("port").get("device") == port:
              start_socat_client(MESHCAT_HOST, devices.get("tcp_port"))

    return { "message": f"Could not find running device {port}" }

@app.command()
def stop(port: str):
    response = requests.post(f"{SERVER_URL}/stop?port={port}")
    if response.status_code == 200:
        stop_socat()
        print(f"Device stopped on port {port}")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failure status code: {response.status_code}")

if __name__ == "__main__":
    app()
