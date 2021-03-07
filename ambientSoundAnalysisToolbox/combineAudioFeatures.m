%function combineAudioFeatures()
%
%   combineAudioFeatures.m
%
%   OVERVIEW:
%       combine mfcc and mel spectrogram energy features from
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

% Load all features and combine to create featureMatrices.

% System home directory path
sysHomeFolder = '/path/to/repo/';

% Code repository root folder
repoRootFolder = [sysHomeFolder, 'OS_Edge_Compute_Data_Capture_RPi/'];

% Toolbox folder
toolboxFolder = [repoRootFolder, 'ambientSoundAnalysisToolbox/'];

% Audio data path
featuresPath = [toolboxFolder, 'data/features/'];

load([featuresPath, 'labels.mat']);

for alfa = 1:9

    energyMat = [];
    mfccMat = [];
    
    
    %% Load all features and labels
    
    load([featuresPath, 'genhi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'oxyhi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'venthi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'cardhi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'temphi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'drughi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'perfhi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'powerhi-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'genmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'oxymed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'ventmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'cardmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'tempmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'drugmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];

    load([featuresPath, 'perfmed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    load([featuresPath, 'powermed-', num2str(alfa)]);
    energyMat = [energyMat, energies];
    mfccMat = [mfccMat, mfcc];
    
    %% Zscore each feature-vector
    mfccVar = var(mfccMat);
    energyVar = var(energyMat);
    mfccMat = zscore(mfccMat);
    energyMat = zscore(energyMat);
    
    save([featuresPath, 'mfccFeatures-', num2str(alfa)],'mfccMat','mfccVar');
    save([featuresPath, 'energyFeatures-', num2str(alfa)],'energyMat','energyVar');
    
% % %     %% TSNE
% % %     mfccTsneEmbedding = tsne(mfccMat');
% % %     energiesTsneEmbedding = tsne(energyMat');
% % %     featuresTsneEmbedding = tsne([mfccMat', energyMat']);
% % %     
% % %     %% PCA
% % %     [mfccCoeff, mfccPcaEmbedding, mfccLatent] = pca(mfccMat');
% % %     [energiesCoeff, energiesPcaEmbedding, energiesLatent] = pca(energyMat');
% % %     [featuresCoeff, featuresPcaEmbedding, featureLatent] = pca([mfccMat', energyMat']);
% % %     
% % %     % Just use first two principal componenets for plotting
% % %     mfccPcaEmbedding = mfccPcaEmbedding(:,1:2);
% % %     energiesPcaEmbedding = energiesPcaEmbedding(:,1:2);
% % %     featuresPcaEmbedding = featuresPcaEmbedding(:,1:2);
% % %     
% % %     %% Plot Settings
% % %     C = {[0, 0.4470, 0.7410], [0, 0, 1], [0.8500, 0.3250, 0.0980],[0, 0.5, 0], [0.9290, 0.6940, 0.1250], [1, 0, 0], [0.4940, 0.1840, 0.5560], [0, 0.75, 0.75],...
% % %         [0.4660, 0.6740, 0.1880], [0.05, 0, 0.75], [0.1, 0.1, 0.1]};
% % %     
% % %     markers = {'.' , 'o' , '*' , '+' , 'x' , 'square' , 'diamond', 'v' ,'^' ,  'pentagram' , 'hexagram' };
% % %     
% % %     %% TSNE MFCC
% % %     figure(1);
% % %     for ii = 1:length(mfccTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,1);plot(mfccTsneEmbedding(ii,1), mfccTsneEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     title('TSNE - MFCC [20 feaures]');
% % %     
% % %     %% TSNE Energies
% % %     figure(1);
% % %     for ii = 1:length(energiesTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,3);plot(energiesTsneEmbedding(ii,1), energiesTsneEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     
% % %     title('TSNE - Mel Filternbank Energies [10 feaures]');
% % %     %% TSNE All features
% % %     figure(1);
% % %     for ii = 1:length(featuresTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,5);plot(featuresTsneEmbedding(ii,1), featuresTsneEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     
% % %     title('TSNE - All 30 features');
% % %     %% PCA MFCC
% % %     figure(1);
% % %     for ii = 1:length(mfccTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,2);plot(mfccPcaEmbedding(ii,1), mfccPcaEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     title('PCA - MFCC [20 feaures]');
% % %     
% % %     %% PCA Energies
% % %     figure(1);
% % %     for ii = 1:length(energiesTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,4);plot(energiesPcaEmbedding(ii,1), energiesPcaEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     
% % %     title('PCA - Mel Filternbank Energies [10 feaures]');
% % %     %% PCA All features
% % %     figure(1);
% % %     for ii = 1:length(featuresTsneEmbedding)
% % %         if (labelMat(ii) == 10)
% % %             mSize = 6;
% % %             lWidth = 0.5;
% % %         else
% % %             mSize = 24;
% % %             lWidth = 6;
% % %         end
% % %         ax(1) = subplot(3,2,6);plot(featuresPcaEmbedding(ii,1), featuresPcaEmbedding(ii,2),'Color',C{labelMat(ii) + 1},'marker',markers{labelMat(ii) + 1},'MarkerSize',mSize, 'LineWidth', lWidth);hold on;
% % %     end
% % %     
% % %     title('PCA - All 30 features');
% % %     pause
% % %     close all
end
