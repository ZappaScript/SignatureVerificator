import sklearn
import json
import re
import numpy as np
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier 
import keras
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import argparse
from sklearn.externals import joblib

import os
if __name__ == "__main__":
    orbsJson = json.load(open('Modelo_Global_Combinado/boostTestingData.json'))
    b = []                           
    for i in orbsJson:                                                                                                                                   
        b.append(orbsJson[i]['genuineOrbs'])

    allGenuineOrbs = []
    allForgeryOrbs = []

    for y in range(len(b[0])):     
        c = []                 
        for x in range(len(b)):      
            if x == 5:
                c.append(b[x][y][0])
                c.append(b[x][y][1])
            else:
                c.append(b[x][y])
        allGenuineOrbs.append(c)
    trYGen = [1]*len(allGenuineOrbs)


    b = []                                                                                                                                        
    for i in orbsJson:                                                                                                                                   
        b.append(orbsJson[i]['forgOrbs'])

    for y in range(len(b[0])):     
            
        c = []                 
                            
        for x in range(len(b)):      
            if x == 5:
                c.append(b[x][y][0])
                c.append(b[x][y][1])
            else:
                c.append(b[x][y])
        allForgeryOrbs.append(c)

    trYForg = [0]*len(allForgeryOrbs)

    trX = np.concatenate((allGenuineOrbs,allForgeryOrbs),axis = 0)
    trY = np.concatenate((trYGen,trYForg),axis = 0)
    print('Working as intended')
    BaggingC = joblib.load('Modelo_Global_Combinado/boostedBaggingModel.pkl')
    mlp=load_model('Modelo_Global_Combinado/ensenmble_mlp.h5')
    allGBag = BaggingC.predict(allGenuineOrbs)
    allForgBag = BaggingC.predict(allForgeryOrbs)
    print(sum(allGBag)/len(allGBag))
    print(1 - sum(allForgBag)/len(allForgBag))
    print(len(trX))
    #BaggingC = BaggingClassifier(svm.SVC(cache_size = 100), max_samples=1.0 / 10, n_estimators=10,n_jobs=-1)
    #BaggingC.fit(trX,trY)
    #joblib.dump(BaggingC,"Modelo_Global_Combinado/boostedBaggingModel.pkl")
    allGMLP = mlp.predict(np.array(allGenuineOrbs))
    allForgMLP = mlp.predict(np.array(allForgeryOrbs))
    print(sum(allGMLP)/len(allGMLP))
    print(1 - sum(allForgMLP)/len(allForgMLP))
    #trY = keras.utils.to_categorical(trY, 2)
    
    #print('Ajustando el MLP\n ')
    ##model = Sequential()
    ##model.add(Dense(7, activation='relu', input_shape=(len(trX[0]),)))
    ##model.add(Dropout(0.2))
    ##model.add(Dense(7, activation='relu'))
    ##model.add(Dropout(0.2))
    ##model.add(Dense(2, activation='softmax'))
    ##model.compile(loss='categorical_crossentropy', optimizer=RMSprop(), metrics=['accuracy'])
    ##history = model.fit(trX, trY,
    ##                batch_size=128,
    ##                epochs=128,
    ##                verbose=1
    ##                )

    