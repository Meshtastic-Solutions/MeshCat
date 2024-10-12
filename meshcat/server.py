import subprocess
import uvicorn
from fastapi import FastAPI
import serial
import serial.tools.list_ports
from .utils import get_devices_from_json, get_open_tcp_port, enter_dfu_mode, ports_started

devices_from_json = get_devices_from_json()

def find_device(vid, pid, manufacturer):
    for device in devices_from_json:
        matchesVid = not device["vid"] or vid in device["vid"]
        matchesPid = not device["pid"] or pid in device["pid"]
        matchesManufacturer = not device["manufacturer"] or manufacturer in device["manufacturer"]
        if matchesVid and matchesPid and matchesManufacturer:
            return device
    return None


app = FastAPI()

@app.get("/")
def get_device_list():
    ports = serial.tools.list_ports.comports()

    ports = list(map(lambda port: {
        "pio_env": find_device(port.vid, port.pid, port.manufacturer).get("pio_env"),
        "arch": find_device(port.vid, port.pid, port.manufacturer).get("arch"),
        "requires_dfu": find_device(port.vid, port.pid, port.manufacturer).get("requires_dfu"),
        "is_running": port.device in ports_started,
        "tcp_port": next((tcp_port for port_started in ports_started if port.device in port_started for tcp_port in port_started.values()), None),
        "port": port
    }, ports))
    return ports

@app.post("/start")
def start_device(port):
    return { "message": "Device started", "tcp_port": start_socat_server(port) }

@app.post("/stop")
def stop_device(port):
    stop_socat(port)
    return { "message": "Device stopped" }

@app.post("/dfu")
def dfu(port):
    result = enter_dfu_mode(port)
    return { "message": "Entering DFU mode... the device may re-appear under a different serial port" if result else "Error attempting to enter DFU mode" }

def start():
    """Launched with `poetry run start` at root directory"""
    uvicorn.run("meshcat.server:app", host="0.0.0.0", port=6900, reload=True)
