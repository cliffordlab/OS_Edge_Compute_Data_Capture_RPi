#!/bin/bash
: <<'END'
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 22nd, 2021
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

# Create new directories
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/bin
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/mse
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/bin
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/mse
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/Videos
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/bin
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/mse
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/bin
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/mse
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/Images
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ambientSoundRecordings
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ambientSoundRecordings/wavfiles
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ambientSoundRecordings/features
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/geolocationToolbox
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/geolocationToolbox/data
sudo mkdir /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/geolocationToolbox/dataUpload

# Provide '777' permission to the created data directories (A redundant step to make sure data write never fails. A better solution is indeed possible.)
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ambientSoundRecordings/*
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/geolocationToolbox/*

sudo apt-get update

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

# Install OpenCV and its requirements
pip3 install opencv-python
sudo apt install -y libqt4-test
sudo apt-get install -y libatlas-base-dev
sudo apt install -y libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase12 libopenexr22 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libqtgui4 libqtcore4
sudo apt install -y libjasper-runtime

# Install gedit 
sudo apt-get install -y gedit

# Install xterm for running subprocess threads
sudo apt-get install -y xterm

# Install matplotlib for data visualizations in python
sudo apt-get install -y python3-matplotlib

# Install scipy for binarizing the data
sudo apt-get install -y python3-scipy

# Install Adafruit_DHT for temperature and humidity
pip3 install Adafruit_DHT

# Save git username and password locally to run git pull hassle-free
git config credential.helper store
while true; do git pull && break || sleep 2; done

# geolocationToolbox related installations
sudo apt-get install libglib2.0-dev ntp ntpdate
pip3 install bluepy
pip3 install pandas
blue_path=$(pip3 show bluepy | grep Location: | awk -F " " '{path=$2"/bluepy/bluepy-helper"; print path}')
sudo setcap 'cap_net_raw,cap_net_admin+eip' $blue_path

# Setup auto_time_tracker
echo "3">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "0">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "0">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "PM">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "9">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "0">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "0">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
echo "AM">>/home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker
sudo chmod 777 /home/pi/OS_Edge_Compute_Data_Capture_RPi/autorec_time_tracker