#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Mar 5th, 2020
Copyright [2021] [Clifford Lab]
LICENSE:
This software is offered freely and without warranty under
the GNU GPL-3.0 public license. See license file for
more information
"""
from sklearn.model_selection import StratifiedKFold, GridSearchCV, LeaveOneOut, RandomizedSearchCV
from sklearn.metrics import f1_score, precision_recall_curve, average_precision_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn.linear_model import LogisticRegression, ElasticNet
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from inspect import signature
from sklearn.svm import SVC
from tqdm import tqdm
from sys import path

import matplotlib.pyplot as plt
import texttable as tt
import scipy.io as sio
import pandas as pd
import numpy as np
import collections
import pickle
import time
import pdb
import os

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


class OrderedSet(collections.Set):
    def __init__(self, iterable=()):
        self.d = collections.OrderedDict.fromkeys(iterable)

    def __len__(self):
        return len(self.d)

    def __contains__(self, element):
        return element in self.d

    def __iter__(self):
        return iter(self.d)

def evaluate(y_true, 
             y_pred_prob, 
             size):  
    """Evaluate testing performance for given targeting size.
    
    Parameters
    ----------
    y_true: array, shape = [n_samples]
      True values of y.
      
    y_pred_prob: array, shape = [n_samples]
      Predicted scores/probability of y.
      
    size: int
      Targeting patients size
      
    Returns
    -------
    Precision and recall scores
    """
    indices = np.argsort(y_pred_prob)[::-1]
    threshold = y_pred_prob[indices][size-1]
    y_pred = np.where(y_pred_prob>=threshold, 1 ,0)
    return [precision_score(y_true, y_pred), recall_score(y_true, y_pred), threshold]
    
    

def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    
    # Begin CHANGES
    fst_empty_cell = (columnwidth-3)//2 * " " + "t/p" + (columnwidth-3)//2 * " "
    
    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    # Print header
    print("    " + fst_empty_cell, end=" ")
    # End CHANGES
    
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
        
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()

kfolds = 5

np.random.seed(seed=10)
    
#############
# Load data #
#############

nClasses = 11

labelsFile = '/path/to/repo/OS_Edge_Compute_Data_Capture_RPi/ambientSoundAnalysisToolbox/data/features/labels.mat'
labelsDict = sio.loadmat(labelsFile)
Y = labelsDict['labelMat'].ravel() 

##################
# Load alfa data #
##################

for alfa in range(1,10):
    print(alfa)

    mfccFeaturesFile = '/path/to/repo/OS_Edge_Compute_Data_Capture_RPi/ambientSoundAnalysisToolbox/data/features/mfccFeatures-' + str(int(alfa)) + '.mat'
    mfccFeaturesDict = sio.loadmat(mfccFeaturesFile)
    mfccFeatures = mfccFeaturesDict['mfccMat']
    mfccVar = mfccFeaturesDict['mfccVar']

    energyFeaturesFile = '/path/to/repo/OS_Edge_Compute_Data_Capture_RPi/ambientSoundAnalysisToolbox/data/features/energyFeatures-' + str(int(alfa)) + '.mat'
    energyFeaturesDict = sio.loadmat(energyFeaturesFile)
    energyFeatures = energyFeaturesDict['energyMat']
    energyVar = energyFeaturesDict['energyVar']

    X_alfa =  np.transpose(np.concatenate((mfccFeatures, energyFeatures, mfccVar, energyVar),0))

    ##########################
    # kfold cross-validation #
    ##########################

    skf = StratifiedKFold(n_splits=kfolds, shuffle=True, random_state=42)

    loo = LeaveOneOut()
    loo.get_n_splits(X_alfa)

    y_train_prob_meta_xg = np.zeros((X_alfa.shape[0], nClasses))
    y_train_prob_meta_rf = np.zeros((X_alfa.shape[0], nClasses))
    y_train_prob_meta_lr = np.zeros((X_alfa.shape[0], nClasses))
    y_train_prob_meta_svc = np.zeros((X_alfa.shape[0], nClasses))
    feat_wght_xg = np.zeros(X_alfa.shape[1])
    feat_wght_rf = np.zeros(X_alfa.shape[1])
    feat_wght_lr = np.zeros(X_alfa.shape[1])
    feat_wght_svc = np.zeros(X_alfa.shape[1])

    # for idx, (train_idx, val_idx) in enumerate(loo.split(X_alfa)):
    for idx, (train_idx, val_idx) in enumerate(skf.split(X_alfa, Y)):
        #print('='*80)
        print('Fold = {}'.format(idx))
        #print('='*80)

        # define train-validation split
        X_train_splt = X_alfa[train_idx]
        y_train_splt = Y[train_idx]

        X_val_splt = X_alfa[val_idx]
        y_val_splt = Y[val_idx]

        ################################################################################
        # define classifier

        ############
        # XG Boost #
        ############

        clf_xg = XGBClassifier(
          n_estimators=150,
          objective='multi:softmax',
          num_class=11,
          n_jobs=-1,
          max_depth=6,
          random_state=42)

        #################
        # Random Forest #
        #################

        randomForest = RandomForestClassifier(class_weight='balanced')

        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start = 50, stop = 2000, num = 40)]
        # Number of features to consider at every split
        max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4, 6, 8, 10]
        # Method of selecting samples for training each tree
        bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}
        score = 'f1_micro'
        
        clf_rf = RandomizedSearchCV(estimator = randomForest, param_distributions = random_grid, n_iter = 10, cv = 5, scoring=score, verbose=0, random_state=42, n_jobs = -1)

        #######################
        # Logistic Regression #
        #######################

        logistic = LogisticRegression(class_weight='balanced', penalty='elasticnet', solver='saga', multi_class='multinomial')

        # Create regularization hyperparameter space
        C = np.logspace(-1, 1, 10)
        l1_ratio = np.linspace(0, 1, 11) # alpha

        # Create hyperparameter options
        hyperparameters = dict(C=C, l1_ratio=l1_ratio)
        score = 'f1_micro'

        # Create grid search using 5-fold cross validation
        clf_lr = GridSearchCV(logistic, hyperparameters, cv=5, scoring=score, verbose=0, n_jobs = -1)

        #######    
        # SVC #
        #######
        
        # Set the parameters by cross-validation
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-4, 1e-3, 1e-2, 1e-1, 1e-0, 1e-1, 1e2, 1e3],
                             'C': [0.01, 0.1, 1, 10, 100, 1000]},
                            {'kernel': ['linear'], 'C': [0.01, 0.1, 1, 10, 100, 1000]}]
       
        score = 'f1_micro'

        clf_svc = GridSearchCV(SVC(probability=True, class_weight='balanced'), tuned_parameters, cv=5, scoring=score, verbose=0, n_jobs = -1)

        ############################################################################

        # train classifier
        t1 = time.time()
        clf_xg.fit(X_train_splt, y_train_splt)
        # print('Training XGB uses {:.2f} secs'.format(time.time() - t1))
        print('XGBoost Trained')
        
        t1 = time.time()
        clf_rf.fit(X_train_splt, y_train_splt)
        # print('Training RF uses {:.2f} secs'.format(time.time() - t1))
        # print(clf_rf.cv_results_)  
        print('RF Trained')
        
        """    
        t1 = time.time()
        clf_lr.fit(X_train_splt, y_train_splt)
        # print('Training LR uses {:.2f} secs'.format(time.time() - t1))
        print(clf_lr.cv_results_)  
        print('LR Trained')

        t1 - time.time()
        clf_svc.fit(X_train_splt, y_train_splt)
        # print('Training SVC uses {:.2f} secs'.format(time.time() - t1))
        print(clf_svc.cv_results_)  
        print('SVC Trained')
        """
        # make prediction on fold and obtain probabilities

        y_val_prob_xg = clf_xg.predict_proba(X_val_splt)
        y_val_prob_rf = clf_rf.predict_proba(X_val_splt)
        #y_val_prob_lr = clf_lr.predict_proba(X_val_splt)
        #y_val_prob_svc = clf_svc.predict_proba(X_val_splt)

        # keep prediction result
        y_train_prob_meta_xg[val_idx, 0:nClasses] = y_val_prob_xg
        y_train_prob_meta_rf[val_idx, 0:nClasses] = y_val_prob_rf
        #y_train_prob_meta_lr[val_idx, 0:nClasses] = y_val_prob_lr
        #y_train_prob_meta_svc[val_idx, 0:nClasses] = y_val_prob_svc

        # get feature importance for fold
        feat_wght_xg += clf_xg.feature_importances_ / kfolds
        feat_wght_rf += clf_rf.best_estimator_.feature_importances_ / kfolds
        #feat_wght_lr += clf_lr.best_estimator_.coef_.reshape(-1) / kfolds


    labels = np.array(Y)
    threshold = 0.5
    y_pred_xg = np.argmax(y_train_prob_meta_xg, axis=1)
    y_pred_rf = np.argmax(y_train_prob_meta_rf, axis=1)
    #y_pred_lr = np.argmax(y_train_prob_meta_lr, axis=1)
    #y_pred_svc = np.argmax(y_train_prob_meta_svc, axis=1)
    C_xg = confusion_matrix(labels, y_pred_xg, labels = [0,1,2,3,4,5,6,7,8,9,10])
    C_rf = confusion_matrix(labels, y_pred_rf, labels = [0,1,2,3,4,5,6,7,8,9,10])
    #C_lr = confusion_matrix(labels, y_pred_lr, labels = [0,1,2,3,4,5,6,7,8,9,10])
    #C_svc = confusion_matrix(labels, y_pred_svc, labels = [0,1,2,3,4,5,6,7,8,9,10])
    F1_xg = f1_score(labels, y_pred_xg, labels = [0,1,2,3,4,5,6,7,8,9,10], average='micro')
    F1_rf = f1_score(labels, y_pred_rf, labels = [0,1,2,3,4,5,6,7,8,9,10], average='micro')
    #F1_lr = f1_score(labels, y_pred_lr, labels = [0,1,2,3,4,5,6,7,8,9,10], average='micro')
    #F1_svc = f1_score(labels, y_pred_svc, labels = [0,1,2,3,4,5,6,7,8,9,10], average='micro')
    #F1_all = [F1_xg, F1_rf, F1_lr, F1_svc]
    F1_all = [F1_xg, F1_rf]

    F1_macro_xg = f1_score(labels, y_pred_xg, labels = [0,1,2,3,4,5,6,7,8,9,10], average='macro')
    F1_macro_rf = f1_score(labels, y_pred_rf, labels = [0,1,2,3,4,5,6,7,8,9,10], average='macro')
    #F1_macro_lr = f1_score(labels, y_pred_lr, labels = [0,1,2,3,4,5,6,7,8,9,10], average='macro')
    F1_macro_all = [F1_macro_xg, F1_macro_rf]

    featNames = ['mfcc01', 'mfcc02', 'mfcc03', 'mfcc04', 'mfcc05', 'mfcc06', 'mfcc07', 'mfcc08', 'mfcc09', 'mfcc10','mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20', 'ener01', 'ener02', 'ener03', 'ener04', 'ener05', 'ener06', 'ener07', 'ener08', 'ener09', 'ener10', 'mfccVar','energyVar']
    feat_wght = pd.DataFrame({
        'feature': featNames, 
        'wght_xgb': feat_wght_xg,
        'wght_rf': feat_wght_rf,
        #'coef_lr': feat_wght_lr
    })
    feat_wght = feat_wght.sort_values(by='wght_xgb', ascending=False)
    print('='*80)
    print(feat_wght)
    print('='*80)
    print(F1_all)
    print('='*80)
    print(F1_macro_all)
    print('='*80)
    print_cm(C_xg, ['0','1','2','3','4','5','6','7','8','9','10'])
    print_cm(C_rf, ['0','1','2','3','4','5','6','7','8','9','10'])
    #print_cm(C_lr, ['0','1','2','3','4','5','6','7','8','9','10'])
    #print_cm(C_svc, ['0','1','2','3','4','5','6','7','8','9','10'])

