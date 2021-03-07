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

# Obtain Raspberry Pi ID
folder="$(sudo cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)"
dirName=$(date +'%m-%d-%Y')

# Make directories on EmoryBox if they don't exist
rclone mkdir EmoryBox:CFD/audioFeatures
rclone mkdir EmoryBox:CFD/audioFeatures/${folder}
rclone mkdir EmoryBox:CFD/audioFeatures/${folder}/features
rclone mkdir EmoryBox:CFD/audioFeatures/${folder}/features/${dirName}

# Transfer audio feature files to Emory AWS
#for fullFilePathName in /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/features/*; do
#fileName=${fullFilePathName##*/}
#curl --request POST -H "Content-Type: application/mat" --data-binary "@${fullFilePathName}" https://uniquePath.amazonaws.com/version#/apiGateway?path=${folder}/pir/${fileName}
#rm ${fullFilePathName}
#done

# rclone move audio feature files to Emory Box
rclone move /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/features EmoryBox:repoName/audioFeatures/${folder}/features/${dirName}


