function message = audioSpectrogram(fileName, spectrogramParams)
%
%   audioSpectrogram(fileName, spectrogramParams)
%
%   OVERVIEW:   
%       plot, label and save audio spectrogram       
%
%   INPUT:      
%       fileName - Name of the audio file to be processed.
%       spectrogramParams - A structure with various parameters.
%           spectrogramParams.windowLength - Window Length to be used in the spectrogram computation.
%           spectrogramParams.shift - The shift length to be used in the spectrogram computation.
%           spectrogramParams.analysisWindow - A two element vector that contains start and stop time of the audio signal snippet to be processed in seconds. 
%           spectrogramParams.displayFrequencyCutoff - The Display Frequency Cutoff in Hertz.
%           spectrogramParams.filtering - A structure within the structure holding information corresponding to the filter settings.
%               spectrogramParams.filtering.flag - if flag = 1, perform filtering.
%               spectrogramParams.filtering.n - n is the order of the cheby2 filter.
%               spectrogramParams.filtering.Ws - Ws is the normalized stopband edge frequency.
%               spectrogramParams.filtering.r - r is the stopband attenuation down from the peak passband value in decibels.
%
%   OUTPUT:
%       message - A string message if something goes wrong in the spectrogram computation. 
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
%       the GNU GPL-3.0 public license. See license file for
%       more information

%%

% % System home directory path
%  sysHomeFolder = '/path/to/repo/';
% 
% % Code repository root folder
% repoRootFolder = [sysHomeFolder, 'OS_Edge_Compute_Data_Capture_RPi/'];
% 
% % Toolbox folder
% toolboxFolder = [repoRootFolder, 'ambientSoundAnalysisToolbox/'];
% 
% % Audio data path
% dataPath = [toolboxFolder, 'data/']; 
% 
% % Addpath lines
% addpath([sysHomeFolder, 'ToolBox/edfRead.m']);
message = '';
% Read spectrogram settings

spectrogramTitle = spectrogramParams.spectrogramTitle;
windowLength = spectrogramParams.windowLength; % Expressed in seconds.
shift = spectrogramParams.shift; % Expressed in fraction of windowLength. Value lies in [0, 1]
% `analysisWindow` is two element vector. 
% First element is the start time and second element is the stop time in seconds.
analysisWindow = spectrogramParams.analysisWindow; 
displayFrequencyCutoff = spectrogramParams.displayFrequencyCutoff; % Expressed in Hertz
filtering.flag = spectrogramParams.filtering.flag;
filtering.n = spectrogramParams.filtering.n;
filtering.r = spectrogramParams.filtering.r;
filtering.Ws = spectrogramParams.filtering.Ws;


% Read audio file
[signal,fs] = audioread(fileName);
fs
% If audio file has more than one channel, then choose the first channel for analysis
if (size(signal,2) > 1)
    signal = signal(:,1);
end

% Sanity check and correction for analysisWindow values
if isempty(analysisWindow)
    analysisWindow = [0, (length(signal)/fs)];
end

if analysisWindow(1) < 0
    analysisWindow(1) = 0;
    message = [message, 'Start-time in analysisWindow vector cannot be less than 0. It has been set to be 0. '];
elseif analysisWindow(1) > (length(signal)/fs)
    analysisWindow(1) = (length(signal)/fs);
    message = [message, 'Start-time in analysisWindow vector cannot be greater than the length of the signal in seconds. ',...
        'It has been set to be the length of the signal in seconds. '];
end

if analysisWindow(2) > (length(signal)/fs)
    analysisWindow(2) = (length(signal)/fs);
    message = [message, 'Stop-time in analysisWindow vector cannot be greater than the length of the signal in seconds. ',...
        'It has been set to be the length of the signal in seconds. '];
end

if analysisWindow(2) <= analysisWindow(1)
    message = [message, 'Stop-time in analysisWindow cannot be greater than the start time. ',...
        'Please provide valid start-time and stop-time. '];
    return;
end

% Use analysisWindow two-element vector to crop the input signal to spectrogram
signal = signal(analysisWindow(1)*fs + 1: floor(analysisWindow(2)*fs));
% player = audioplayer(signal, fs);
% play(player);

% Construct input arguments for spectrogram command
window = round(hamming(windowLength * fs));
nOverlap = round((1-shift) * windowLength * fs);
nfft = fs;

% Filter the signal and play the filtered audio.
if (filtering.flag)
    signal = resample(signal,filtering.Ws,fs);
    fs = filtering.Ws;
    nfft = fs;
    %[b, a] = cheby2(filtering.n, filtering.r, filtering.Ws/(fs/2));
    %signal_old = signal;
    %signal = filtfilt(b, a, signal_old);
end
% player = audioplayer(signal, fs);
% play(player);


% Run the spectrogram command
figure;spectrogram(signal, window, nOverlap, nfft, fs);
view(90, -90);
colormap('jet');
set(gca,'fontweight','bold','fontsize',10); 
set(gcf, 'Position',  [100, 100, 500, 130]);
yt = get(gca, 'YTick');
if (yt(1) == 100)
    set(gca, 'YTick',yt, 'YTickLabel',yt/1000);
    ylabel('Time (secs)')
end
saveas(1,[spectrogramTitle(1:end-4), '.png'])
close all;
%title(spectrogramTitle);
% % % [s,f,~] = spectrogram(signal, window, nOverlap, nfft, fs);
% % % s = s(f<=displayFrequencyCutoff, :);
% % % s = log(abs(flipud(s)));
% % % 
% % % % imagesc(s);colorbar;
% % % ax = gca;
% % % 
% % % % Replace the original yTick values of the `imagesc` plot. 
% % % yTicks = ax.YAxis.TickValues;
% % % tickDifference = yTicks(2) - yTicks(1);
% % % for ii = 1:length(yTicks)
% % %     yTicks(ii) = size(s,1) - tickDifference * (ii - 1);
% % % end
% % % yTicks = sort(yTicks);
% % % ax.YAxis.TickValues = yTicks;
% % % 
% % % % Replace the ticklabel values to match the flipped axis.
% % % yTickLabels = ax.YAxis.TickLabels;
% % % scaling = 10^double(ax.YAxis.Exponent);
% % % for ii = 1:length(yTickLabels)
% % %     yTickLabels{ii} = num2str(size(s,1) - str2double(yTickLabels{ii})*scaling);
% % % end
% % % ax.YAxis.TickLabels = yTickLabels;

return;
end
