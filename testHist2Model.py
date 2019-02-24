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
import json

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("gengenVectors")
    parser.add_argument("forgenVectors")
    parser.add_argument("numUsers")
    parser.add_argument("mode")
    args = parser.parse_args()
        
    mode= int(args.mode)
    genuinePairs = json.load(open(args.gengenVectors))
    forgeriesPairs = json.load(open(args.forgenVectors))


   
    teGenOrbs = [genuinePairs[i][:150] for i in genuinePairs if getUser(i,mode)> int(args.numUsers)*0.75 ]
    teForgOrbs = [forgeriesPairs[i][:150] for i in forgeriesPairs if getUserF(i,mode)> int(args.numUsers)*0.75 ]

    
    teX = np.concatenate((teGenOrbs,teForgOrbs),axis = 0)

    

    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    teY = np.concatenate((teYGen, teYForg),axis=0)
    
    results = {}
    
    print('Proando el SVC-RBF\n ')
    mRbf = joblib.load(args.path  + 'rbfSVC.pkl')    
    genOrbsVal = mRbf.predict(teGenOrbs)
    forgOrbsVal = mRbf.predict(teForgOrbs)
    results['rbfSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    
    print('Probando el SVC-L\n ')
    mLinear = joblib.load(args.path  + 'lSVC.pkl')
    genOrbsVal = mLinear.predict(teGenOrbs)
    forgOrbsVal = mLinear.predict(teForgOrbs)
    results['lSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]

    print('Probando el B-SVC-RBF\n ')
    BaggingC = joblib.load(args.path  + 'bSVC.pkl') 
    genOrbsVal = BaggingC.predict(teGenOrbs)
    forgOrbsVal = BaggingC.predict(teForgOrbs)
    results['bSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]

    print('Probando el Random Forest\n ')
    rFrst =joblib.load(args.path  + 'rForest.pkl')        
    genOrbsVal = rFrst.predict(teGenOrbs)
    forgOrbsVal = rFrst.predict(teForgOrbs)
    results['rForest']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    
    print('Probando el k-NN (N=3)\n ') ##Must run the model again, got overwritten
    neigh = joblib.load(args.path  + 'kNN.pkl')
    genOrbsVal = neigh.predict(teGenOrbs)
    forgOrbsVal = neigh.predict(teForgOrbs)
    results['kNN']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    
    
    teYGen = keras.utils.to_categorical(teYGen, 2)
    teYForg = keras.utils.to_categorical(teYForg, 2)
    model = load_model(args.path  + 'mlp.h5')
    genOrbsVal = model.evaluate(np.array(teGenOrbs),np.array(teYGen))
    forgOrbsVal = model.evaluate(np.array(teForgOrbs),np.array(teYForg))
    results['mlp'] = [genOrbsVal[1],forgOrbsVal[1]]
    json.dump(results,open(args.path+'results','w'))