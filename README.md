# OS_Edge_Compute_Data_Capture_RPi
*An Edge Computing and Ambient Data Capture System in Clinical and Home Environments.*

This repository contains scripts to simultaneously collect the following signals using off-body sensors.
1. Human movement signal using a passive infrared sensor.
2. Global and local difference signals (as a proxy for human movement) using a Raspberry Pi camera.
3. Mel spectorgram and MFCC features from audio recordings recorded using a Fifine USB microphone.
4. Geolocation of Bluetooth devices.
5. Ambient light logging using the TCS34725 color sensor.
6. Ambient temperature and humidity logging using the DHT22 sensor.

## Hardware Requirements
1. Raspberry Pi 3B or Raspberry Pi 4 (2G).
2. PIR sensor.
3. NoIR Rapsberry Pi Camera V2 with IR emitters.
4. TCS34725 Color sensor.
5. DHT22 sensor.
6. Fifine USB microphone.
7. A Bluetooth Beacon.

## Code Description
Please run `INSTALL.sh` script in a command line on a Raspberry Pi to install all the necessary software before using the scripts in this repository. The `gui.py` contains the wrapper codes needed to record human movement and ambient environement data (including illuminance, temperature and humidity). The `binarizeData.py` script can be used to convert data stored in text files to a binary format (specifically .mat). The `mseComputation.py` utilizes the compiled `mse` script to perform multi-scale entropy computations on various 1-D signals including the global difference signal. The `uploadToCloud.sh` is an example script that can be used to upload recorded data to a cloud database.The scripts `binarizeData.py`, `mseComputation.py` and `uploadToCloud.py` are all called from `gui.py` as subprocesses.

The folder `humanMovementDetectionToolbox` contains the python class and functions needed to capture human movement using the infrared Rapsberry Pi camera. The folder `ambientLightSensingToolbox` contains the python class and functions needed to capture light illuminance. The folder `temperatureAndHumiditySensingToolbox` contains the core script to capture ambient temperature and humidity values on a Raspberry Pi using the DHT22 sensor.

The folders `ambientSoundRecordingToolbox` and `ambientSoundAnalysisToolbox` contain the scripts needed to capture ambient audio, compute audio features and perform alarm note classification.

The folder `geolocationToolbox` contains all the code needed to capture and process Bluetooth signal strength data to determine the location of a Bluetooth beacon.

## Bill of Materials [As of Mar 22, 2021]
1. Raspberry Pi         : $35.00 [57mm X 87mm]
2. PIR sensor           :  $2.00 [24mm X 32mm X 25mm]
3. RPi camera           : $22.99 [25mm x 23mm x 9mm]
4. TCS34725             :  $9.35 [27mm X 20mm]
5. DHT22 sensor         :  $9.99 [15.3mm X 7.8mm X 25.3mm]
6. Microphone           : $35.99 [124mm X 66mm X 185mm]
7. Beacon               : $24.00 [56mm X 55mm X 15mm]
8. Coral USB Accelerator: $59.99 [65 mm x 30 mm]

Total                   = $199.31

## Citation

Please cite the following work when using this codebase.

*To be updated*

