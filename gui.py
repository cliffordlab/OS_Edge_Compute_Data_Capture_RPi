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

from temperatureAndHumiditySensingToolbox.dht22_sensor_toolbox import SensorToolbox
from ambientLightSensingToolbox.TCS34725 import TCS34725
from tkinter import Tk, Label, Button, messagebox
from matplotlib.widgets import Slider
from datetime import datetime

import humanMovementDetectionToolbox.irCameraFineApi as camApi
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np

import subprocess
import picamera
import socket
import time
import glob
import pdb
import sys
import os

def get_lock(process_name):
    # Lock the program run so that cronjob doesn't run it while a process is running
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print('I got the lock')
    except socket.error:
        print('lock exists')
        sys.exit()

get_lock('gui')

# Declare global variables
global last_block_time_in_ms
global window_size_in_ms
global record_status
global window_count
global auto_status
global pltxrange
global pltyrange
global cpuSerial
global filename
global ts_in_ms
global PIR_PIN
global TH_PIN
global s_time
global count
global f
global a

# Color Sensor variables
global light

# TH Sensor variables
global dht22_sensor

# Grab Raspberry Pi
cpuSerial = subprocess.check_output("cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2", shell=True).decode('utf-8').strip()

# Initialize declared global variables
pltyrange = 100
pltxrange = 10
filename = ""
a = 0
count = 0
window_size_in_ms = 600
window_count = []
ts_in_ms = int(round(time.time()))
last_block_time_in_ms = ts_in_ms
s_time = int(0.5*1000)
record_status = 0
auto_status = 0
PIR_PIN = 21
TH_PIN = 23

# Remove any Video files that are currently sitting in secondary memory
subprocess.Popen(['xterm','-e','rm -rf /home/pi/OS_Edge_Compute_Data_Capture_RPi/data/Videos/*'])
ir_sig = camApi.VideoTS()
ir_sig.see()

# Initialize Light Sensor

light=TCS34725(0X29, debug=False)
if(light.TCS34725_init() == 1):
    print("TCS34725 initialization error!!")
else:
    print("TCS34725 initialization success!!")

# Initialize TH sensor
dht22_sensor = SensorToolbox.DHT22Tool(pin = TH_PIN)
dht22_sensor.detect(poll_time = 1)

