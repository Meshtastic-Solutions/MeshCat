import json
import os
import typer
import requests
from .socat import start_socat_client, stop_socat_all

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
    response = requests.get(f"{SERVER_URL}")
    if response.status_code == 200:
        for devices in response.json():
            if devices.get("port").get("device") == port:
              start_socat_client(MESHCAT_HOST, devices.get("tcp_port"))

    return { "message": f"Could not find running device {port}" }

@app.command()
def update(port: str, firmware_path: str):
    with open(firmware_path, 'rb') as file:
        files = {'upload_file': file}
        print(f"Updating device {port} with firmware {firmware_path}")
        response = requests.post(f"{SERVER_URL}/update?port={port}", files=files)
        if response.status_code == 200:
            print(f"Device {port} updated")
            print(json.dumps(response.json(), indent=2))

    return { "message": f"Could not find running device {port}" }

@app.command()
def dfu(port: str):
    response = requests.post(f"{SERVER_URL}/dfu?port={port}")
    if response.status_code == 200:
        print(f"Device {port} in DFU mode")
        print(json.dumps(response.json(), indent=2))

    return { "message": f"Could not find running device {port}" }

@app.command()
def stop(port: str):
    response = requests.post(f"{SERVER_URL}/stop?port={port}")
    if response.status_code == 200:
        stop_socat_all()
        print(f"Device stopped on port {port}")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failure status code: {response.status_code}")

if __name__ == "__main__":
    app()
