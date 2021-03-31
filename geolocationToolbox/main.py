#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Authors: Jacob Zelko (alias TheCedarPrince)
         Pradyumna B Suresha (alias Pradyumna94)
Last Modified: Mar 22nd, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

from hardware.system_toolbox import SystemToolbox
from datetime import datetime
from pandas import DataFrame
from time import sleep

import subprocess
import socket
import sys


# This function is useful in running the script eternally and to check any multiple runs of the same script
def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage colleted when the function exists
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    
    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print('I got the lock')
    except socket.error:
        print('lock exists')
        sys.exit()

def main():

    refresh_time = 1
    
    syncTime = subprocess.check_output(['/home/pi/OS_Edge_Compute_Data_Capture_RPi/geolocationToolbox/syncTime.sh'])

    sys_tool = SystemToolbox.SystemTool()
    bt_tool = SystemToolbox.BluetoothTool(bluetooth_module=sys_tool
                                          .bluetooth_module())

    # TODO: Fix Documentation here; this begins the bluetooth scanning thread
    bt_tool.bluetooth_scan()
    sleep(3)

    main_results = DataFrame({"addr" : [], "rssi" : [], "time_present" : []})
    
    # Previously create a folder called 'data'
    filename = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/geolocationToolbox/' + datetime.strftime(datetime.now(), "%m_%d_%y_%H_%M_%S_log.txt")
    
    with open(filename, "a") as f:
        f.write("UTC, ADDR, RSSI\n")

    while True:
        scan_results = bt_tool.return_devices()

        for device in scan_results.addr.values:
            if device not in main_results.addr.values:
                # NOTE: This method is not the most efficient method to use here
                main_results = main_results.append({"addr": device, "rssi": 0
                                                    ,"time_present" : 0},
                                                    ignore_index=True)
            else:
                row = scan_results.index[scan_results["addr"] == device][0]
                rssi = scan_results.at[row, "rssi"]
                main_results.at[row, "rssi"] = rssi
                main_results.at[row, "time_present"] += 1

        with open(filename, "a") as f:
            for timestamp, addr, rssi in zip(scan_results.time, scan_results.addr, scan_results.rssi):
                f.write("{}, {}, {}\n".format(timestamp, addr, rssi))
        
    
        sleep(refresh_time)

if __name__ == "__main__":
    
    if True:
        get_lock('main')

    while True:
        main()
