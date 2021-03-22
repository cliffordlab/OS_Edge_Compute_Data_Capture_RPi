#!/bin/sh
: <<'END'
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 21st, 2021
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
END

# Turn on the WiFi and confirm by pinging google.com
sudo ifconfig wlan0 up
wget --spider -4 https://google.com
while [ "$?" != 0 ]; do  sleep 5; wget --spider -4 https://google.com; done

sleep 5

# Obtain Raspberry Pi ID
cpuSerial="$(sudo cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)"

# Assign the correct value to the variable remoteName
remoteName=""

# Path to the directory where the data shall be stored in the cloud should be specified below
pathToData=""

# Make directories on ${remoteName} if they don't exist
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/pir
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/pir/bin
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/pir/mse
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/ir
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/ir/bin
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/ir/mse
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/color
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/color/bin
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/color/mse
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/temperatureAndHumidity
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/temperatureAndHumidity/bin
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/temperatureAndHumidity/mse
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/ambientSoundRecordings
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/ambientSoundRecordings/features
rclone mkdir ${remoteName}:${pathToData}/${cpuSerial}/geolocationToolbox

# rsync all binary files to ${remoteName}
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/pir/bin ${remoteName}:${pathToData}/${cpuSerial}/pir/bin
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/pir/mse ${remoteName}:${pathToData}/${cpuSerial}/pir/mse
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/ir/bin ${remoteName}:${pathToData}/${cpuSerial}/ir/bin
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/ir/mse ${remoteName}:${pathToData}/${cpuSerial}/ir/mse
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/color/bin ${remoteName}:${pathToData}/${cpuSerial}/color/bin
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/color/mse ${remoteName}:${pathToData}/${cpuSerial}/color/mse
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/temperatureAndHumidity/bin ${remoteName}:${pathToData}/${cpuSerial}/temperatureAndHumidity/bin
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/temperatureAndHumidity/mse ${remoteName}:${pathToData}/${cpuSerial}/temperatureAndHumidity/mse
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/ambientSoundRecordings/features ${remoteName}:${pathToData}/${cpuSerial}/ambientSoundRecordings/features
rclone move /home/pi/OS_Edge_Compute_Data_Capture/data/geolocationToolbox ${remoteName}:${pathToData}/${cpuSerial}/geolocationToolbox

# Delete all video-files that were recorded
rm -rf /home/pi/OS_Edge_Compute_Data_Capture/data/Videos/*

# Run the upload_complete.py GUI to display that upload is indeed complete
sudo python3 /home/pi/OS_Edge_Compute_Data_Capture/codes/upload_complete.py
