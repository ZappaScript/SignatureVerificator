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
    parser.add_argument("vectorName")
    parser.add_argument("opt")
    args = parser.parse_args()
    
    pathBengali = 'BHSig260FIX/Bengali/Vectores_Característicos/'
    pathHindi = 'BHSig260FIX/Hindi/Vectores_Característicos/'
    pathCommon = 'signatures/Vectores_Característicos/'
        
   
    forgeriesPairsB = json.load(open(pathBengali + args.vectorName))
    forgeriesPairsH = json.load(open(pathHindi + args.vectorName))
    forgeriesPairsC = json.load(open(pathCommon + args.vectorName))


    forgeriesPairsBLBPHoG = json.load(open(pathBengali + args.vectorName +'.LBPHoG'))
    forgeriesPairsHLBPHoG = json.load(open(pathHindi + args.vectorName+'.LBPHoG'))
    forgeriesPairsCLBPHoG = json.load(open(pathCommon + args.vectorName+'.LBPHoG'))

    
    if(args.opt=='morph'):
        teForgOrbsB = [forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG  ]
        teForgOrbsH = [forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG  ]
        teForgOrbsC = [forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG ]
        
    if(args.opt == 'hog'):
        teForgOrbsB = [forgeriesPairsBLBPHoG[i] for i in forgeriesPairsBLBPHoG  ]
        teForgOrbsH = [forgeriesPairsHLBPHoG[i] for i in forgeriesPairsHLBPHoG  ]
        teForgOrbsC = [forgeriesPairsCLBPHoG[i] for i in forgeriesPairsCLBPHoG ]

    if(args.opt == 'mix'):
        teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG  ]
        teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG  ]
        teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG ]


    if(args.opt == 'pca'):
        teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG  ]
        teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG  ]
        teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG ]
        pca = joblib.load(args.path+'pca.pkl')
        teForgOrbs = pca.transform(np.concatenate((teForgOrbsB,teForgOrbsH,teForgOrbsC),axis=0))
    else:
        teForgOrbs = np.concatenate((teForgOrbsB,teForgOrbsH,teForgOrbsC),axis=0)



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
    
   
    
    teYForg = [0] * len(teForgOrbs)
    
    results = {}
    print('Modelos para:',args.path)
    if (os.path.isfile(args.path  + 'bSVC.pkl')):
        print('Probando el B-SVC-RBF\n ')
        BaggingC = joblib.load(args.path  + 'bSVC.pkl') 
        forgOrbsVal = BaggingC.predict(teForgOrbs)
        results['bSVC']=modelAccuraccy(forgOrbsVal,0)
        print(results['bSVC'])
        BaggingC=None
    
    
    
    print('Probando el SVC-RBF\n ')
    mRbf = joblib.load(args.path  + 'rbfSVC.pkl')    
    forgOrbsVal = mRbf.predict(teForgOrbs)
    results['rbfSVC'] =  modelAccuraccy(forgOrbsVal,0)
    print(results['rbfSVC'])
    mRbf = None

    print('Probando el SVC-L\n ')
    mLinear = joblib.load(args.path  + 'lSVC.pkl')
    forgOrbsVal = mLinear.predict(teForgOrbs)
    results['lSVC']= modelAccuraccy(forgOrbsVal,0)
    print(results['lSVC'])
    mLinear = None
    
    print('Probando el Random Forest\n ')
    rFrst =joblib.load(args.path  + 'rForest.pkl')        
    forgOrbsVal = rFrst.predict(teForgOrbs)
    results['rForest']=modelAccuraccy(forgOrbsVal,0)
    print(results['rForest'])
    rFrst = None

    print('Probando el k-NN (N=3)\n ') ##Must run the model again, got overwritten
    neigh = joblib.load(args.path  + 'kNN.pkl')
    forgOrbsVal = neigh.predict(teForgOrbs)
    results['kNN']=modelAccuraccy(forgOrbsVal,0)
    print(results['kNN'])
    neigh=None
    
    teYForg = keras.utils.to_categorical(teYForg, 2)
    model = load_model(args.path  + 'mlp.h5')
    forgOrbsVal = model.evaluate(np.array(teForgOrbs),np.array(teYForg))
    results['mlp']=forgOrbsVal[1]
    print(results['mlp'])
    json.dump(results,open(args.path+'simpleForgeriesResult','w+' ))