# The GUI class
class interface:
    def __init__(self, master):
        """ Initialization """
        subprocess.Popen(['sudo','ifconfig','wlan0','down'])
        self.master = master
        master.title("Motion Sensor")

        self.label1 = Label(master, text="Interface",bg = "yellow")
        self.label1.grid(row = 0, columnspan = 2)   
         
        self.Binarize_button = Button(master, text="Manual Upload Now", command=self.Backup)
        self.Binarize_button.grid(row = 1, column = 0, ipadx = 36, ipady = 19)

        self.Record_button = Button(master, text="Start/Stop Recording\nIDLE", command=self.Record)
        self.Record_button.grid(row = 1, column = 1, ipadx = 43, ipady = 11)

        self.close_button = Button(master, text="Auto-Recording Menu", command=self.autorecmenu)
        self.close_button.grid(row = 2, column = 0, ipadx = 30, ipady = 19)
    
        self.close_button = Button(master, text="Graph Data", command=self.graph_data)
        self.close_button.grid(row = 2, column = 1,ipadx = 72,ipady=19)
    
        self.close_button = Button(master, text="View raw Data", command=self.view_data)
        self.close_button.grid(row = 3, column = 0,ipadx = 53,ipady=19)

        self.close_button = Button(master, text="Close", command=self.clean_exit)
        self.close_button.grid(row = 3, column = 1,ipadx = 90,ipady=19)
        
        self.label3 = Label(text="Record-Mode: Manual")
        self.label3.grid(row = 4, columnspan = 2)
        global window_count
        window_count = []
        self.auto_record()   
        
        self.label2 = Label(text="")
        self.label2.grid(row = 5 , columnspan = 2)
        self.update_clock()

    def Backup(self):
        """ Binarize, compute features and backup data to AWS and Box """
        global filename
        global cpuSerial
        global ir_sig

        self.master.update_idletasks()
        # Call scripts to save *.mat files for PIR / Camera data
        subprocess.check_output(['xterm','-e','python3', '/home/pi/OS_Edge_Compute_DataCapture_RPi/binarizeData.py',
                '--cpuSerial', cpuSerial, '--dateTime', filename]) 
        
        # Call scripts to compute MSE from PIR / Camera data.
        # This script can be further modified to include other feature extraction methods. MSE computation is an example.
        subprocess.check_output(['xterm','-e','python3', '/home/pi/OS_Edge_Compute_DataCapture_RPi/mseComputation.py', 
                '--cpuSerial', cpuSerial, '--dateTime', filename])
        
        # Call scripts to upload data to cloud         
        subprocess.check_output(['xterm','-e','/home/pi/OS_Edge_Compute_DataCapture_RPi/codes/uploadToCloud.sh'])
        
        # Save the posix-timestamp corresponding to when the Backup occurs.
        # Uncomment the following 3 lines to enable upload tracking.
        #f = open("/home/pi/OS_Edge_Compute_DataCapture_RPi/lastBackupTimestamp.txt", "w")
        #f.write(str(round(time.time())))
        #f.close()
        
        #GPIO.cleanup()
        time.sleep(1)

    def Record(self):
        """ An older method of recording only PIR data manually. Not currently in use. See auto_record(self) for the most recent method.  """
        global auto_status
        global record_status
        global filename
        global window_count
        global PIR_PIN
        global cpuSerial
        
        if auto_status == 0:
            if record_status == 0:
                record_status = 1
                subprocess.Popen(['sudo','ifconfig','wlan0','down'])
                window_count = []
                self.master.update_idletasks()
                self.Record_button.configure(text="Start/Stop Recording\nRECORDING...")
                filename = time.strftime("%Y%m%d-%I-%M-%S-%p")
                f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/timestamps_' + cpuSerial + '_' + filename+'.txt','a')
                f.close()
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(PIR_PIN, GPIO.IN)
                self.PIR()
            else:
                record_status = 0
                #GPIO.cleanup()
                self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                self.Backup()
                self.Record_button.configure(text="Start/Stop Recording\nIDLE")
                filename = ""
        else:
            self.Record_button.configure(text="Start/Stop Recording\nAuto Recorder prevented this action")
            self.master.update()

    def autorecmenu(self):
        """ Run auto-record-menu GUI to set auto-recording times """
        subprocess.Popen(['python3', '/home/pi/PIR-interface/codes/auto_record_menu.py'])
    
    # An example function of what can be done. There is much room for improvement.
    def graph_data(self):
        """ Plot data being captured in real time or the most recent data"""
        global filename
        global pltxrange
        global pltyrange
        
        if filename == "":
            files = glob.glob("/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/*pirTenMinuteCounter.txt")
            temp = files[:]
            for ii in range(len(temp)):
                temp[ii] = temp[ii][-44:-24]
                temp[ii] = datetime.strptime(temp[ii],'%Y%m%d-%I-%M-%S-%p')
            
            idx = sorted(range(len(temp)), key=lambda k: temp[k]);
            gfile=files[idx[-1]]
            fd = open(gfile,'r')    
            d = np.loadtxt(fd, delimiter=',', dtype={'names': ('start_time','end_time','count'), 'formats': ('int', 'int', 'int', )})
            fd.close()
            data = d['count']
            plttitle = gfile[28:]
        else:
            data = window_count
            plttitle = 'ten_min_counter_'+filename+'.txt'
            
        # PLOT
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)
        l, = plt.plot(data,'ro')
        ax.set_title(plttitle)
        plt.axis([0, pltxrange, 0 , pltyrange]) 
        axcolor = 'lightgoldenrodyellow'
        axpos = plt.axes([0.2, 0.1, 0.65, 0.03], axisbg=axcolor)
        
        spos = Slider(axpos, 'Pos', 0.1, 90.0)

        def update(val):
            pos = spos.val
            ax.axis([pos,pos+pltxrange,0,pltyrange])
            
        spos.on_changed(update)

        plt.show()
        self.master.quit()
        
    def view_data(self):
        """ View PIR sensor data on a leafpad """
        files = glob.glob("/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/timestamps_*.txt")
        temp = files[:]
        for ii in range(len(temp)):
            temp[ii] = temp[ii][-24:-4]
            temp[ii] = datetime.strptime(temp[ii],'%Y%m%d-%I-%M-%S-%p')
            
        idx = sorted(range(len(temp)), key=lambda k: temp[k]);
        gfile=files[idx[-1]]
        subprocess.Popen(['leafpad',gfile])
        self.master.update()
                    
    def PIR(self):
        """ Do data capturing for manual data record via the Record function """
        global record_status
        global PIR_PIN
        if record_status == 1:
            global f
            global g
            global a
            global count
            global window_size_in_ms
            global window_count
            global ts_in_ms
            global last_block_time_in_ms
            global s_time
            global filename
            global cpuSerial
            
            print("Seek and Destroy")
            ts_in_ms = int(round(time.time()))
            if GPIO.input(PIR_PIN):
                ts_in_ms = int(round(time.time()))
                print("Motion Detected!")
                f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTimestamps.txt','a')
                f.write(str(ts_in_ms) + ' \n')
                f.close()
                a = a+1
                count=count+1

            if (ts_in_ms - last_block_time_in_ms >= window_size_in_ms):
                window_count.append(count)
                g = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTenMinuteCounter.txt','a')
                g.write(str(last_block_time_in_ms)+','+str(ts_in_ms)+','+str(window_count[-1]) + ' \n')
                g.close()                
                count = 0
                last_block_time_in_ms= ts_in_ms
            
            self.master.after(s_time, self.PIR)    
                        
    def auto_record(self):
        """ Auto recorder for recording PIR signal and IR camera data """
        
        global auto_status
        global record_status
        global f
        global g
        global a
        global count
        global window_size_in_ms
        global window_count
        global ts_in_ms
        global last_block_time_in_ms
        global s_time
        global filename
        global PIR_PIN
        global TH_PIN
        global ir_sig
        global light
        global dht22_sensor
        
        # We are computing cpuSerial in the beginning. No need to recompute
        # cpuSerial = getSerial()
        
        # Read autorec_time_tracker to start, continue or stop recording
        with open('/home/pi/PIR-interface/codes/autorec_time_tracker','r') as f:
            BHr = f.readline()[:-1]
            BMin = f.readline()[:-1]
            BSec = f.readline()[:-1]
            BAP = f.readline()[:-1]
            EHr = f.readline()[:-1]
            EMin = f.readline()[:-1]
            ESec = f.readline()[:-1]
            EAP = f.readline()[:-1]
  
        Btime = BHr+':'+BMin+':'+BSec+':'+BAP
        Btime = time.strptime(Btime,"%I:%M:%S:%p")
        Etime = EHr+':'+EMin+':'+ESec+':'+EAP
        Etime = time.strptime(Etime,"%I:%M:%S:%p")
        curtime = time.strptime(time.strftime("%I:%M:%S:%p"),"%I:%M:%S:%p")
        
        # Start, continue or stop recording
        if(Etime>Btime):
            if(curtime>=Btime and curtime<=Etime and auto_status == 0):
                if(record_status==1):
                    record_status = 0
                    #GPIO.cleanup()
                    self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                    self.Backup()
                    self.Record_button.configure(text="Start/Stop Recording\nIDLE")

                subprocess.Popen(['sudo','ifconfig','wlan0','down'])   
                auto_status = 1
                self.Record_button.configure(text="Start/Stop Recording\nRECORDING...")
                self.label3.configure(text="Record-Mode: Auto")
                filename = time.strftime("%Y%m%d-%I-%M-%S-%p")
                f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTimestamps.txt','a')
                f.close()
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(PIR_PIN, GPIO.IN)

            if(curtime>=Etime and auto_status == 1):
                auto_status = 0
                print(" Quit")
                #GPIO.cleanup()
                self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                self.Backup()
                self.Record_button.configure(text="Start/Stop Recording\nIDLE")
                self.label3.configure(text="Record-Mode: Manual")
                filename = ""
                
        else:
            if(curtime>=Btime):
                if(auto_status==0): 
                    if(record_status==1):
                        record_status = 0
                        #GPIO.cleanup()
                        self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                        self.Backup()
                        self.Record_button.configure(text="Start/Stop Recording\nIDLE")

                    subprocess.Popen(['sudo','ifconfig','wlan0','down'])
                    auto_status = 1
                    self.Record_button.configure(text="Start/Stop Recording\nRECORDING...")
                    filename = time.strftime("%Y%m%d-%I-%M-%S-%p")
                    f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTimestamps.txt','a')
                    f.close()
                    self.label3.configure(text="Record-Mode: Auto")
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(PIR_PIN, GPIO.IN)                                        
                    #ir_sig.see()
            else:
                if(auto_status==1 and curtime>=Etime):
                    auto_status = 0
                    print(" Quit")
                    #GPIO.cleanup()
                    self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                    self.Backup()
                    self.Record_button.configure(text="Start/Stop Recording\nIDLE") 
                    self.label3.configure(text="Record-Mode: Manual") 
                    filename = ""
                elif(auto_status==0 and curtime<=Etime):
                    if(record_status==1):
                        record_status = 0
                        #GPIO.cleanup()
                        self.Record_button.configure(text="Start/Stop Recording\nBACKING UP")
                        self.Backup()
                        self.Record_button.configure(text="Start/Stop Recording\nIDLE")

                    subprocess.Popen(['sudo','ifconfig','wlan0','down'])
                    auto_status = 1
                    self.Record_button.configure(text="Start/Stop Recording\nRECORDING...")
                    filename = time.strftime("%Y%m%d-%I-%M-%S-%p")
                    f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTimestamps.txt','a')
                    f.close()
                    self.label3.configure(text="Record-Mode: Auto")
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(PIR_PIN, GPIO.IN)
                    #ir_sig.see()
                    
        # Start or continue recording if the condition is satisfied
        if auto_status==1:
            
            GDS_to_save = ir_sig.return_GDS(1)
            GDPC_to_save = ir_sig.return_GDPC(1)
            
            # Fine Signal
            LDS_to_save = ir_sig.return_LDS(1)
            LDPC_to_save = ir_sig.return_LDPC(1)            
            floatTimes = time.time()
            times = int(round(time.time()))
            
            # Write captured signal values to text files
            
            with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/'+ cpuSerial + '_' +filename+'_GlobalSignals.txt','a+') as f:
                for ii in range(len(GDS_to_save)):
                    f.write("%s,%s\n" % (GDS_to_save[ii],
                                         GDPC_to_save[ii]))
            
            with open ('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/'+ cpuSerial + '_' +filename+'_times.txt','a+') as f:
                f.write(str(floatTimes) + ',' + str(times) + ' \n')

            with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/'+ cpuSerial + '_' +filename+'_LDS.txt','a+') as f:
                for ii in range(len(LDS_to_save)):
                    f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" 
                                      % (LDS_to_save[ii][0],LDS_to_save[ii][1],LDS_to_save[ii][2],LDS_to_save[ii][3],LDS_to_save[ii][4],
                                         LDS_to_save[ii][5],LDS_to_save[ii][6],LDS_to_save[ii][7],LDS_to_save[ii][8],LDS_to_save[ii][9],
                                         LDS_to_save[ii][10],LDS_to_save[ii][11],LDS_to_save[ii][12],LDS_to_save[ii][13],LDS_to_save[ii][14],
                                         LDS_to_save[ii][15],LDS_to_save[ii][16],LDS_to_save[ii][17],LDS_to_save[ii][18],LDS_to_save[ii][19]))            
            with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/ir/'+ cpuSerial + '_' +filename+'_LDPC.txt','a+') as f:
                for ii in range(len(LDPC_to_save)):
                    f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" 
                                      % (LDPC_to_save[ii][0],LDPC_to_save[ii][1],LDPC_to_save[ii][2],LDPC_to_save[ii][3],LDPC_to_save[ii][4],
                                         LDPC_to_save[ii][5],LDPC_to_save[ii][6],LDPC_to_save[ii][7],LDPC_to_save[ii][8],LDPC_to_save[ii][9],
                                         LDPC_to_save[ii][10],LDPC_to_save[ii][11],LDPC_to_save[ii][12],LDPC_to_save[ii][13],LDPC_to_save[ii][14],
                                         LDPC_to_save[ii][15],LDPC_to_save[ii][16],LDPC_to_save[ii][17],LDPC_to_save[ii][18],LDPC_to_save[ii][19]))
            # Record PIR sensor signal
            print("Seek and Destroy")
            ts_in_ms = int(round(time.time()))
            if GPIO.input(PIR_PIN):
                ts_in_ms = int(round(time.time()))
                print("Motion Detected!")
                f = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTimestamps.txt','a')
                f.write(str(ts_in_ms) + ' \n')
                f.close()
                a = a+1
                count=count+1

            # Update ten_min_counter file
            if(ts_in_ms - last_block_time_in_ms >= window_size_in_ms):
                window_count.append(count)
                g = open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/pir/'+ cpuSerial + '_' +filename+'_pirTenMinuteCounter.txt','a')
                g.write(str(last_block_time_in_ms)+','+str(ts_in_ms)+','+str(window_count[-1]) + ' \n')
                g.close()                
                count = 0
                last_block_time_in_ms= ts_in_ms
                
            # Record Light Sensor Data
            R = -1;G = -1;B = -1;C = -1;RGB565 = -1;RGB888 = -1;LUX = -1;CT = -1;INT = -1
            try:
                light.Get_RGBData()
                light.GetRGB888()
                light.GetRGB565()
                
                R = light.RGB888_R
                G = light.RGB888_G
                B = light.RGB888_B
                C = light.C
                RGB565 = light.RG565
                RGB888 = light.RGB888
                LUX = light.Get_Lux()
                # A modified wa of capturing ambient light. Needs more research.
                LUX_noIRCompensation = light.Get_Lux_noIRCompensation()
                CT = light.Get_ColorTemp()
                INT = light.GetLux_Interrupt(0xff00, 0x00ff)
            except:
                pass
            
            with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/color/'+ cpuSerial + '_' + filename + '_color.txt','a+') as f:
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (R,G,B,C,RGB565,RGB888,LUX,CT,INT))            
            
            # Record Temperature and Humidity
            
            temp = round(float(dht22_sensor.return_temperature()) * 10) / 10
            hum = round(float(dht22_sensor.return_humidity()) * 10) / 10
            
            with open('/home/pi/OS_Edge_Compute_Data_Capture_RPi/data/temperatureAndHumidity/'+ cpuSerial + '_' + filename + '_th.txt','a+') as f:
                f.write("%s,%s\n" % (temp, hum))            
            
        self.master.after(s_time, self.auto_record)      
    
    def clean_exit(self):
        """ Clean exit """
        global record_status
        global auto_status
        global ir_sig
        #GPIO.cleanup()
        if messagebox.askyesno("Close", "Click Yes to Close the GUI"):
            if (record_status == 1 or auto_status == 1):
                self.Backup()
            
            cam = ir_sig.return_pi_camera()
            cam.close()
            self.master.quit()
             
    def update_clock(self):
        """ Update clock """
        global cpuSerial
        now = 'UTC = '+str(int(time.time()))+' GMT = '+str(datetime.utcnow())[0:-7]+' PiID = '+cpuSerial
        self.label2.configure(text=now) 
        self.master.after(1000, self.update_clock)        

""" Display GUI """
root = Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
my_gui = interface(root)
root.mainloop()
