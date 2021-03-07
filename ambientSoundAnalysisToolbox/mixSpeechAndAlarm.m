%function mixSpeechAndAlarm()
%
%   mixSpeechAndAlarm.m
%
%   OVERVIEW:
%       mix speech signal with alarm signal at for alfa in [0.1, 0.9]
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
rng(42);
% System home directory path
sysHomeFolder = '/path/to/repo/';

% Code repository root folder
repoRootFolder = [sysHomeFolder, 'OS_Edge_Compute_Data_Capture_RPi'];

% Toolbox folder
toolboxFolder = [repoRootFolder, 'ambientSoundAnalysisToolbox/'];

% Audio data path
dataPath = [toolboxFolder, 'data/wavfiles/']; 

% Codes path
codesPath = toolboxFolder;

% Output data path
outPath = [toolboxFolder, 'data/mixWavfiles/'];  

wavFiles = dir([dataPath, '*.wav']);
wavFiles = extractfield(wavFiles, 'name')';

# A structure called spectrogramParams as specified in the description of audioSpectrogram.m 
load([codesPath, 'spectrogramParams.mat']);
spectrogramParams.filtering.flag = 1;

[speechSignal,fsSpeech] = audioread([toolboxFolder, 'data/mix-resampled.wav']);
speechSignal = speechSignal(:,1);
alfa = 0.5; % Null statement. Can be removed.

for ii = 1:length(wavFiles)
    fileName = wavFiles{ii};
    
    [alarmSignal,fs] = audioread([dataPath, fileName]);
    r = floor(unifrnd(1,length(speechSignal) - length(alarmSignal)));
    sSignal = speechSignal(r:r + length(alarmSignal) - 1);
    
    for alfa = 0.1:0.1:0.9
        signal = alfa * sSignal + (1 - alfa) * alarmSignal;
        
        audiowrite([outPath, fileName(1:end-4), '-', num2str(alfa * 10), '.wav'],signal,fs);
    end
end
