# MeshCat (Meshcatstic)

Meshtastic serial device discovery gateway service and cli client built around `socat` and other tooling

![MeshCat Logo](meshcat.svg)

## Requirements

- Posix environment (tested with Ubunutu)
- Python 3.10+ and Poetry (for development)
- socat (`sudo apt install socat`)
- Uvicorn server (comes with pypi installation or poetry install)
- `pipx install meshcatstic`

## Running for development

## Server

- Clone the repository
- Install dependencies with `poetry install`
- Run the service with `poetry run start`

### Endpoints

- `GET /list`: List all connected Meshtastic serial devices.
- `POST /connect?port=/dev/ttymythang`: Initiate a socat server for the client connect to a meshtastic serial device on `/dev/ttymythang`. Should be unecessary to initiate manually, as background service handles this.
- `POST /update?port=/dev/ttymythang`: Flash device with uploaded binary on selected port
- `POST /stop?port=/dev/ttymythang`: Kill socat process on port

## Client

> **Warning**: Requires running with `sudo` because `socat` is creating virtual ports.

- Clone the repository
- Install dependencies with `sudo poetry install`
- Set environment variable with the remote host `MESHCAT_HOST="meshcathostname"`
- List devices on the remote service with `poetry run meshcat list`
- Connect to a device on the remote service with `poetry run meshcat connect /dev/ttyACM0`
- Take the generated TCP portnum for the gateway serial device and use meshtastic cli or any other client to connect to port `/tmp/meshcat{tcpportnum}`
- To update (flash) a remote device on the service, `poetry run meshcat flash /dev/ttymythang firmware-mythang-update.bin`


## Running

After pip installing `meshcatstic`, you can run both the server and client.

To run the server using uvicorn: `uvicorn meshcatstic:app`
To run the client: `meshcat ... command`

## Future features

- Streaming text respsonse for progress
- RP2040 support w/ picotool
- Full erase and flash
