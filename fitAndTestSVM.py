import sklearn
import json
import re
import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import argparse
from sklearn.externals import joblib


def getUser(x):
    a = re.search('H-S-(.+?)-G.',x)
    return(int(a.group(1)))

def getUserF(x):
    a = re.search('H-S-(.+?)-F.',x)
    return(int(a.group(1)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("gengenVectors")
    parser.add_argument("forgenVectors")
    parser.add_argument("numUsers")
    args = parser.parse_args()
        

    genuinePairs = json.load(open(args.path+args.gengenVectors))
    forgeriesPairs = json.load(open(args.path+args.forgenVectors))


    trGenOrbs = [genuinePairs[i] for i in genuinePairs if getUser(i)<= int(args.numUsers)*0.75 ]
    trForgOrbs = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i)<= int(args.numUsers)*0.75 ]
    teGenOrbs = [genuinePairs[i] for i in genuinePairs if getUser(i)> int(args.numUsers)*0.75 ]
    teForgOrbs = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i)> int(args.numUsers)*0.75 ]

    trX = np.concatenate((trGenOrbs,trForgOrbs),axis = 0)
    teX = np.concatenate((teGenOrbs,teForgOrbs),axis = 0)

    trYGen = [1] * len(trGenOrbs)
    trYForg = [0] * len(trForgOrbs)
    trY = np.concatenate((trYGen, trYForg),axis=0)

    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    teY = np.concatenate((teYGen, teYForg),axis=0)
    

    print('Ajustando el SVC-RBF\n ')
    mRbf = svm.SVC()
    mRbf.fit(trX,trY)
    print('Ajustando el SVC-L\n ')
    mLinear = svm.LinearSVC()
    mLinear.fit(trX,trY)
    print('Ajustando el Random Forest\n ')
    rFrst = RandomForestClassifier(max_depth=2, random_state=0)
    rFrst.fit(trX, trY)
    print('Ajustando el k-NN (N=3)\n ')
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(trX, trY) 

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


    
    joblib.dump(mRbf,args.path  + 'rbfSVC.pkl')    
    joblib.dump(mLinear,args.path  + 'lSVC.pkl')
    joblib.dump(rFrst,args.path  + 'rForest.pkl')        
    joblib.dump(neigh,args.path  + 'kNN.pkl')
    model.save(args.path  + 'mlp.h5')
            

    