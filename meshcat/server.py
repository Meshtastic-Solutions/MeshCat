import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, File, UploadFile
import serial
import serial.tools.list_ports

from meshcat.flash import update_firmware_esp32, update_firmware_nrf52840
from .utils import get_devices_from_json, enter_dfu_mode, write_temp_file
from .socat import start_socat_server, stop_socat, stop_socat_all

ports_running = []
ports_flashing = []

devices_from_json = get_devices_from_json()

def find_device(vid, pid, manufacturer):
    for device in devices_from_json:
        matchesVid = device["vid"] is None or vid in device["vid"]
        matchesPid = device["pid"] is None or pid in device["pid"]
        matchesManufacturer = device["manufacturer"] is None or (manufacturer or "").lower() in device["manufacturer"]
        # print(f"matchesVid: {matchesVid}, matchesPid: {matchesPid}, matchesManufacturer: {matchesManufacturer}")
        # print (f"device: {device}")
        if matchesVid and matchesPid and matchesManufacturer:
            return device
    return {}

class MeshCatProcessRunner:
    def __init__(self):
        self.value = self.find_and_start_ports()

    async def run_main(self):
        while True:
            await asyncio.sleep(0.3)
            self.value = self.find_and_start_ports()

    def find_and_start_ports(self):
        ports = list(map(lambda port: {
                "pio_env": find_device(port.vid, port.pid, port.manufacturer).get("pio_env"),
                "arch": find_device(port.vid, port.pid, port.manufacturer).get("arch"),
                "requires_dfu": find_device(port.vid, port.pid, port.manufacturer).get("requires_dfu"),
                "state": "stopped",
                "tcp_port": next((tcp_port for port_started in ports_running if port.device in port_started for tcp_port in port_started.values()), None),
                "port": port
            }, serial.tools.list_ports.comports()))
        ports = [port for port in ports if port["pio_env"] is not None]
        for port in ports:
            is_running = any(port.device in port_started for port_started in ports_running)
            is_flashing = any(port.device in ports_flashing for ports_flashing in ports_flashing)
            remote_serial_port = port["port"].device
            if is_flashing:
                port["state"] = "flashing"
                continue
            elif is_running:
                port["state"] = "running"
                continue

            tcp_port = start_socat_server(remote_serial_port)
            ports_running.append({remote_serial_port: tcp_port})
            # Update the port with the new tcp_port and set is_running to True
            port["tcp_port"] = tcp_port
            port["virtual_port"] = f"/dev/meshcat{tcp_port}"
            port["state"] = "running"
        return ports

runner = MeshCatProcessRunner()

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(runner.run_main())
    yield
    task.cancel()
    stop_socat_all()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def get_device_list():
    return runner.value

@app.get("/ports")
def get_serial_ports_raw():
    return serial.tools.list_ports.comports()

# Probably should deprecated this endpoint
@app.post("/connect")
def start_connect(port: str):
    tcp_port = start_socat_server(port)
    ports_running.append({port: tcp_port})
    return { "message": "Device started", "tcp_port": tcp_port }

@app.post("/update")
def flash_device(port: str, upload_file: UploadFile = File(...)):
    ports = runner.value
    found_device = next((port for port in ports if port["port"].device == port), None)
    ports_flashing.append(port)
    firmware_path = f"/tmp/{upload_file.filename}"
    write_temp_file(upload_file.file.read(), firmware_path)
    if found_device.get("arch") == "nrf52840":
        update_firmware_nrf52840(port.device, firmware_path)
    elif found_device.get("arch") == "esp32":
        update_firmware_esp32(port.device, firmware_path)
    # Remove the port from the flashing list
    ports_flashing = [port_started for port_started in ports_flashing if port not in port_started]
    return { "message": "Flashing device" }

@app.post("/stop")
def stop_connection(port: str):
    stop_socat(port, ports_running=ports_running)
    ports_running = [port_started for port_started in ports_running if port not in port_started]
    return { "message": "Device stopped" }

@app.post("/dfu")
def dfu(port):
    result = enter_dfu_mode(port)
    return { "message": "Entering DFU mode... the device may re-appear under a different serial port" if result else "Error attempting to enter DFU mode" }

def start():
    """Launched with `poetry run start` at root directory"""
    uvicorn.run("meshcat.server:app", host="0.0.0.0", port=6900, reload=True)
