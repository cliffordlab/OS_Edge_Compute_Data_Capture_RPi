"""
Author: Pradyumna B Suresha (alias Pradyumna94)
Last Modified: Mar 22nd, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from scipy.special import softmax
from scipy.signal import medfilt
from matplotlib import animation
from bisect import bisect
from pytz import timezone
from dateutil import tz
from glob import glob

import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Specify the folder with all the recorded data
dataFolder = ''

rpiIds = ['room1_1', 'room1_2', 'room1_3', 'room2_4', 'room2_5', 'room2_6' ,'room3_7', 'room3_8', 'room3_9']
data = dict()

beta = 0.2

# Read the data
for idx in range(9):
    
    data[rpiIds[idx]] = dict()
    dataFile = glob(dataFolder + rpiIds[idx] + "/04_07_20_*.txt")[0]
    
    with open(dataFile) as fp:
        lines = fp.read().splitlines()

    lines = [line for line in lines if 'D9:DB:AC' in line] 

    dates = [line.split(',')[0] for line in lines]
    btPower = [float(line.split(',')[-1]) for line in lines]

    dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in dates]

    dates = [date - timedelta(hours=4) for date in dates]
    #dates = [timezone('US/Eastern').localize(date) for date in dates]
    #dates = [date.astimezone(timezone('US/Eastern')) for date in dates]
    
    btPower = [btPower[idx] for idx, date in enumerate(dates) if date.hour == 9 and date.minute >= 40 and date.minute < 50]
    dates = [date for date in dates if date.hour == 9 and date.minute >= 40 and date.minute < 50]
    
    times = [datetime.strptime("2020-04-07 09:40:01", "%Y-%m-%d %H:%M:%S") + timedelta(seconds=idx) for idx in range(600)]

    btPowerInterpolated = []
    for time in times:
        if time in dates:
            bidx = dates.index(time)
            interpolatedValue = max([btPower[bidx], -200])
        else:
            bidx = bisect(dates, time)
            previousBtPower = -200 if bidx == 0 else btPower[bidx-1]
            timeDifference = 1 if bidx == 0 else (time - dates[bidx-1]).total_seconds()
            interpolatedValue = max([previousBtPower * max([beta * timeDifference, 1]), -200])
        
        btPowerInterpolated.append(interpolatedValue)
    
    btPowerInterpolated = medfilt(btPowerInterpolated)
    data[rpiIds[idx]]['dates'] = times
    data[rpiIds[idx]]['btPower'] = btPowerInterpolated

# Plot all signals on one plot and visualize the btPower
tzone = tz.gettz('US/Eastern')

twoMinutes = mdates.MinuteLocator(interval = 2)
minutes = mdates.MinuteLocator()
timeForm = mdates.DateFormatter('%H:%M')

# Create figure and plot space
fig, ax = plt.subplots(figsize=(12,8))

piLines = [0]*9
colors = ['b', 'darkviolet', 'm', 'c', 'tab:blue', 'lime', 'tab:orange', 'tab:brown', 'r']
markers = ['*','*', '*', 'o','o','o','+','+','+']
for idx in range(9):
    #x = data[rpiIds[idx]]['dates']
    y = data[rpiIds[idx]]['btPower']
    x = range(len(y))
    plt.plot(x, y, color=colors[idx], linestyle = "None", marker=markers[idx], markersize=12)

xmax = len(y)

x = [0,0,159,159]
y = [-190, -50, -50, -190]
plt.fill(x, y, color = 'b', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [146,146,286,286]
y = [-190, -50, -50, -190]
plt.fill(x, y, color = 'g', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [268,268,480,480]
y = [-190, -50, -50, -190]
plt.fill(x, y, color = 'r', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [470,470,xmax,xmax]
y = [-190, -50, -50, -190]
plt.fill(x, y, color = 'b', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room I'
plt.text(0.05906, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room II'
plt.text(0.2875, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room III'
plt.text(0.5550, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room I'
plt.text(0.8350, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

# Set title and labels for axes
plt.xlabel("Time (seconds)", fontsize=24)
plt.ylabel("RSSI (decibels)", fontsize=24)
plt.xlim((0, xmax))
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)



legendText = [ 'Room 1 - RPi 1', 'Room 1 - RPi 2', 'Room 1 - RPi 3', 'Room 2 - RPi 1', 'Room 2 - RPi 2', 'Room 2 - RPi 3', 'Room 3 - RPi 1', 'Room 3 - RPi 2', 'Room 3 - RPi 3']
plt.grid(True)

plt.ylim((-190,-50))
plt.savefig('RSSI.png')
plt.clf()

# Probabilities plot
dataPerRoom = dict()
dataPerRoom['room1'] = (np.array(data[rpiIds[0]]['btPower']) + np.array(data[rpiIds[1]]['btPower']) + np.array(data[rpiIds[2]]['btPower'])) / 3
dataPerRoom['room2'] = (np.array(data[rpiIds[3]]['btPower']) + np.array(data[rpiIds[4]]['btPower']) + np.array(data[rpiIds[3]]['btPower'])) / 3
dataPerRoom['room3'] = (np.array(data[rpiIds[6]]['btPower']) + np.array(data[rpiIds[7]]['btPower']) + np.array(data[rpiIds[8]]['btPower'])) / 3

probabilities = np.zeros((len(times), 3))
for idx, time in enumerate(times):
    currentBtPowers = np.array([dataPerRoom['room1'][idx], dataPerRoom['room2'][idx], dataPerRoom['room3'][idx]])
    probabilities[idx,:] = softmax(currentBtPowers)

fig, ax = plt.subplots(figsize=(12,8))
roomLines = [0]*3
colors = ['b','lime','red']
markers = ['*','o','+']
for idx in range(3):
    room = 'room' + str(idx + 1)
    x = data[rpiIds[idx]]['dates']
    y = probabilities[:,idx]
    x = range(len(y))
    plt.plot(x, y, color=colors[idx], linestyle="None", marker=markers[idx], markersize=12)
    
xmax = len(y)

x = [0,0,159,159]
y = [-0.1, 1.1, 1.1, -0.1]
plt.fill(x, y, color = 'b', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [146,146,286,286]
y = [-0.1, 1.1, 1.1, -0.1]
plt.fill(x, y, color = 'g', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [268,268,480,480]
y = [-0.1, 1.1, 1.1, -0.1]
plt.fill(x, y, color = 'r', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

x = [470,470,xmax,xmax]
y = [-0.1, 1.1, 1.1, -0.1]
plt.fill(x, y, color = 'b', linestyle = 'dashed', linewidth=0.5, alpha=0.3)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room I'
plt.text(0.05906, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room II'
plt.text(0.2875, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room III'
plt.text(0.5550, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
textstr = 'Room I'
plt.text(0.8350, 0.50, textstr, transform=ax.transAxes, fontsize=24,
        verticalalignment='top', bbox=props)

# Set title and labels for axes
plt.xlabel("Time (seconds)", fontsize = 24)
plt.ylabel("Probability of being in Room I, II or III", fontsize=24)
plt.xlim((0, xmax))
plt.xticks(fontsize=24)
plt.yticks(fontsize=24)

plt.grid(True)

plt.ylim((-0.1,1.1))
plt.savefig('probabilities.png')

# Validation
correct = 0
for ii in range(600):
    probability = probabilities[ii,:]
    roomN = np.argmax(probability) + 1

    if (ii >= 0 and ii < 146):
        if roomN == 1:
            correct += 1

    if (ii >= 146 and ii < 159):
        if roomN == 1 or roomN == 2:
            correct += 1

    if (ii >= 159 and ii < 268):
        if roomN == 2:
            correct += 1


    if (ii >= 268 and ii < 286):
        if roomN == 2 or roomN == 3:
            correct += 1


    if (ii>= 286 and ii < 470):
        if roomN == 3:
            correct += 1


    if (ii >= 470 and ii < 480):
            correct += 1

    
    if (ii >= 480):
        if roomN == 1:
            correct += 1

print(correct)
