#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Jacob Zelko (alias TheCedarPrince)
Last Modified: Mar 5th, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""

import os
from datetime import datetime
from dateutil.tz import gettz
from subprocess import call, PIPE, Popen, run
from threading import Thread
from time import sleep, time, mktime

from bluepy.btle import Scanner
from pandas import DataFrame


class SystemToolbox:

    class SystemTool:

        """
        Provides utilities to interact with the underlying system.

        Creates an object that is given temporary root access to execute
        very specific methods to interact with the underlying system
        architecture.

        """

        def mount(self, path=None):
            """
            Mounts a repository using the underlying system tools.

            Paramaters
            ----------
            path : string
                Path of repository to mount.

            Example
            -------
            ...
            ...
            >>> SystemTool.mount("/home/Downloads")
            ...
            ...
            """
            if os.path.exists(path):
                mount_result = run(['mount', path])
                if mount_result.returncode != 0:
                    print("Mounting failed")
                    return mount_result.returncode
                else:
                    return mount_result.returncode
            else:
                print("Invalid filepath to mount.")
                raise SystemExit()

        def bluetooth_module(self):
            """Returns the name of the first bluetooth module on system

            Example
            -------
            ...
            >>> system_tool = SystemTool()
            >>> print(system_tool.bluetooth_module())
            hci0
            """
            mod_cmd_1 = Popen((["hciconfig", "name"]), stdout=PIPE)
            mod_cmd_2 = Popen((["sed", "-n", "1p"]), stdout=PIPE,
                              stdin=mod_cmd_1.stdout)
            mod_cmd_3 = Popen((["cut", "-d:", "-f1"]), stdout=PIPE,
                              stdin=mod_cmd_2.stdout)
            return ((mod_cmd_3.communicate()[0]).decode("UTF-8")).strip()

    class BluetoothTool:

        """
        Scans the surrounding environment for bluetooth low energy devices.

        Class that scans the surrounding environment for bluetooth low energy
        devices. Transparent imports of the Scanner class from the bluepy.btle
        module. This class allows for some tweaking such as setting scanning
        times, the ability to print out a file with the results of the scan to
        somewhere on one's file system, and time stamping capabilities.

        Instantiating this class also instantiates the Scanner object.

        Attributes
        ----------
        device_dataframe: pandas.DataFrame Object
            Transparent instantiation of pandas.DataFrame object.
        btle_scanner: bluepy.btle.Scanner
            Transparent instantiation of bluepy.btle.Scanner object.
        bluetooth_module : str
            A string representing the name of the local machine's bluetooth
            hardware set.

        """

        def __init__(self, bluetooth_module):
            """Inits with bluepy.btle.Scanner."""
            self.device_dataframe = DataFrame({"time" : [], "addr": [],
                                               "rssi": []})
            self.btle_scanner = Scanner()
            self.bluetooth_module = bluetooth_module

        def _bluetooth_scan(self, scan_time, to_file, timestamp):
            """
            Performs a scan for bluetooth low energy devices.

            Parameters
            ----------
            scan_time : int
                The setting for how many seconds the method is to scan.
            to_file : boolean, str, optional
                Determines if a log file with scan results is generated. Accepts
                string representing absolute path for where log file is stored.
            output : boolean, optional
                Option to display scan output to CLI.
            timestamp : str
                Creates a timestamp to display next to bluetooth low energy
                devices detected.

            Returns
            -------
            self.device_dataframe : pandas.DataFrame
                Returns an empty pandas.DataFrame with labels preserved if no
                device is detected. Else, the method will return a dataframe
                containing the devices detected with associated MAC addresses,
                RSSI values, and timestamps.

            Examples
            --------
            >>> tool = BluetoothTool()
            >>> tool.bluetooth_scan(output = True)
            00:00:00,6A:30:A5:CF:F4:22,-97
            00:00:00,C8:69:CD:E7:37:81,-76
            00:00:00,5C:62:89:08:28:71,-67

            >>> tool.bluetooth_scan(output = True)
            No devices detected

            >>> devices = tool.bluetooth_scan(output = True)
            00:00:00,6A:30:A5:CF:F4:22,-97
            >>> print(devices.addr)
            6A:30:A5:CF:F4:22

            """


            while True:

                zoned_time = datetime.fromtimestamp(time(),
                                                    gettz("US/Eastern"))
                timestamp = int(mktime(zoned_time.timetuple()))
                timestamp = datetime.utcfromtimestamp(timestamp).strftime(
                                                                 "%Y-%m-%d %H:%M:%S")

                devices = self.btle_scanner.scan(scan_time)
                self.device_dataframe = self.device_dataframe[0:0]

                if to_file:
                    if len(devices) == 0:
                        print("No devices detected.")
                        print("")
                    else:
                        with open(to_file, 'a') as datafile:
                            for device in devices:
                                datafile.write("{},{},{}\n".format(
                                    timestamp, (device.addr).upper(),
                                    device.rssi))
                                print("{},{},{}".format(timestamp,
                                                        (device.addr).upper(),
                                                        device.rssi))
                            print("")
                if len(devices) == 0:
                    return(self.device_dataframe)
                else:
                    for device in devices:
                        self.device_dataframe = self.device_dataframe.append(
                                                    {"time" : timestamp,
                                                     "addr" : (device.addr).upper(),
                                                     "rssi" : device.rssi},
                                                    ignore_index=True)


        def bluetooth_scan(self, scan_time=1,
                           to_file=False, timestamp="00:00:00"):
            """
            Performs a scan for bluetooth low energy devices.

            Parameters
            ----------
            scan_time : int
                The setting for how many seconds the method is to scan.
            to_file : boolean, str, optional
                Determines if a log file with scan results is generated. Accepts
                string representing absolute path for where log file is stored.
            timestamp : str
                Creates a timestamp to display next to bluetooth low energy
                devices detected.

            Returns
            -------
            self.device_dataframe : pandas.DataFrame
                Returns an empty pandas.DataFrame with labels preserved if no
                device is detected. Else, the method will return a dataframe
                containing the devices detected with associated MAC addresses,
                RSSI values, and timestamps.

            # NOTE: FIX EXAMPLES
            Examples
            --------
            >>> tool = BluetoothTool()
            >>> tool.bluetooth_scan(output = True)
            00:00:00,6A:30:A5:CF:F4:22,-97
            00:00:00,C8:69:CD:E7:37:81,-76
            00:00:00,5C:62:89:08:28:71,-67

            >>> tool.bluetooth_scan(output = True)
            No devices detected

            >>> devices = tool.bluetooth_scan(output = True)
            00:00:00,6A:30:A5:CF:F4:22,-97
            >>> print(devices.addr)
            6A:30:A5:CF:F4:22

            """

            scan_thread = Thread(target=self._bluetooth_scan,
                                 kwargs={"scan_time": scan_time,
                                         "to_file": to_file,
                                         "timestamp": timestamp})
            scan_thread.daemon = True
            scan_thread.start()

        def return_devices(self):

            return self.device_dataframe

        def reset_bluetooth(self):
            """
            Resets the local machine's bluetooth module. Uses the "call"
            method from subprocess as to not create a bottleneck in usage of
            this command.

            Examples
            --------
            >>> utility = BluetoothTool()
            >>> utility.reset_bluetooth()

            """
            call(['sudo', 'hciconfig', self.bluetooth_module, 'reset'])