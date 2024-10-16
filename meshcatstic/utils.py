import os
import json
import time

import serial

def get_devices_from_json():
    json_file_path = os.path.join(os.path.dirname(__file__), 'devices.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return []

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

def write_temp_file(data, filename: str):
    with open(filename, 'wb') as file:
        file.write(data)
    return filename

def print_mesh_cat():
    print("Starting MeshCat...")
    print("""
                           @@@@@                                     @@@@@@                         
                           @@@@@@@@@@                           @@@@@@@@@@                          
                    @@@    @@@  @@@@@@@@@@                 @@@@@@@@@@         @@@                   
                    @@@    @@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@                   
                    @@@    @@@                                      @@@@@@@@@@@@@                   
                    @@@    @@@                                   @@@@@@@      @@@                   
                    @@@    @@@                                    @           @@@                   
                    @@@    @@@                                                @@@                   
                    @@@     @@                                                @@@                   
                     @@                                                       @@@                   
                     @@                                                       @@@                   
                    @@@             @@@@@                   @@@@@@@           @@@@                  
                   @@@            @@@@@@@@                 @@@@@@@@@           @@@@                 
                  @@@             @@@@@@@@@                @@@@@@@@@            @@@                 
                 @@@@             @@@@@@@@                 @@@@@@@@@             @@@                
      @@@        @@@              @@@@@@@@                  @@@@@@@              @@@        @@@     
      @@@@@@@@   @@@                @@@@                                          @@@ @@@@@@@@@     
           @@@@@@@@@                                                             @@@@@@@@@@         
                @@@@@@@@                                                      @@@@@@@               
      @@@@@@@@@@@@@@@@@@                     @                                @@@@@@@@@@@@@@@@@     
      @@@@@@@@@@@@@@@@@@                    @@@     @@@                       @@@@@@@@@@@@@@@@@     
                 @@@@@@@                  @@@@    @@@@@@                      @@@@@@@               
           @@@@@@@@@@@@                  @@@@    @@@@ @@@@                     @@@@@@@@@@@@         
      @@@@@@@@@@@  @@@                  @@@     @@@@   @@@@                    @@@@   @@@@@@@@@     
      @@@@         @@@@                @@@     @@@@      @@@                   @@@           @@     
                    @@@@              @@@     @@@@        @@@                @@@@                   
                      @@@            @@@     @@@           @@@@             @@@@                    
                       @@@@           @       @             @@            @@@@@                     
                         @@@                                            @@@@@                       
                          @@@@@                                       @@@@@@                        
                            @@@@@                                  @@@@@@                           
                               @@@@@@                           @@@@@@@                             
                                  @@@@@@@@@@              @@@@@@@@@                                 
                                      @@@@@@@@@@@@@@@@@@@@@@@@@                                     
    """)