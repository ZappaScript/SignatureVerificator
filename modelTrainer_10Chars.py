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


    trGenOrbs = [genuinePairs[i] for i in genuinePairs if getUser(i,mode)<= int(args.numUsers)*0.75 ]
    trForgOrbs = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i,mode)<= int(args.numUsers)*0.75 ]
    teGenOrbs = [genuinePairs[i] for i in genuinePairs if getUser(i,mode)> int(args.numUsers)*0.75 ]
    teForgOrbs = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i,mode)> int(args.numUsers)*0.75 ]

    trX = np.concatenate((trGenOrbs,trForgOrbs),axis = 0)
    teX = np.concatenate((teGenOrbs,teForgOrbs),axis = 0)

    trYGen = [1] * len(trGenOrbs)
    trYForg = [0] * len(trForgOrbs)
    trY = np.concatenate((trYGen, trYForg),axis=0)

    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    teY = np.concatenate((teYGen, teYForg),axis=0)
    
    timeStart = time.time()
    print('Ajustando el SVC-RBF\n ')
    mRbf = svm.SVC()
    mRbf.fit(trX,trY)
    timeEnd= time.time()
    print(timeEnd-timeStart)
    joblib.dump(mRbf,args.path  + 'rbfSVC.pkl')
    mRbf = None

    timeStart = time.time()
    print('Ajustando el SVC-L\n ')
    mLinear = svm.LinearSVC()
    mLinear.fit(trX,trY)
    timeEnd= time.time()
    print(timeEnd-timeStart)
    joblib.dump(mLinear,args.path  + 'lSVC.pkl')
    mLinear = None

    timeStart = time.time()
    print('Ajustando el B-SVC-RBF\n ')
    BaggingC = BaggingClassifier(svm.SVC(cache_size=200), max_samples=1.0 / 10, n_estimators=10,n_jobs=-1)
    BaggingC.fit(trX,trY)
    timeEnd= time.time()
    print(timeEnd-timeStart)
    joblib.dump(BaggingC,args.path  + 'bSVC.pkl') 
    BaggingC = None

    timeStart = time.time()
    print('Ajustando el Random Forest\n ')
    rFrst = RandomForestClassifier(max_depth=2, random_state=0)
    rFrst.fit(trX, trY)
    timeEnd= time.time()
    print(timeEnd-timeStart)
    joblib.dump(rFrst,args.path  + 'rForest.pkl') 
    rFrst = None

    timeStart = time.time()
    print('Ajustando el k-NN (N=3)\n ')
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(trX, trY)
    timeEnd= time.time()
    print(timeEnd-timeStart)
    joblib.dump(neigh,args.path  + 'kNN.pkl')
    neigh = None

    trY = keras.utils.to_categorical(trY, 2)
    teY = keras.utils.to_categorical(teY, 2)
    print('Ajustando el MLP\n ')
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(15,)))
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

    model.save(args.path  + 'mlp.h5')
            

    