import esptool
from nordicsemi.dfu.dfu import Dfu
from nordicsemi.dfu.dfu_transport_serial import DfuTransportSerial

def update_firmware_esp32(port: str, firmware_path):
    command = ['--port', port, '--baud', '115200', 'write_flash', '0x10000', firmware_path]
    print('Using esptool command %s' % ' '.join(command))
    esptool.main(command)

def update_firmware_nrf52840(port: str, firmware_path):
    """Program a device with bootloader that support serial DFU"""
    serial_backend = DfuTransportSerial(com_port=port, touch=1200)
    #serial_backend.register_events_callback(DfuEvent.PROGRESS_EVENT, update_progress)
    
    dfu = Dfu(firmware_path, dfu_transport=serial_backend)
    dfu.dfu_send_images()

