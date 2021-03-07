#!/bin/bash
: <<'END'
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 5th, 2021
Copyright [2021] [Clifford Lab]
LICENSE:    
This software is offered freely and without warranty under 
the GNU GPL-3.0 public license. See license file for
more information
END

# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Run rclone config
rclone config

# Install ALSA-mixer
sudo apt-get install -y libasound-dev

# Install alsa-utils
sudo apt-get install -y alsa-utils

# Install MP3 tools
sudo apt-get install -y mpg321

# Install WAV to MP3 conversion tool
sudo apt-get install -y lame

# Load the sound-driver
sudo modprobe snd-bcm2835

# Switch Audio output to 3.5mm Jack
amixer cset numid=3 1 # Use `numid=3 2` for HDMI out

# Install requirements
sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev

# Install sounddevice
python3 -m pip install sounddevice --user

# Matplotlib
sudo apt-get install -y python3-matplotlib

# Scipy
sudo apt-get install -y python3-scipy

# Install soundfile
sudo apt-get install libsndfile1
sudo pip3 install soundfile

# Install libbrosa
sudo apt -y install libblas-dev llvm
sudo pip3 install librosa
sudo pip3 uninstall numba
sudo pip3 install numba==0.48.0
sudo pip3 install colorama --upgrade
# You may have to run this if it upgrades to a too new a version
#sudo pip3 uninstall colorama==0.3.7
#sudo pip3 uninstall colorama==0.4.3

# Install xterm
sudo apt-get install -y xterm 

# Make a new directory
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data

sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/wavfiles
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/wavfiles

sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/features
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/data/features

# Save git username and password locally to run git pull hassle-free
git config credential.helper store
while true; do git pull && break || sleep 2; done

# Setup crontabs
crontab -r
(crontab -l 2>/dev/null; crontab -l) | grep -q '*/5 * * * * /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/crony.sh' && echo 'Crontab already set' || (crontab -l 2>/dev/null; echo "*/5 * * * * /home/pi/OS_Edge_Compute_Data_Capture_RPi/ambientSoundRecordingToolbox/crony.sh") | crontab -


