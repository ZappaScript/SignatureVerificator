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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    
    pathBengali = 'BHSig260FIX/Bengali/Vectores_Característicos/'
    pathHindi = 'BHSig260FIX/Hindi/Vectores_Característicos/'
    pathCommon = 'signatures/Vectores_Característicos/'
        

    genuinePairsB = json.load(open(pathBengali+'gengenVectors.LBPHoG'))
    genuinePairsH = json.load(open(pathHindi+'gengenVectors.LBPHoG'))
    genuinePairsC = json.load(open(pathCommon+'gengenVectors.LBPHoG'))

    forgeriesPairsB = json.load(open(pathBengali + 'forgenVectors.LBPHoG'))
    forgeriesPairsH = json.load(open(pathHindi + 'forgenVectors.LBPHoG'))
    forgeriesPairsC = json.load(open(pathCommon + 'forgenVectors.LBPHoG'))

    trGenOrbsB = [genuinePairsB[i] for i in genuinePairsB if getUser(i,1)<= 100*0.75 ]
    trGenOrbsH = [genuinePairsH[i] for i in genuinePairsH if getUser(i,2)<= 160*0.75 ]
    trGenOrbsC = [genuinePairsC[i] for i in genuinePairsC if getUser(i,3)<= 55*0.75 ]
    print('Training orbs gen ',len(trGenOrbsB),' ',len(trGenOrbsH),' ',len(trGenOrbsC))

    trForgOrbsB = [forgeriesPairsB[i] for i in forgeriesPairsB if getUserF(i,1)<= 100 * 0.75 ]
    trForgOrbsH = [forgeriesPairsH[i] for i in forgeriesPairsH if getUserF(i,2)<= 160 * 0.75 ]
    trForgOrbsC = [forgeriesPairsC[i] for i in forgeriesPairsC if getUserF(i,3)<= 55 * 0.75 ]
    print('Training orbs forg ',len(trForgOrbsB),' ',len(trForgOrbsH),' ',len(trForgOrbsC))

    teGenOrbsB = [genuinePairsB[i] for i in genuinePairsB if getUser(i,1)> 100*0.75 ]
    teGenOrbsH = [genuinePairsH[i] for i in genuinePairsH if getUser(i,2)> 160*0.75 ]
    teGenOrbsC = [genuinePairsC[i] for i in genuinePairsC if getUser(i,3)> 55*0.75 ]
    print('Test orbs gen ', len(teGenOrbsB),' ',len(teGenOrbsH),' ',len(teGenOrbsC))

    teForgOrbsB = [forgeriesPairsB[i] for i in forgeriesPairsB if getUserF(i,1)> 100 * 0.75 ]
    teForgOrbsH = [forgeriesPairsH[i] for i in forgeriesPairsH if getUserF(i,2)> 160 * 0.75 ]
    teForgOrbsC = [forgeriesPairsC[i] for i in forgeriesPairsC if getUserF(i,3)> 55 * 0.75 ]
    print('Test orbs forg ',len(teForgOrbsB),' ',len(teForgOrbsH),' ',len(teForgOrbsC))

    genuinePairsB = None
    genuinePairsH = None
    genuinePairsC = None
    forgeriesPairsB = None
    forgeriesPairsH = None
    forgeriesPairsC = None

    trX = np.concatenate((trGenOrbsB, trGenOrbsH, trGenOrbsC, trForgOrbsB, trForgOrbsH, trForgOrbsC),axis = 0)
    

    trYGen = [1] * ( len(trGenOrbsB) + len(trGenOrbsH) + len(trGenOrbsC))
    trYForg = [0] * (len(trForgOrbsB) + len(trForgOrbsH) + len(trForgOrbsC))
    trY = np.concatenate((trYGen, trYForg),axis=0)

    
    if(os.path.isfile(args.path+'Global_rbfSVC_LBPHoG.pkl')==False):
        print('Ajustando el SVC-RBF\n ')
        mRbf = svm.SVC(cache_size=1000)
        mRbf.fit(trX,trY)
        joblib.dump(mRbf, args.path+'Global_rbfSVC_LBPHoG.pkl')    
        mRbf = None
    
    if(os.path.isfile(args.path+'Global_lSVC_LBPHoG.pkl')==False):
        print('Ajustando el SVC-L\n ')
        mLinear = svm.LinearSVC()
        mLinear.fit(trX,trY)
        joblib.dump(mLinear,args.path+'Global_lSVC_LBPHoG.pkl')
        mLinear = None
    
    if(os.path.isfile(args.path+'GLobal_bSVC_LBPHoG.pkl')==False):
        print('Ajustando el BSVC\n ')
        BaggingC = BaggingClassifier(svm.SVC(cache_size=50), max_samples=1.0 / 10, n_estimators=10,n_jobs=1)
        BaggingC.fit(trX,trY)
        joblib.dump(BaggingC, args.path+'GLobal_bSVC_LBPHoG.pkl') 
        BaggingC = None
    
    
    if(os.path.isfile(args.path+'Global_rForest_LBPHoG.pkl')==False):
        print('Ajustando el Random Forest\n ')
        rFrst = RandomForestClassifier(max_depth=2, random_state=0)
        rFrst.fit(trX, trY)
        joblib.dump(rFrst, args.path+'Global_rForest_LBPHoG.pkl') 
        rFrst = None
    
    
    if(os.path.isfile(args.path+'Global_kNN_LBPHoG.pkl')==False):
        print('Ajustando el k-NN (N=3)\n ')
        neigh = KNeighborsClassifier(n_neighbors=3,n_jobs=4)
        neigh.fit(trX, trY) 
        joblib.dump(neigh, args.path+'Global_kNN_LBPHoG.pkl')
        neigh = None

    
    if(os.path.isfile(args.path+'Gloabl_mlp_LBPHoG.h5')==False):
        
        teX = np.concatenate((teGenOrbsB, teGenOrbsH, teGenOrbsC, teForgOrbsB, teForgOrbsH, teForgOrbsC),axis = 0)
        teYGen = [1] * ( len(teGenOrbsB) + len(teGenOrbsH) + len(teGenOrbsC))
        teYForg = [0] * (len(teForgOrbsB) + len(teForgOrbsH) + len(teForgOrbsC))
        teY = np.concatenate((teYGen, teYForg),axis=0)
        trY = keras.utils.to_categorical(trY, 2)
        teY = keras.utils.to_categorical(teY, 2)
        print('Ajustando el MLP\n ')
        model = Sequential()
        model.add(Dense(128, activation='relu', input_shape=(180,)))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(2, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
        history = model.fit(trX, trY,
                        batch_size=128,
                        epochs=128,
                        verbose=1,
                        validation_data=(teX, teY))

        model.save(args.path+'Gloabl_mlp_LBPHoG.h5')
            

    