
import random
import socket
import subprocess

def get_open_tcp_port():
    while True:
        port = random.randint(3000, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            
def start_socat_server(port):
    tcp_port = get_open_tcp_port()
    subprocess.Popen(["socat", "-d", "-d", f"tcp-listen:{tcp_port},reuseaddr,fork", f"file:{port},nonblock,raw,echo=0,b115200"])
    print(f"Started: socat file:{port},nonblock,raw,echo=0,b115200 tcp-listen:{tcp_port},reuseaddr,fork")
    return tcp_port

def start_socat_client(host, tcp_port):
    process = subprocess.Popen(["socat", f"tcp:{host}:{tcp_port}", f"pty,link=/dev/meshcat{tcp_port},raw,echo=0,group-late=dialout,mode=777"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Started: socat tcp:{host}:{tcp_port} pty,link=/dev/meshcat{tcp_port},raw,group-late=dialout,mode=777")
    stdout, stderr = process.communicate()
    print(f"stdout: {stdout.decode()}")
    print(f"stderr: {stderr.decode()}")
    pass

def stop_socat():
    subprocess.Popen(["kill", "-9", "socat"])

def stop_socat(port, ports_started):
    for port_started in ports_started:
        if port in port_started:
            subprocess.Popen(["kill", "-9", "socat", str(port_started)])
            ports_started.remove(port_started)