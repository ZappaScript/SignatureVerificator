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
from sklearn.decomposition import PCA

from sklearn.externals import joblib
import os
from keras.models import load_model
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
    args = parser.parse_args()
    
    pathBengali = 'BHSig260FIX/Bengali/Vectores_Característicos/'
    pathHindi = 'BHSig260FIX/Hindi/Vectores_Característicos/'
    pathCommon = 'signatures/Vectores_Característicos/'
        
    genuinePairsB = json.load(open(pathBengali+'gengenVectors'))
    genuinePairsH = json.load(open(pathHindi+'gengenVectors'))
    genuinePairsC = json.load(open(pathCommon+'gengenVectors'))

    forgeriesPairsB = json.load(open(pathBengali + 'forgenVectors'))
    forgeriesPairsH = json.load(open(pathHindi + 'forgenVectors'))
    forgeriesPairsC = json.load(open(pathCommon + 'forgenVectors'))

    genuinePairsBLBPHoG = json.load(open(pathBengali+'gengenVectors.LBPHoG'))
    genuinePairsHLBPHoG = json.load(open(pathHindi+'gengenVectors.LBPHoG'))
    genuinePairsCLBPHoG = json.load(open(pathCommon+'gengenVectors.LBPHoG'))

    forgeriesPairsBLBPHoG = json.load(open(pathBengali + 'forgenVectors.LBPHoG'))
    forgeriesPairsHLBPHoG = json.load(open(pathHindi + 'forgenVectors.LBPHoG'))
    forgeriesPairsCLBPHoG = json.load(open(pathCommon + 'forgenVectors.LBPHoG'))

    teGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1)> 100*0.75 ]
    teGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2)> 160*0.75 ]
    teGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3)> 55*0.75 ]
    print('Test orbs gen ', len(teGenOrbsB),' ',len(teGenOrbsH),' ',len(teGenOrbsC))

    teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)> 100 * 0.75 ]
    teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)> 160 * 0.75 ]
    teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)> 55 * 0.75 ]
    print('Test orbs forg ',len(teForgOrbsB),' ',len(teForgOrbsH),' ',len(teForgOrbsC))

    genuinePairsBLBPHoG = None
    genuinePairsHLBPHoG = None
    genuinePairsCLBPHoG = None
    forgeriesPairsBLBPHoG = None
    forgeriesPairsHLBPHoG = None
    forgeriesPairsCLBPHoG = None
    genuinePairsB = None
    genuinePairsH = None
    genuinePairsC = None
    forgeriesPairsB = None
    forgeriesPairsH = None
    forgeriesPairsC = None

    pca = joblib.load(args.path+'pca.pkl')
    teGenOrbs = pca.transform(np.concatenate((teGenOrbsB,teGenOrbsH,teGenOrbsC),axis=0))
    teForgOrbs = pca.transform(np.concatenate((teForgOrbsB,teForgOrbsH,teForgOrbsC),axis=0))
    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    
    results = {}
    print('Modelos para:',args.path)
    if (os.path.isfile(args.path  + 'bSVC.pkl')):
        print('Probando el B-SVC-RBF\n ')
        BaggingC = joblib.load(args.path  + 'bSVC.pkl') 

        genOrbsVal = BaggingC.predict(teGenOrbs)
        forgOrbsVal = BaggingC.predict(teForgOrbs)
        results['bSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
        print(modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0))
        BaggingC=None
    
    
    
    print('Proando el SVC-RBF\n ')
    mRbf = joblib.load(args.path  + 'rbfSVC.pkl')    
    genOrbsVal = mRbf.predict(teGenOrbs)
    forgOrbsVal = mRbf.predict(teForgOrbs)
    results['rbfSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print(modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0))
    mRbf = None
    print('Probando el SVC-L\n ')
    mLinear = joblib.load(args.path  + 'lSVC.pkl')
    genOrbsVal = mLinear.predict(teGenOrbs)
    forgOrbsVal = mLinear.predict(teForgOrbs)
    results['lSVC']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print(modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0))
    mLinear = None
    
    print('Probando el Random Forest\n ')
    rFrst =joblib.load(args.path  + 'rForest.pkl')        
    genOrbsVal = rFrst.predict(teGenOrbs)
    forgOrbsVal = rFrst.predict(teForgOrbs)
    results['rForest']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print(modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0))
    rFrst = None
    print('Probando el k-NN (N=3)\n ') ##Must run the model again, got overwritten
    neigh = joblib.load(args.path  + 'kNN.pkl')
    genOrbsVal = neigh.predict(teGenOrbs)
    forgOrbsVal = neigh.predict(teForgOrbs)
    results['kNN']=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print(modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0))
    neigh=None
    
    teYGen = keras.utils.to_categorical(teYGen, 2)
    teYForg = keras.utils.to_categorical(teYForg, 2)
    model = load_model(args.path  + 'mlp.h5')
    genOrbsVal = model.evaluate(np.array(teGenOrbs),np.array(teYGen))
    forgOrbsVal = model.evaluate(np.array(teForgOrbs),np.array(teYForg))
    results['mlp']=[genOrbsVal[1],forgOrbsVal[1]]
    print(genOrbsVal[1],forgOrbsVal[1])
    
    json.dump(results,open(args.path+'results','w+' ))

    
    
            

    