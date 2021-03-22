#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 20th, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

import scipy.io as sio
import numpy as np

import argparse
import errno
import os

if __name__ == '__main__':
    #import pdb;pdb.set_trace()
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpuSerial", dest="cpuSerial", help="Serial ID of CPU")
    parser.add_argument("--dateTime", dest="dateTime", help="Start date-time of the file")
    args = parser.parse_args()
    cpuSerial = args.cpuSerial
    dateTime = args.dateTime
    
    # Construct filenames that have to be binarized
    pirFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/' + cpuSerial + '_' +  dateTime + '_pirTimestamps.txt'
    camFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_GlobalSignals.txt'
    LDSFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_LDS.txt'
    LDPCFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_LDPC.txt'
    camTimeFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/' + cpuSerial + '_' + dateTime + '_times.txt'
    colorFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/' + cpuSerial + '_' + dateTime + '_color.txt'
    thFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/' + cpuSerial + '_' + dateTime + '_th.txt'
    
#####PIR data
    # Read data in PIR file to pirArray
    splits = pirFile.split('/')
    fileName = splits[-1][:-4]
    with open(pirFile, 'r') as fp:
        pirArray = fp.readlines()
    
    pirArray = [int(x.strip()) for x in pirArray]
    
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise             
        pass
    
    # Save binarized PIR file
    pirMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/bin/' + fileName + '.mat'                      
    sio.savemat(pirMatFile, {'val':pirArray})
    
##### Process Camera data
    # Read data in camera file to camArray
    splits = camFile.split('/')
    fileName = splits[-1][:-18]
    with open(camFile, 'r') as fp:
        camArray = fp.readlines()
    
    camArray = [x.strip() for x in camArray]
    
    # Split the data into four channels namely red, green, blue, grey 
    # This is the old way
    camScaledArray = [float(x.split(',')[-1]) for x in camArray]
    camArray = [float(x.split(',')[0]) for x in camArray]
    
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Save binarized IR camera files
    camMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_GDS.mat'                    
    sio.savemat(camMatFile, {'val':camArray})

    camScaledMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_GDPC.mat'                    
    sio.savemat(camScaledMatFile, {'val':camScaledArray})
    
##### Process Fine Camera data
    # Read data in camera file to camArray
    splits = LDSFile.split('/')
    fileName = splits[-1][:-4]
    with open(LDSFile, 'r') as fp:
        LDSArray = fp.readlines()
    
    LDSArray = [x.strip() for x in LDSArray]
    
    # Read the 20 channels into array
    LDSArray = [x.split(',') for x in LDSArray]
    LDSArray = [[float(x) for x in row] for row in LDSArray]

    nChannels = float(len(LDSArray[0]))
    LDSArrayPart1 = [[x for x in row[:int(nChannels/4)]] for row in LDSArray]
    LDSArrayPart2 = [[x for x in row[int(nChannels/4):int(nChannels/2)]] for row in LDSArray]
    LDSArrayPart3 = [[x for x in row[int(nChannels/2):int(3*nChannels/4)]] for row in LDSArray]
    LDSArrayPart4 = [[x for x in row[int(3*nChannels/4):]] for row in LDSArray]
    
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Save binarized Fine camera files
    camFineMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part1.mat'                    
    sio.savemat(camFineMatFile, {'val':LDSArrayPart1})
    
    camFineMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part2.mat'                    
    sio.savemat(camFineMatFile, {'val':LDSArrayPart2})
    
    camFineMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part3.mat'                    
    sio.savemat(camFineMatFile, {'val':LDSArrayPart3})
    
    camFineMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part4.mat'                    
    sio.savemat(camFineMatFile, {'val':LDSArrayPart4})
    
##### Process Fine Scaled Camera data
    # Read data in camera file to camArray
    splits = LDPCFile.split('/')
    fileName = splits[-1][:-4]
    with open(LDPCFile, 'r') as fp:
        LDPCArray = fp.readlines()
    
    LDPCArray = [x.strip() for x in LDPCArray]
    
    # Read the 20 channels into array
    LDPCArray = [x.split(',') for x in LDPCArray]
    LDPCArray = [[float(x) for x in row] for row in LDPCArray]
    
    nChannels = float(len(LDPCArray[0]))
    LDPCArrayPart1 = [[x for x in row[:int(nChannels/4)]] for row in LDPCArray]
    LDPCArrayPart2 = [[x for x in row[int(nChannels/4):int(nChannels/2)]] for row in LDPCArray]
    LDPCArrayPart3 = [[x for x in row[int(nChannels/2):int(3*nChannels/4)]] for row in LDPCArray]
    LDPCArrayPart4 = [[x for x in row[int(3*nChannels/4):]] for row in LDPCArray]
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Save binarized Fine camera files
    camFineScaledMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part1.mat'                    
    sio.savemat(camFineScaledMatFile, {'val':LDPCArrayPart1})
    
    camFineScaledMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part2.mat'                    
    sio.savemat(camFineScaledMatFile, {'val':LDPCArrayPart2})

    camFineScaledMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part3.mat'                    
    sio.savemat(camFineScaledMatFile, {'val':LDPCArrayPart3})
    
    camFineScaledMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_part4.mat'                    
    sio.savemat(camFineScaledMatFile, {'val':LDPCArrayPart4})
    
