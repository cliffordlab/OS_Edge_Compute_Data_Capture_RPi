%function runAlarmSounds()
%
%   ruinAlarmSounds.m
%
%   OVERVIEW:
%       This is a wrapper script to call audioSpectorgram.m
%
%   INPUT:
%       NONE
%
%   OUTPUT:
%       NONE
%
%   DEPENDENCIES & LIBRARIES:
%       NONE
%
%   REFERENCE:
%       NONE
%
%       REPO:
%       https://github.com/cliffordlab/OS_Edge_Compute_Data_Capture_RPi.git
%
%   ORIGINAL SOURCE AND AUTHORS:
%       Pradyumna Byappanahalli Suresh
%       Last Modified: Mar 5th, 2021
%       COPYRIGHT (C) 2021
%
%   LICENSE:
%       This software is offered freely and without warranty under
%       the GNU GPL-3.0 public license. See license file for
%       more information

% mix alarm sound with speech
% System home directory path
sysHomeFolder = '/path/to/repo/';

% Code repository root folder
repoRootFolder = [sysHomeFolder, 'Edge-Computing-in-OR/'];

% Toolbox folder
toolboxFolder = [repoRootFolder, 'ambientSoundAnalysisToolbox/'];

% Audio data path
dataPath = [toolboxFolder, 'data/wavfiles/']; 

% Codes path
codesPath = [toolboxFolder, 'codes/'];

wavFiles = dir([dataPath, '*.wav']);
wavFiles = extractfield(wavFiles, 'name')';

load([codesPath, 'spectrogramParams.mat']);
spectrogramParams.filtering.flag = 1;
for ii = 1:length(wavFiles)
    fileName = wavFiles{ii};
    spectrogramParams.spectrogramTitle = fileName;
    message = audioSpectrogram([dataPath, fileName], spectrogramParams);
end