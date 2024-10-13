# MeshCat

Meshtastic serial device discovery gateway service built around `socat`

## Requirements

- Posix environment (tested with Ubunutu)
- Python 3.10+ and Poetry
- socat (`sudo apt install socat`)

## Running for development

## Server

- Clone the repository
- Install dependencies with `poetry install`
- Run the service with `poetry run start`

### Endpoints

- `GET /list`: List all connected Meshtastic serial devices.
- `POST /connect?port=/dev/ttymythang`: Initiate a socat server for the client connect to a meshtastic serial device on `/dev/ttymythang`.
- `POST /stop?port=/dev/ttymythang`: Kill socat process on port
- `POST /dfu?port=/dev/ttymythang`: Initiate 1200bps reset on selected port

## Client

> **Warning**: Requires running with `sudo` because `socat` is creating virtual ports.

- Clone the repository
- Install dependencies with `sudo poetry install`
- List devices on the remote service with `MESHCAT_HOST="meshcathostname" poetry run meshcat list`
- Connect to a device on the remote service with `MESHCAT_HOST="meshcathostname" poetry run meshcat connect /dev/ttyACM0`
- Take the generated TCP portnum for the gateway serial device and use meshtastic cli or any other client to connect to port `/dev/meshcat{tcpportnum}`

## Running as agent in production

TODO...
