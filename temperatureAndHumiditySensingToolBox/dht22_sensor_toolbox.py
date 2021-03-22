#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Jacob Zelko (alias TheCedarPrince)
Modified: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 16th, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

from datetime import datetime
from threading import Thread
from time import sleep

from Adafruit_DHT import read_retry, DHT22

class SensorToolbox:

    """
    A superclass that provides subclasses to interface with hardware sensors.
    SensorTool enables one to interface with temperature and humidity
    sensors currently using the Adafruit_DHT module. More sensors and modules
    can be added by creating additional subclasses for each sensor in this
    superclass.
    """
    class DHT22Tool:

        """
        Samples temperature in current environment using the Adafruit DHT22.
        Class provides an interface to the DHT22 with associated methods to poll
        the current environment's temperature and humidity. By default,
        temperature is returned in celsius and humidity is given as a percent.
        Attributes
        ----------
        pin: int
            Expects an integer designating data output pin.
        sensor : DHT22 Object
            Expects a DHT22 Object designating the sensor used.
        Example
        -------
        >>> dht22_sensor = DHT22Tool(pin = 4)
        >>> dht22_sensor.detect(poll_time = 2)
        >>> print(dht22_sensor.return_temperature())
            23.8
        >>> print(dht22_sensor.return_humidity())
            64.0
        """

        def __init__(self, pin):
            """Instantiates sensor to interface with and pin for data output"""
            self.sensor = DHT22
            self.pin = pin

        def _detect(self, celsius, fahrenheit, poll_time):
            """
            Thread for detecting temperature.
            Uses Adafruit_DHT module to detect temperature of environment.
            Properties
            ----------
            Inherits **kwargs from detect method.
            """
            while True:
                self.humidity, self.temperature = read_retry(self.sensor,
                                                             self.pin)

                if celsius:
                    pass
                else:
                    self.temperature = self.temperature * 9/5.0 + 32
                sleep(poll_time)

        def detect(self, celsius=True, fahrenheit=False, poll_time=5):
            """
            Initiates _detect daemon thread
            Parameters
            ----------
            celsius : boolean
                Accepts a boolean expression to return temperatue in celsius
            fahrenheit : boolean
                Accepts a boolean expression to return temperature in fahrenheit
            poll_time : int
                Accepts an integer denoting how often to poll environment in
                seconds
            """
            detect_thread = Thread(target=self._detect,
                                 kwargs={"celsius": celsius,
                                         "fahrenheit": fahrenheit,
                                         "poll_time": poll_time})
            detect_thread.daemon = True
            detect_thread.start()

        def return_temperature(self):
            """Returns a string denoting temperature"""
            return str(self.temperature)

        def return_humidity(self):
            """Returns a string denoting current humidity"""
            return str(self.humidity)
