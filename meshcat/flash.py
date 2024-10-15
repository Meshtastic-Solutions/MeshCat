import esptool
from nordicsemi.dfu.dfu import Dfu
from nordicsemi.dfu.dfu_transport_serial import DfuTransportSerial

def update_firmware_esp32(port, firmware_path):
    esp = esptool.ESPLoader.detect_chip(port=port, initial_baud=115200)
    esp.connect()
    esptool.write_flash(
        esp=esp,
        address=0x10000,
        filename=firmware_path,
        flash_size='detect',
        flash_mode='dio',
        flash_freq='40m'
    )
    # Disconnect from the ESP device
    esp.hard_reset()

def update_firmware_nrf52840(port, firmware_path):
    """Program a device with bootloader that support serial DFU"""
    serial_backend = DfuTransportSerial(port, 115200, flowcontrol=False, singlebank=False, touch=True)
    #serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, update_progress)
    
    dfu = Dfu(firmware_path, dfu_transport=serial_backend)
    dfu.dfu_send_images()

