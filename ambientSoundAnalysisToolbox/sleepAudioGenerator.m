%
%   sleepAudioGenerator.m
%
%   OVERVIEW:   
%       generate audio to be heard during sleep while EEG is being captured to demonstrate auditory evoked potential.      
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
%	REPO:       
%       https://github.com/cliffordlab/OS_Edge_Compute_Data_Capture_RPi.git
%
%   ORIGINAL SOURCE AND AUTHORS:     
%       Pradyumna Byappanahalli Suresh
%       Last Modified: Mar 5th, 2021 
%	    COPYRIGHT (C) 2021
%
%   LICENSE:    
%       This software is offered freely and without warranty under 
%       the GNU GPL-3.0  public license. See license file for
%       more information

%%

% System home directory path
sysHomeFolder = '/path/to/repo/';

% Code repository root folder
repoRootFolder = [sysHomeFolder, 'OS_Edge_Compute_Data_Capture_RPi/'];

% Toolbox folder
toolboxFolder = [repoRootFolder, 'ambientSoundAnalysisToolbox/'];

% Audio data path
dataPath = [toolboxFolder, 'data/']; 

fs = 22050;
sig = zeros(30*60*fs,1);
[genmed, ~] = audioread([dataPath, 'wavFiles/genmed.wav']);
sig = [sig;genmed;genmed;genmed;genmed;genmed;genmed;genmed;genmed;genmed;genmed];
s = zeros(10*60*fs,1);
sig = [sig;s];
[genhi, ~] = audioread([dataPath, 'wavFiles/genhi.wav']);
sig = [sig; genhi;genhi;genhi;genhi;genhi;genhi;genhi;genhi;genhi;genhi];
sig = [sig;s];
[ins, ~] = audioread([dataPath, 'Instrumental.mp3']);
ins = ins(2:2:end, 1);
sig = [sig;ins];
audiowrite([dataPath, 'sleepAudio.wav'],sig,fs);