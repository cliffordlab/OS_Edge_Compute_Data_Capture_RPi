#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 5th, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

import subprocess
import os

def ComputeMSE(signal = [],
               scales = 20,
               a = 1,
               mseScriptLoc = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/'):
    
    if signal == []:
        return []
    
    # Write `signal` to a temporary file.
    with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/idt.txt', 'w') as f:
        for item in signal:
                f.write("%s\n" % item)

    # Execute `mse.c` to compute MSE.
    process = subprocess.check_output([mseScriptLoc+"./mse -n " + str(scales) + " -a " + str(a) + " </home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/idt.txt >/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/mse.txt"], shell=True)
    
    os.unlink('/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/idt.txt')
    # Read `.mse.txt` and store the MSE information in python list.
    mse = []
    with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/mse.txt', 'r') as fp:
        for ii in range(5):
            line = fp.readline()
        
        while(line):
            splits = line.split()
            mse.append(float(splits[1]))
            line = fp.readline()
    
    os.unlink('/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/mse.txt')
    return mse