##### Process Time File to generate header file and missing timestamps file
    # Read Camera Timestamp file
    splits = camFile.split('/')
    fileName = splits[-1][:-4]
    with open(camTimeFile, 'r') as fp:
        timeArray = fp.readlines()
    
    # Find the missed timestamps
    timeArray = [x.strip() for x in timeArray]
    floatTimeArray = [float(x.split(',')[0]) for x in timeArray]
    timeArray = [int(x.split(',')[1]) for x in timeArray]
    nSamples = timeArray[-1] - timeArray[0] + 1
    refTimeArray = np.linspace(timeArray[0],timeArray[-1], nSamples)
    timeArray = np.array(timeArray)
    missedTimes = np.setdiff1d(refTimeArray, timeArray)
    floatTimeArray = np.array(floatTimeArray)
    
    # Save missed timestamps in binary format
    missedTimesFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_missedTimes.mat'
    sio.savemat(missedTimesFile, {'val':missedTimes})
    
    # Save timestamps in binary format
    timesFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '_times.mat'
    sio.savemat(timesFile, {'val':floatTimeArray})
    
    # Write IR camera difference signal Header file
    camHeader = 'Begin-Time=' + str(timeArray[0]) + '\n' + 'End-Time=' + str(timeArray[-1]) + '\n' + 'Fs=1Hz' + '\n' + 'missedTimesFile=' + missedTimesFile
    camHeaderFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin/' + fileName + '.hea'
    with open(camHeaderFile, 'w') as fp:
        fp.write(camHeader)
        
##### Process Light-Color data
    # Read data in color file to colorArray
    splits = colorFile.split('/')
    fileName = splits[-1][:-4]
    with open(colorFile, 'r') as fp:
        colorArray = fp.readlines()
        
    colorArray = [x.strip() for x in colorArray]
    
    R = [float(x.split(',')[0]) for x in colorArray]
    G = [float(x.split(',')[1]) for x in colorArray]
    B = [float(x.split(',')[2]) for x in colorArray]
    C = [float(x.split(',')[3]) for x in colorArray]
    RGB565 = [float(x.split(',')[4]) for x in colorArray]
    RGB888 = [float(x.split(',')[5]) for x in colorArray]
    LUX = [float(x.split(',')[6]) for x in colorArray]
    CT = [float(x.split(',')[7]) for x in colorArray]
    INT = [float(x.split(',')[8]) for x in colorArray]
    
    data = dict()
    data['R'] = R
    data['G'] = G
    data['B'] = B
    data['C'] = C
    data['LUX'] = LUX
    data['CT'] = CT
    
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Save binarized color files
    colorMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/bin/' + fileName + '.mat'                    
    sio.savemat(colorMatFile, data)
    
    # Write Color Header file
    colorHeader = 'Begin-Time=' + str(timeArray[0]) + '\n' + 'End-Time=' + str(timeArray[-1]) + '\n' + 'Fs=1Hz' + '\n' + 'missedTimesFile=' + missedTimesFile + '\n' + 'Columns' + '\n' + 'R,G,B,C,RGB565,RGB888,LUX,CT,INT'
    colorHeaderFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/bin/' + fileName + '.hea'
    with open(colorHeaderFile, 'w') as fp:
        fp.write(colorHeader)   
    
##### Process temperature humidity data
    # Read data in color file to colorArray
    splits = thFile.split('/')
    fileName = splits[-1][:-4]
    with open(thFile, 'r') as fp:
        thArray = fp.readlines()
        
    thArray = [x.strip() for x in thArray]
    
    T = [float(x.split(',')[0]) for x in thArray]
    H = [float(x.split(',')[1]) for x in thArray]
    
    data = {}
    data['T'] = T
    data['H'] = H
    
    # Try and create directories if they don't exist for whatever reason
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/th')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    try:
        os.mkdir('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/th/bin')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    
    # Save binarized temperature humidity files
    thMatFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/bin/' + fileName + '.mat'                    
    sio.savemat(thMatFile, data)
    
    # Write Temperature Humidity Header file
    thHeader = 'Begin-Time=' + str(timeArray[0]) + '\n' + 'End-Time=' + str(timeArray[-1]) + '\n' + 'Fs=1Hz' + '\n' + 'missedTimesFile=' + missedTimesFile + '\n' + 'Columns' + '\n' + 'T,H'
    thHeaderFile = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/bin/' + fileName + '.hea'
    with open(thHeaderFile, 'w') as fp:
        fp.write(thHeader)  
