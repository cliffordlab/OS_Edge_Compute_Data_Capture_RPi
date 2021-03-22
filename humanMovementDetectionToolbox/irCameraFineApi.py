#!/usr/bin/python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 16th, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from time import time,sleep
import numpy as np
import cv2


class VideoTS:
    """
    Extracts multiple time-series from video and returns the most recent samples

    This class utilizes IR/NoIR camera to access video-frames and poll the current
    average red, green, blue and grey values of the video-frames. It comprises
    of multiple "return methods" to return the needed values. Sepcifically it has
    seperate methods to return the average red, green, blue and grey values.
    Attributes
    ----------
    VIDEO_BASE_FOLDER: string
        Folder location for saving video-frames temporarily.
    current_time_ms: int
        Return value of a Lambda function that returns the current time in POSIX format.
    camera: PiCamera object
        A PiCamera object that stores information corresponding to camera-capture settings.
    camera.reolution: int tuple
        Resolution setting of the camera.
    camera.framerate: int
        Framerate value of the video capture.
    rawCapture: PiRGBArray object
        A PiRGBArray object that can be used to access captured video frames.
    max_signal_length: int
        Maximum length of time series to store

    Example
    -------
    >>> vid_time_series = VideoTS()
    >>> vid_time_series.see(poll_time = 0.2)
    >>> print(vid_time_series.return_all_signals())
        [[131.31365966796875, 131.40003662109376, 131.26851806640624, 131.556884765625, 131.41928710937501],
        [130.29289550781249, 130.29340820312501, 130.21351318359376, 130.1702880859375, 130.23497314453124],
        [131.68802490234376, 131.56695556640625, 132.00104980468751, 131.72231445312499, 131.77058105468751],
        [130.78260498046876, 130.78345947265626, 130.75004882812499, 130.78642578124999, 130.78330078125001]]
    """

    def __init__(self,
                 VIDEO_BASE_FOLDER='/home/pi/PIR-interface/data/Videos/',
                 resolution = (320, 256),
                 framerate = 30,
                 max_signal_length = 100,
                 filterSize = 64):
        """Definitions"""
        self.VIDEO_BASE_FOLDER = VIDEO_BASE_FOLDER
        self.current_time_ms = lambda: int(round(time() * 1000))
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.max_signal_length = max_signal_length
        self.filterSize = filterSize
        self.sig_b = []
        self.sig_r = []
        self.sig_g = []
        self.sig_gs= []
        self.sigDiffB = []
        self.sigDiffG = []
        self.sigDiffR = []
        #self.sigDiffGS = []
        #self.sigDiffGSScaled = []
        self.GDS = []
        self.GDPC = []
        self.tempVar1 = []
        
        self.LDS = []
        self.LDPC = []
        rowLength = self.camera.resolution[0]
        colLength = self.camera.resolution[1]
        stepLength = self.filterSize
        nRows = len(range(0, rowLength - stepLength + 1, stepLength))
        nCols = len(range(0, colLength - stepLength + 1, stepLength))
        self.nSamples = nRows*nCols
        sleep(0.1)

    def get_video_filename(self):
        """Open a h264 file to write video frames and return the file name"""
        return self.VIDEO_BASE_FOLDER+str(self.clock)+'_video.h264'

    def _see(self, poll_time):
        """
        Thread for computing average red, green, blue and grey in video frames.
        Currently, BGR has been disabled - only Difference Frame Greyscale works. Scaled version has been added.
        Uses cv2 and numpy module to compute the average channel intensities

        Properties
        ----------
        Inherits **kwargs from `see` method
        """
        self.clock = self.current_time_ms()
        self.camera.start_recording(self.get_video_filename())
        cv2.startWindowThread()
        
        # New Code by Pradyumna on September 20th 2019 -- Need verification on Raspberry Pi
        frameOld = np.zeros([self.camera.resolution[1], self.camera.resolution[0]], dtype=np.uint8)
        ###################################################################################

        for frame in self.camera.capture_continuous(self.rawCapture,
                                                format="bgr",
                                                use_video_port=True):
            frame = frame.array
            framegs = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            self.tempVar1.append(sum(sum(framegs)))
            
            # New Code by Pradyumna on September 20th 2019 -- Verified on Raspberry Pi.
            frameDiffGS = np.array(np.absolute(np.array(framegs, dtype=int) - np.array(frameOld, dtype=int)), dtype=np.uint8)
            frameOld = framegs
            
            # (1)
            self.GDS.append(np.mean(np.mean(frameDiffGS)))
            # (2)
            M = self.camera.resolution[1]
            N = self.camera.resolution[0]
            scalingBaseline = (np.count_nonzero(frameDiffGS)*255)/(M*N)
            self.GDPC.append(scalingBaseline)
            if(len(self.GDPC)>self.max_signal_length):
                self.GDPC = self.GDPC[-self.max_signal_length:] 
            
            # (3) & (4)
            rowLength = self.camera.resolution[0]
            colLength = self.camera.resolution[1]
            stepLength = self.filterSize
            nRows = len(range(0, rowLength - stepLength + 1, stepLength))
            nCols = len(range(0, rowLength - stepLength + 1, stepLength))
            self.nSamples = nRows*nCols
            sig = []
            sigScaled = []
            pixelCount = []
            for col in range(0, colLength - stepLength + 1, stepLength):
                for row in range(0, rowLength - stepLength + 1, stepLength):
                    miniFrame = frameDiffGS[col:col + stepLength - 1, row:row + stepLength - 1]
                    #self.sigDiffGSFine[mm].append(np.mean(np.mean(miniFrame)))
                    sig.append(np.mean(np.mean(miniFrame)))
                    pixelCount.append((np.count_nonzero(miniFrame)*255)/(stepLength*stepLength))
                    
            self.LDS.append(sig)
            self.LDPC.append(pixelCount)
            #####################################################################################        

            self.rawCapture.truncate(0)
            sleep(poll_time)

    def see(self, poll_time=0.2):
        """
        Initiates _see daemon thread

        Parameters
        ----------
        poll_time: float
            Expects a float value that specifies the sleep time between two frames
        """
        self.see_thread = Thread(target=self._see,
                            kwargs={"poll_time": poll_time})
        self.see_thread.deamon = True
        self.see_thread.start()
 
    def return_pi_camera(self):
        """
        Returns the handle for pi camera
        
        Parameters
        ----------
        None
        """
        
        return self.camera
  
    def return_GDS(self, samples_to_return=5):
        """
        Returns a list of length samples_to_return with the latest samples of the
        time-series average grey channel of the difference signal. The latest sample 
        is the last sample in the list.

        Parameters
        ----------
        samples_to_return: int
            Expects an integer that specifies the number of latest samples to return
        """
        if(len(self.GDS)<samples_to_return):
            self.GDS = [0]*(samples_to_return-len(self.GDS))+self.GDS
        return self.GDS[-samples_to_return:]
 
    def return_GDPC(self, samples_to_return=5):
        """
        Returns a list of length samples_to_return with the latest samples of the pixel count
        time-series of the grey channel of the difference signal. The latest sample 
        is the last sample in the list.

        Parameters
        ----------
        samples_to_return: int
            Expects an integer that specifies the number of latest samples to return
        """
        if(len(self.GDPC)<samples_to_return):
            self.GDPC = [0]*(samples_to_return-len(self.GDPC))+self.GDPC
        return self.GDPC[-samples_to_return:]
 
    def return_LDS(self, samples_to_return=5):
        """
        Returns a list of length samples_to_return with the latest samples of the 
        time-series average grey channel (local) of the difference signal. The latest sample 
        is the last sample in the list.

        Parameters
        ----------
        samples_to_return: int
            Expects an integer that specifies the number of latest samples to return
        """
        if(len(self.LDS)<samples_to_return):
            self.LDS = [[0]*self.nSamples]*(samples_to_return-len(self.LDS))+self.LDS
        return self.LDS[-samples_to_return:]    
 
    def return_LDPC(self, samples_to_return=5):
        """
        Returns a list of length samples_to_return with the latest samples of the pixel count
        time-series of the grey channel (local) of the difference signal. The latest sample 
        is the last sample in the list.

        Parameters
        ----------
        samples_to_return: int
            Expects an integer that specifies the number of latest samples to return
        """
        if(len(self.LDPC)<samples_to_return):
            self.LDPC = [[0]*self.nSamples]*(samples_to_return-len(self.LDPC))+self.LDPC
        return self.LDPC[-samples_to_return:]
