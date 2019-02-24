import sklearn
import json
import re
import numpy as np
from sklearn import svm
import argparse
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
def getUser(x):
    a = re.search('C-S-(.+?)-G.',x)
    return(int(a.group(1)))

def getUserF(x):
    a = re.search('C-S-(.+?)-F.',x)
    return(int(a.group(1)))
genuinePairs = json.load(open('signatures/gengenVectors'))
forgeriesPairs = json.load(open('signatures/forgenVectors'))
b = [genuinePairs[i] for i in genuinePairs if getUser(i)< 55*0.75]
c = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i)< 55*0.75 ]
X = np.concatenate((b,c),axis = 0)
yg = [1] * len(b)
yf = [0] * len(c)
Y = np.concatenate((yg,yf),axis=0)
bT = [genuinePairs[i] for i in genuinePairs if getUser(i)> 55*0.75]
cT = [forgeriesPairs[i] for i in forgeriesPairs if getUserF(i)> 55*0.75 ]
Xt = np.concatenate((bT,cT),axis = 0)
ygT = [1] * len(bT)
yfT = [0] * len(cT)
Yt = np.concatenate((ygT,yfT),axis=0)
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
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])



y_train = keras.utils.to_categorical(y_train, num_classes)
num_classes = 10
y_train = keras.utils.to_categorical(y_train, num_classes)
y_train
Y = keras.utils.to_categorical(Y, 2)
Y
Yt = keras.utils.to_categorical(Yt, 2)
epochs = 20
batch_size = 128
history = model.fit(X, Y,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(Xt, Yt))
score = model.evaluate(Xt, Yt, verbose=0)
score[1]
model.predict(Xt)
epochs = 128
history = model.fit(X, Y,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(Xt, Yt))
score = model.evaluate(Xt, Yt, verbose=0)
score[1]
ygT = keras.utils.to_categorical(ygT, 2)
score = model.evaluate(bT, ygT, verbose=0)
bT
ygT
len(bT)
len(ygT)
score = model.evaluate(bT, ygT, verbose=0)
X[0]
bT[0]
bT= np.concatenate(bT,[],axis=0)
bT= np.concatenate((bT,[]),axis=0)
bT= np.array(bT)
bT
ygT
score = model.evaluate(bT, ygT, verbose=0)
score[1]
1 - score[1]
%history -f kerasTest.py
