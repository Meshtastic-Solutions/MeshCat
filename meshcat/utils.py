import os
import json
import random
import socket
import random
import subprocess
import time

import serial

ports_started = []

def get_devices_from_json():
    json_file_path = os.path.join(os.path.dirname(__file__), 'devices.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return []

def get_open_tcp_port():
    while True:
        port = random.randint(1024, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            
def start_socat_server(port):
    tcp_port = get_open_tcp_port()
    ports_started.append({port: tcp_port})
    #subprocess.Popen(["socat", "-d", "-d", f"pty,raw,echo=0,link={port},b115200", f"tcp-listen:{tcp_port},reuseaddr,fork"])
    return tcp_port

def stop_socat(port):
    for port_started in ports_started:
        if port in port_started:
            subprocess.Popen(["killall", "socat"])
            ports_started.remove(port_started)

def enter_dfu_mode(port):
    try:
        with serial.Serial(port, 1200) as serial_port:
            serial_port.dtr = False  # Set Data Terminal Ready to False
            time.sleep(0.5)  # Wait for half a second
            serial_port.dtr = True   # Set Data Terminal Ready to True
            return True
    except serial.SerialException as e:
        print(f"Error: {e}")
        return False