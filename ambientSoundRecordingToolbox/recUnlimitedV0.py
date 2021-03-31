#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 22nd, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

"""Create a recording with arbitrary duration.

The soundfile module (https://PySoundFile.readthedocs.io/) has to be installed!

"""
import subprocess
import datetime
import argparse
import tempfile
import socket
import queue
import time
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def get_lock(process_name):
    # Lock the program run so that cronjob doesn't run it while a process is running
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print('I got the lock')
    except socket.error:
        print('lock exists')
        sys.exit()


get_lock('recUnlimitedV0')

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()

# Grab Raspberry Pi
cpuSerial = subprocess.check_output("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2", shell=True).decode('utf-8').strip()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

recordingLength = 300 #seconds
while True:
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        #args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',suffix='.wav', dir='')
        before = datetime.datetime.now()
        filename = time.strftime("%Y%m%d-%I-%M-%S-%p")
        args.filename = '/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ambientSoundRecordings/wavfiles/' + cpuSerial + '_' + filename + '.wav'

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
                    after = datetime.datetime.now()
                    delta = after - before
                    if (delta.seconds >= recordingLength):
                        subprocess.Popen(['xterm','-e','python3','/home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/computeAudioFeatures.py',args.filename])
                        break
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
