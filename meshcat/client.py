import typer
import requests
from .utils import start_socat_client, stop_socat

app = typer.Typer()

@app.command()
def list(host: str, server_port: int = 6900):
    response = requests.get(f"http://{host}:{server_port}/")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to call API. Status code: {response.status_code}")


@app.command()
def connect(host: str, port: int = 6900, formal: bool = False):
    response = requests.post(f"http://{name}/start")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to call API. Status code: {response.status_code}")

if __name__ == "__main__":
    app()
