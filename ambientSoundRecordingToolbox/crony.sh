#!/bin/sh
: <<'END'
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 5th, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
END
# This script is run by a cronjub that runs every minute.
export XAUTHORITY=/home/pi/.Xauthority
export DISPLAY=:0
python3 /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/recUnlimitedV0.py