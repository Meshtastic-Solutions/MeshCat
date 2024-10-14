import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
import serial
import serial.tools.list_ports
from .utils import get_devices_from_json, enter_dfu_mode
from .socat import start_socat_server, stop_socat

# Assuming ports_started is a global variable or needs to be defined
ports_started = []

devices_from_json = get_devices_from_json()

class MeshCatProcessRunner:
    def __init__(self):
        self.value = self.find_and_start_ports()

    async def run_main(self):
        while True:
            await asyncio.sleep(0.2)
            ports = self.find_and_start_ports()
            self.value = ports

    def find_and_start_ports(self):
        ports = list(map(lambda port: {
                "pio_env": find_device(port.vid, port.pid, port.manufacturer).get("pio_env"),
                "arch": find_device(port.vid, port.pid, port.manufacturer).get("arch"),
                "requires_dfu": find_device(port.vid, port.pid, port.manufacturer).get("requires_dfu"),
                "is_running": port.device in ports_started,
                "tcp_port": next((tcp_port for port_started in ports_started if port.device in port_started for tcp_port in port_started.values()), None),
                "port": port
            }, serial.tools.list_ports.comports()))
        ports = [port for port in ports if port["pio_env"] is not None]
        for port in ports:
            if port["is_running"]:
                continue
            tcp_port = start_socat_server(port)
            ports_started.append({port: tcp_port})
                # Update the port with the new tcp_port and set is_running to True
            port["tcp_port"] = tcp_port
            port["is_running"] = True
        return ports

runner = MeshCatProcessRunner()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(runner.run_main())
    yield
    task.cancel()
    stop_socat()

def find_device(vid, pid, manufacturer):
    for device in devices_from_json:
        matchesVid = device["vid"] is None or vid in device["vid"]
        matchesPid = device["pid"] is None or pid in device["pid"]
        matchesManufacturer = device["manufacturer"] is None or (manufacturer or "").lower() in device["manufacturer"]
        if matchesVid and matchesPid and matchesManufacturer:
            return device
    return {}

app = FastAPI()

@app.get("/")
def get_device_list():
    return runner.value
    # ports = serial.tools.list_ports.comports()
    # ports = list(map(lambda port: {
    #     "pio_env": find_device(port.vid, port.pid, port.manufacturer).get("pio_env"),
    #     "arch": find_device(port.vid, port.pid, port.manufacturer).get("arch"),
    #     "requires_dfu": find_device(port.vid, port.pid, port.manufacturer).get("requires_dfu"),
    #     "is_running": port.device in ports_started,
    #     "tcp_port": next((tcp_port for port_started in ports_started if port.device in port_started for tcp_port in port_started.values()), None),
    #     "port": port
    # }, ports))
    # return [port for port in ports if port["pio_env"] is not None]

@app.post("/connect")
def start_connect(port):
    tcp_port = start_socat_server(port)
    ports_started.append({port: tcp_port})
    return { "message": "Device started", "tcp_port": tcp_port }

@app.post("/stop")
def stop_connection(port):
    stop_socat(port)
    ports_started = [port_started for port_started in ports_started if port not in port_started]
    return { "message": "Device stopped" }

@app.post("/dfu")
def dfu(port):
    result = enter_dfu_mode(port)
    return { "message": "Entering DFU mode... the device may re-appear under a different serial port" if result else "Error attempting to enter DFU mode" }

def start():
    """Launched with `poetry run start` at root directory"""
    uvicorn.run("meshcat.server:app", host="0.0.0.0", port=6900, reload=True)
