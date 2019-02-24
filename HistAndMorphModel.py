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
from sklearn.decomposition import PCA
import time
import gc
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
    parser.add_argument("gengenVectors")
    parser.add_argument("forgenVectors")
    parser.add_argument("numUsers")
    parser.add_argument("mode")
    args = parser.parse_args()
        
    mode= int(args.mode)
    genuinePairs = json.load(open(args.gengenVectors))
    forgeriesPairs = json.load(open(args.forgenVectors))
    genuinePairsLBPHoG = json.load(open(args.gengenVectors+'.LBPHoG'))
    forgeriesPairsLBPHoG = json.load(open(args.forgenVectors+'.LBPHoG'))

    trGenOrbs = [genuinePairsLBPHoG[i]+genuinePairs[i] for i in genuinePairs if getUser(i,mode)<= int(args.numUsers)*0.75 ]
    trForgOrbs = [forgeriesPairsLBPHoG[i]+forgeriesPairs[i] for i in forgeriesPairs if getUserF(i,mode)<= int(args.numUsers)*0.75 ]
    
    pca = PCA(n_features = 10)
    pca.fit(np.concatenate((trGenOrbs,trForgOrbs),axis = 0))
    trGenOrbs = pca.transform(trGenOrbs)
    trForgOrbs = pca.transform(trForgOrbs)
    
    genuinePairs = None
    forgeriesPairs = None
    genuinePairsLBPHoG= None
    forgeriesPairsLBPHoG = None
    
    trYGen = [1] * len(trGenOrbs)
    trYForg = [0] * len(trForgOrbs)
    trY = np.concatenate((trYGen, trYForg),axis=0)

    trX = np.concatenate((trGenOrbs,trForgOrbs),axis = 0)
    trGenOrbs = None
    trForgOrbs = None
    
   
    
    if(os.path.isfile(args.path  +'Modelos_combinados/'+ 'rbfSVC.pkl') == False): 
        timeStart = time.time()
        print('Ajustando el SVC-RBF\n ')
        mRbf = svm.SVC()
        mRbf.fit(trX,trY)
        timeEnd= time.time()
        print(timeEnd-timeStart)
        joblib.dump(mRbf,args.path  +'Modelos_combinados/'+ 'rbfSVC.pkl')    
        mRbf = None

    if(os.path.isfile(args.path  +'Modelos_combinados/'+ 'lSVC.pkl') == False): 
        timeStart = time.time()
        print('Ajustando el SVC-L\n ')
        mLinear = svm.LinearSVC()
        mLinear.fit(trX,trY)
        timeEnd= time.time()
        print(timeEnd-timeStart)
        joblib.dump(mLinear,args.path  +'Modelos_combinados/'+ 'lSVC.pkl')
        mLinear = None

    if(os.path.isfile(args.path  +'Modelos_combinados/'+ 'bSVC.pkl') == False): 
        timeStart = time.time()
        print('Ajustando el B-SVC-RBF\n ')
        BaggingC = BaggingClassifier(svm.SVC(cache_size=200), max_samples=1.0 / 10, n_estimators=10,n_jobs=-1)
        BaggingC.fit(trX,trY)
        timeEnd= time.time()
        print(timeEnd-timeStart)
        joblib.dump(BaggingC,args.path  +'Modelos_combinados/'+ 'bSVC.pkl')
        BaggingC = None
        gc.collect() 
    

    if(os.path.isfile(args.path  +'Modelos_combinados/'+ 'rForest.pkl') == False): 
        timeStart = time.time()
        print('Ajustando el Random Forest\n ')
        rFrst = RandomForestClassifier(max_depth=2, random_state=0)
        rFrst.fit(trX, trY)
        timeEnd= time.time()
        print(timeEnd-timeStart)
        joblib.dump(rFrst,args.path  +'Modelos_combinados/'+'rForest.pkl')
        rFrst = None
        gc.collect()        

    if(os.path.isfile(args.path   +'Modelos_combinados/'+'kNN.pkl') == False): 
        timeStart = time.time()
        print('Ajustando el k-NN (N=3)\n ')
        neigh = KNeighborsClassifier(n_neighbors=3,n_jobs=4)
        neigh.fit(trX, trY)
        timeEnd= time.time()
        print(timeEnd-timeStart)
        joblib.dump(neigh,args.path +'Modelos_combinados/' + 'kNN.pkl')
        neigh = None
    
    numNeuronsInput = 195
    numNeuronsOutput = 2
    numNeurons = len(trX) //(10*(numNeuronsInput+numNeuronsOutput)) 
    trY = keras.utils.to_categorical(trY, 2)
    
    print('Ajustando el MLP\n ')
    model = Sequential()
    model.add(Dense(numNeuronsInput, activation='relu', input_shape=(195,)))
    model.add(Dropout(0.2))
    model.add(Dense(numNeurons//3 + 1 , activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(numNeurons//3 + 1, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(numNeurons//3 + 1 , activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(numNeuronsOutput, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    history = model.fit(trX, trY,
                    batch_size=256,
                    epochs=128,
                    verbose=1)
    model.save(args.path  +'Modelos_combinados/'+ 'mlp.h5')