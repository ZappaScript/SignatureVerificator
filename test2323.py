import sklearn
import json
import re
import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier, VotingClassifier 
import keras
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import argparse
from sklearn.externals import joblib
from keras.wrappers.scikit_learn import KerasClassifier
import pickle
import os

def mlpClassifier():
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(195,)))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    return model

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

    Amount = 0.02
    Amount2 = 0.98
    trGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1)< 2 ]
    trGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2)< 2 ]
    trGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3)< 2 ]
    trForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)< 2 ]
    trForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)< 2 ]
    trForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)< 2 ]
    teGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1)>= 100 ]
    teGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2)>= 160  ]
    teGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3)>= 55  ]
    teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)>= 100 ]
    teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)>= 160 ]
    teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)>= 55 ]
    ##trGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1)< 100 * Amount ]
    ##trGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2)< 160 * Amount ]
    ##trGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3)< 55 * Amount ]
    ##
    ##trForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)< 100 * Amount ]
    ##trForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)< 160 * Amount ]
    ##trForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)< 155 * Amount ]
    ##
##
    ##teGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1)>= 100 *  Amount2 ]
    ##teGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2)>= 160 *  Amount2 ]
    ##teGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3)>= 55 * Amount2 ]
    ##
##
    ##teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)>= 100 * Amount2]
    ##teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)>= 160 * Amount2]
    ##teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)>= 55 * Amount2]
    

    genuinePairsB = None
    genuinePairsH = None
    genuinePairsC = None
    forgeriesPairsB = None
    forgeriesPairsH = None
    forgeriesPairsC = None


    trGenOrbs = np.concatenate((trGenOrbsB,trGenOrbsH,trGenOrbsC),axis=0)
    trForgOrbs = np.concatenate((trForgOrbsB,trForgOrbsH,trForgOrbsC),axis=0)
    trYGen = [1] * len(trGenOrbs)
    trYForg = [0] * len(trForgOrbs)

    teGenOrbs = np.concatenate((teGenOrbsB,teGenOrbsH,teGenOrbsC),axis=0)
    teForgOrbs = np.concatenate((teForgOrbsB,teForgOrbsH,teForgOrbsC),axis=0)
    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    trGenOrbsB = None
    trGenOrbsH = None
    trGenOrbsC = None
    trForgOrbsB = None
    trForgOrbsH = None
    trForgOrbsC = None
    teGenOrbsB = None
    teGenOrbsH = None
    teGenOrbsC = None
    teForgOrbsB = None
    teForgOrbsH = None
    teForgOrbsC = None

    results = {}
    print('Probando el k-NN (N=3)\n ') ##Must run the model again, got overwritten
    
    neigh = KNeighborsClassifier(n_neighbors=3,n_jobs=1)
    BaggingC = BaggingClassifier(svm.SVC(cache_size = 100), max_samples=1.0 / 10, n_estimators=10,n_jobs=1) 
    mRbf = mRbf = svm.SVC(cache_size=1000)
    mLinear = mLinear = svm.LinearSVC()
    rFrst = RandomForestClassifier(max_depth=2, random_state=0)       
    ##mlp =  load_model(args.path  + 'mlp.h5')
    model = KerasClassifier( build_fn = mlpClassifier, epochs=1,batch_size=128)
    
    eclf = VotingClassifier(estimators=[('kNN', neigh), ('rbfSVC', mRbf), ('rForest', rFrst),('lSVC', mLinear),('mlp',model),('bSVC',BaggingC) ], voting='hard')
    a = eclf.fit(np.concatenate ((trGenOrbs,trForgOrbs),axis = 0 ),np.concatenate((trYGen,trYForg),axis = 0))  
    b = eclf.predict(teGenOrbs)
    with open('Modelo_Global_Combinado/VotingClasifier.pkl', "wb") as f:
        
        pickle.dump(eclf, f)
    
    ##print(sum (b) / len(b))
    ##b = eclf.predict(teForgOrbs)
    ##print(1 - sum (b) / len(b))

    joblib.dump(eclf,'Modelo_Global_Combinado/VotingClasifier.pkl')


    

