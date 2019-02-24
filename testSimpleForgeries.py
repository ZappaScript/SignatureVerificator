import sklearn
import json
import re
import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier 
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import argparse
from sklearn.externals import joblib
import time
from keras.models import load_model
import os

def getUser(x,mode):
    if (mode == 1):
        a = re.search('B-S-(.+?)-G.',x)
    if (mode == 2):    
        a = re.search('H-S-(.+?)-G.',x)
    if (mode == 3):
        a = re.search('C-S-(.+?)-G.',x)
        
    return(int(a.group(1)))


def getUserF(x,mode):
    
    if (mode == 1):
        a = re.search('B-S-(.+?)-F.',x)
    if (mode == 2):    
        a = re.search('H-S-(.+?)-F.',x)
    if (mode == 3):
        a = re.search('C-S-(.+?)-F.',x)
    return(int(a.group(1)))


def modelAccuraccy(vec,toTest):
    count = 0
    for i in vec:
        if (i==toTest):
            count +=1
    return (count/len(vec))


def filename(file):
    a = re.search('([a-zA-Z.0-9]+?)\Z',file)
    print (a.group(1))
    return a.group(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("simpleForgeriesVectors")
    parser.add_argument("opt")

    parser.add_argument("mode")
    args = parser.parse_args()

    simpleForgeries = json.load(open(args.simpleForgeriesVectors))
    simpleForgeriesLBPHoG = json.load(open(args.simpleForgeriesVectors+'.LBPHoG'))
    simpleForgeriesLBPHoG64 = json.load(open(args.simpleForgeriesVectors+'.64'))

    
    if(args.opt=='xor'):
        teForgOrbs = [simpleForgeries[i][:10] for i in simpleForgeries]    
    if(args.opt=='morph'):
        teForgOrbs = [simpleForgeries[i] for i in simpleForgeries]    
    if(args.opt == 'hog'):
        teForgOrbs = [simpleForgeriesLBPHoG[i] for i in simpleForgeries]
    if(args.opt == 'hog64'):
        teForgOrbs = [simpleForgeriesLBPHoG64[i] for i in simpleForgeries]
    if(args.opt == 'non-lbp'):
        teForgOrbs = [simpleForgeriesLBPHoG[i][:150] for i in simpleForgeries]
    if(args.opt == 'non-lbp64'):
        teForgOrbs = [simpleForgeriesLBPHoG64[i][:150] for i in simpleForgeries]
    if(args.opt == 'mix'):
        teForgOrbs = [simpleForgeriesLBPHoG[i]+simpleForgeries[i] for i in simpleForgeries]

    teYForg = [0] * len(teForgOrbs)
    results= {}
    print('SVC-rbf:')
    mRbf = joblib.load(args.path  + 'rbfSVC.pkl')    
    forgOrbsVal = mRbf.predict(teForgOrbs)
    print(modelAccuraccy(forgOrbsVal,0))
    results['SVC-rbf'] = modelAccuraccy(forgOrbsVal,0)
    mRbf = None
    print('SVC-l:')
    mLinear = joblib.load(args.path  + 'lSVC.pkl')
    forgOrbsVal = mLinear.predict(teForgOrbs)
    print(modelAccuraccy(forgOrbsVal,0))
    results['SVC-l'] = modelAccuraccy(forgOrbsVal,0)
    mLinear = None
    print('Probando el Random Forest\n ')
    rFrst =joblib.load(args.path  + 'rForest.pkl')        
    forgOrbsVal = rFrst.predict(teForgOrbs)
    print(modelAccuraccy(forgOrbsVal,0))
    results['Random Forest'] = modelAccuraccy(forgOrbsVal,0)
    rFrst = None

    if(os.path.isfile(args.path  + 'bSVC.pkl') == True): 
        BagginsC = joblib.load(args.path  + 'bSVC.pkl')
        forgOrbsVal = BagginsC.predict(teForgOrbs)
        print(modelAccuraccy(forgOrbsVal,0))
        results['bSVC'] = modelAccuraccy(forgOrbsVal,0)


    print('MLP')
    teYForg = keras.utils.to_categorical(teYForg, 2)
    model = load_model(args.path  + 'mlp.h5')
    forgOrbsVal = model.evaluate(np.array(teForgOrbs),np.array(teYForg))
    print(forgOrbsVal[1])
    results['MLP'] = forgOrbsVal[1]
    model = None

    print('Probando el k-NN (N=3)\n ') ##Must run the model again, got overwritten
    neigh = joblib.load(args.path  + 'kNN.pkl')
    forgOrbsVal = neigh.predict(teForgOrbs)
    print(modelAccuraccy(forgOrbsVal,0))
    results['k-NN'] = modelAccuraccy(forgOrbsVal,0)
    
    json.dump(results,open(args.path+"simpleForgeriesResult",'w+' ))
