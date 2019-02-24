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
from keras.layers import Dense, Dropout, MaxPooling1D, Convolution1D, Flatten
from keras.optimizers import RMSprop
import argparse
from sklearn.externals import joblib
import time
from keras.layers.normalization import BatchNormalization
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
    genuinePairs = json.load(open(args.path+args.gengenVectors))
    forgeriesPairs = json.load(open(args.path+args.forgenVectors))


    trGenOrbs = [genuinePairs[i][:150] for i in genuinePairs if getUser(i,mode)<= int(args.numUsers)*0.75 ]
    trForgOrbs = [forgeriesPairs[i][:150] for i in forgeriesPairs if getUserF(i,mode)<= int(args.numUsers)*0.75 ]
    teGenOrbs = [genuinePairs[i][:150] for i in genuinePairs if getUser(i,mode)> int(args.numUsers)*0.75 ]
    teForgOrbs = [forgeriesPairs[i][:150] for i in forgeriesPairs if getUserF(i,mode)> int(args.numUsers)*0.75 ]

    trX = np.concatenate((trGenOrbs,trForgOrbs),axis = 0)
    teX = np.concatenate((teGenOrbs,teForgOrbs),axis = 0)

    trYGen = [1] * len(trGenOrbs)
    trYForg = [0] * len(trForgOrbs)
    trY = np.concatenate((trYGen, trYForg),axis=0)

    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    teY = np.concatenate((teYGen, teYForg),axis=0)
    
    
    trY = keras.utils.to_categorical(trY, 2)
    teY = keras.utils.to_categorical(teY, 2)

    datasetTr = np.reshape(trX,(-1,150,1))
    datasetTe = np.reshape(teX,(-1,150,1))
    print('Ajustando el MLP\n ')
    
    model = Sequential()
    model.add(Convolution1D(filters=5, kernel_size=5, activation="relu", input_shape=(150,1)))
    model.add(MaxPooling1D(strides=4))
    model.add(BatchNormalization())
    model.add(Convolution1D(filters=16, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(strides=4))
    model.add(BatchNormalization())
    model.add(Convolution1D(filters=32, kernel_size=5, activation='relu'))
    model.add(MaxPooling1D(strides=4))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    history = model.fit(datasetTr, trY,
                    batch_size=128,
                    epochs=128,
                    verbose=1,
                    validation_data=(datasetTe, teY))
    model.save(args.path  + 'mlp_hist2.h5')