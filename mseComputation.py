#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 21th, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

from datetime import datetime, date, timedelta, time

import scipy.io as sio
import numpy as np

import subprocess
import itertools
import argparse
import errno
import time
import sys
import os

def ComputeMSE(signal = [],
               scales = 20,
               a = 1,
               mseScriptLoc = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/codes/'):
    
    if signal == []:
        return []
    
    # Write `signal` to a temporary file.
    with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/idt.txt', 'w') as f:
        for item in signal:
                f.write("%s\n" % item)

    # Execute `mse.c` to compute MSE.
    process = subprocess.check_output([mseScriptLoc+"./mse -n " + str(scales) + " -a " + str(a) + " </home/pi/OS_Edge_Compute_Data_Capture_RPi/idt.txt >/home/pi/OS_Edge_Compute_Data_Capture_RPi/mse.txt"], shell=True)
    
    os.unlink('/home/pi/OS_Edge_Compute_Data_Capture_RPi/idt.txt')
    # Read `.mse.txt` and store the MSE information in python list.
    mse = []
    with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/mse.txt', 'r') as fp:
        for ii in range(5):
            line = fp.readline()
        
        while(line):
            splits = line.split()
            mse.append(float(splits[1]))
            line = fp.readline()
    
    os.unlink('/home/pi/OS_Edge_Compute_Data_Capture_RPi/mse.txt')
    return mse

if __name__ == '__main__':
    
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpuSerial", dest="cpuSerial", help="Serial ID of CPU")
    parser.add_argument("--dateTime", dest="dateTime", help="Start date-time of the file")
    parser.add_argument("--nScales", dest = "nScales", default = "20", help="Use `N` scales to compute MSE")
    parser.add_argument("--sHour", dest = "sHour", default = "22", help="Start time for MSE computation, Eg: 22")
    parser.add_argument("--eHour", dest = "eHour", default = "6", help="End time for MSE computation, Eg: 6")
    args = parser.parse_args()
    scales = int(args.nScales)
    sHour = int(args.sHour)
    eHour = int(args.eHour)
    cpuSerial = args.cpuSerial
    dateTime = args.dateTime
    
    # Construct filenames
    pirFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/' + cpuSerial + '_' +  dateTime + '_pirTimestamps.txt'
    pirMseFileName = cpuSerial + '_' +  dateTime + '_pirTimestamps_mse'
    pirMseFolder = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/mse/'
    camFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_GlobalSignals.txt'
    camMseFileName = cpuSerial + '_' + dateTime + '_GDS_mse'
    camMseFolder = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/mse/'
    camTimeFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_times.txt'
    mseScriptLoc = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/codes/'
    a = 1;

    # Process PIR data
    # Read data in PIR file to pirArray
    with open(pirFile, 'r') as fp:
        pirArray = fp.readlines()
    
    pirArray = [int(x.strip()) for x in pirArray]
    
    # Find posix timestamps for start and end time.
    hourObject = [datetime.fromtimestamp(x).hour for x in pirArray]
    # Debug purposes
    """
    minObject = [datetime.fromtimestamp(x).minute for x in pirArray]
    txPirArray = [hourObject[ii] + minObject[ii] / 60 for ii in range(len(pirArray))]
    import numpy as np
    y = np.ones([len(pirArray),1])
    import matplotlib.pyplot as plt
    plt.stem(txPirArray,y)
    plt.show()
    """
    pirTemp = []
    for idx, x in enumerate(hourObject):
        if x >= sHour or x <= eHour:
            pirTemp.append(pirArray[idx])
    pirArray = pirTemp.copy()       
    
    # Difference signal and Activity signal computation
    diffSignal = [j - i for i,j in zip( pirArray[:-1], pirArray[1:] )]
    actSignal = [1/x for x in diffSignal]
    
    # Compute MSE for PIR signal
    msePir = ComputeMSE( signal = actSignal,
                         scales = scales,
                         a = a,
                         mseScriptLoc = mseScriptLoc )
    
    # Create a MSE folder inside PIR folder
    try:
        os.mkdir(pirMseFolder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Create content for PIR mse Header file
    pirHeader = 'File=' + pirFile + '\n' + 'n=' + str(scales) + '\n' + 'a=' + str(a) + '\n' +  'script=' + mseScriptLoc + 'mse.c'
    
    # Write PIR mse Header file
    pirHeaderFile = pirMseFolder + pirMseFileName + '.hea'
    with open(pirHeaderFile, 'w') as fp:
        fp.write(pirHeader)
    
    # Save mse files
    msePirFile = pirMseFolder + pirMseFileName + '.mat'                      
    sio.savemat(msePirFile, {'mse':msePir})
    
    # Process IR camera data
    # Read data in Camera file to camArray
    with open(camFile, 'r') as fp:
        camArray = fp.readlines()
    
    camArray = [x.strip() for x in camArray]    
    # Old method
    #camArray = [float(x.split(',')[-1]) for x in camArray]
    # New method
    camArray = [float(x.split(',')[0]) for x in camArray]
    # Read Camera Timestamp file
    with open(camTimeFile, 'r') as fp:
        timeArray = fp.readlines()
    
    timeArray = [(x.strip()) for x in timeArray]
    timeArray = [int(x.split(',')[-1]) for x in timeArray]
    #timeArray = list(itertools.chain.from_iterable(itertools.repeat(x, 5) for x in timeArray))
    if len(timeArray) != len(camArray):
        print('Length of timeArray = '+str(len(timeArray)))
        print('Length of camArray = '+str(len(camArray)))
        sys.exit('Length of timeArray and cam Array are not equal.')
    
    hourObject = [datetime.fromtimestamp(x).hour for x in timeArray]
    camTemp = []
    for idx, x in enumerate(hourObject):
        if x >= sHour or x <= eHour:
            camTemp.append(camArray[idx])
    camArray = camTemp.copy()
    
    # Compute MSE for IR cameara difference signal
    mseCam = ComputeMSE( signal = camArray,
                         scales = scales,
                         a = a,
                         mseScriptLoc = mseScriptLoc )
                         
    # Create a MSE folder inside IR folder
    try:
        os.mkdir(camMseFolder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
                         
    # Create content for IR camera difference signal mse Header file
    camHeader = 'File=' + camFile + '\n' + 'n=' + str(scales) + '\n' + 'a=' + str(a) + '\n' + 'script=' + mseScriptLoc + 'mse.c'
                
    # Write IR camera difference signal mse Header file
    camHeaderFile = camMseFolder + camMseFileName + '.hea'
    with open(camHeaderFile, 'w') as fp:
        fp.write(camHeader)
                         
    # Save mse files
    mseCamFile = camMseFolder + camMseFileName + '.mat'
    sio.savemat(mseCamFile, {'mse':mseCam})
