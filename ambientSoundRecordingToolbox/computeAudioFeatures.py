#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar22nd, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

#import sounddevice as sd
#import soundfile as sf
import audioFeatureToolbox as aft
import scipy.io as sio
import numpy as np
import subprocess
import argparse
import librosa
import os

def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        'filename', nargs='?', metavar='FILENAME',
        help='audio file to store recording to')
    args = parser.parse_args()
    
    featureFilePathSplits = args.filename.split('/')
    featureFilePath = '/' + '/'.join(featureFilePathSplits[1:-2]) + '/features/'
    featureFileName = featureFilePathSplits[-1][:-4]
    featureFile = featureFilePath + featureFileName + '.mat'
    headerFile = featureFilePath + featureFileName + '.hea'
    
    # We used audio files with sr = 22050 If the sampling rate is different, please specify with the 'sr' option.
    y, sr = librosa.load(args.filename)
    blocksize = 30 #ms
    blocksize = round((blocksize / 1000) * sr) # samples
    # 
    win_length = next_power_of_2(blocksize)
    hop_length = round(win_length / 2)
    n_fft = win_length
    
    fp = open(headerFile, 'w+')
    fp.write('File-Name: ' + featureFileName + '\n')
    fp.write('Length of the signal = ' + str(len(y)) + '\n')
    fp.write('Sampling Frequency = ' + str(sr) + '\n')
    fp.write('Window length = ' + str(win_length) + '\n')
    fp.write('Hop Length = ' + str(hop_length) + '\n')
    fp.write('n_fft = ' + str(n_fft) + '\n')
    
    features = dict()
    fp.write('FEATURES'+ '\n')
    
    ## MFCC (20 coefficients)
    M = librosa.feature.mfcc(y=y, sr=sr, win_length = win_length, hop_length = hop_length, n_fft = n_fft) # Use n_fft = win_length
    features['mfcc'] = M
    fp.write('(1) MFCC: ' + str(M.shape) + '\n')
    fp.write('# of MFCC = ' + str(len(M)) + '\n')
    
    ## Energy in different frequency bands (10 coefficients)
    D = np.square(np.abs(librosa.core.stft(y, n_fft=win_length, hop_length=hop_length, win_length=win_length, window='hann'))) # Use n_fft = win_length
    
    # Create Energy Computation Windows to be used for mearging stft computations
    
    # Method 1: Manual-specification with Rectangular Windows
    # Specify the frequency bands for energy computation [beginFreqValue, endFreqValue)
    #energyComputationWindows = [(0,1), (1,501), (501, 2001), (2001, 5001), (5001, 11051)]
    # Use a loop to create mask vectors for each band
    #for ecWindow in energyComputationWindows:
    #    freqBandWeights = np.zeros(1+n_fft/2)
        # To be continued
        
    # Method 2: Use mel filterbank
    melfb = librosa.filters.mel(sr, n_fft, n_mels = 10) # Use same value for sr and n_fft as used in librosa.core.stft
    
    # Compute energies in different bands:
    E = np.matmul(melfb, D)
    features['energies'] = E
    fp.write('(2) Band Energy: ' + str(E.shape) + '\n')
    fp.write('# of Filterbanks = ' + str(len(E)) + '\n')
    ## Sample Entropy (1 value) -- Too slow on RPi3!! So, Skipping for now.
    """
    ii = 0
    sampleEntropy = []
    win_length = sr * 3; # 3 seconds
    hop_length = sr * 1; # 1 second
    flag = True
    while flag == True:
        if (ii + 1) * win_length < len(y):
            sig = y[ii * hop_length:(ii + 1) * win_length]
            ii += 1
        else:
            sig = y[ii * hop_length:]
            flag = False
        
        val = aft.ComputeMSE(signal = sig,
                             scales = 1,
                             a = 1,
                             mseScriptLoc = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/')
        sampleEntropy.append(val)
    
    features['sampleEntropy'] = sampleEntropy
    fp.write('(3) Sample Entropy' + str(sampleEntropy.shape) + '\n')
    fp.write('Window Length = ' + str(win_length) + '\n')
    fp.write('Hop Length = ' + str(hop_length) + '\n')
    """
    
    sio.savemat(featureFile, features)
    fp.close()
    subprocess.check_output(['xterm','-e','/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/backup.sh'])
    os.unlink(args.filename)
    
    
    
    
    
        
        
        
    