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

def modelAccuraccy(vec,toTest):
    count = 0
    for i in vec:
        if (i==toTest):
            count +=1
    return (count/len(vec))

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

    samplesB = np.random.choice(100,100,False).tolist()
    samplesH = np.random.choice(160,160,False).tolist()
    samplesC = np.random.choice(55,55,False).tolist()
    
    trGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1) in samplesB[:int(0.75*100)] ]
    trGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2) in samplesH[:int(0.75*160)] ]
    trGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3) in samplesC[:int(0.75*55)] ]
    print('Training orbs gen ',len(trGenOrbsB),' ',len(trGenOrbsH),' ',len(trGenOrbsC))

    trForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1)in samplesB[:int(0.75*100)] ]
    trForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2)in samplesH[:int(0.75*160)] ]
    trForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3)in samplesC[:int(0.75*55)] ]
    print('Training orbs forg ',len(trForgOrbsB),' ',len(trForgOrbsH),' ',len(trForgOrbsC))
    
    trX = np.concatenate((trGenOrbsB, trGenOrbsH, trGenOrbsC, trForgOrbsB, trForgOrbsH, trForgOrbsC),axis = 0)
    pca = PCA(n_components = 10)
    pca.fit(trX)
    trX = pca.transform(trX)    
    joblib.dump(pca,open(args.path+'pca2222.pkl','wb'))
    trYGen = [1] * ( len(trGenOrbsB) + len(trGenOrbsH) + len(trGenOrbsC))
    trYForg = [0] * (len(trForgOrbsB) + len(trForgOrbsH) + len(trForgOrbsC))
    trY = np.concatenate((trYGen, trYForg),axis=0)
    
    trGenOrbsB = None
    trGenOrbsH = None 
    trGenOrbsC = None 
    trForgOrbsB = None
    trForgOrbsH = None
    trForgOrbsC = None


    teGenOrbsB = [genuinePairsBLBPHoG[i]+genuinePairsB[i] for i in genuinePairsBLBPHoG if getUser(i,1) in samplesB[int(0.75*100):] ]
    teGenOrbsH = [genuinePairsHLBPHoG[i]+genuinePairsH[i] for i in genuinePairsHLBPHoG if getUser(i,2) in samplesH[int(0.75*160):] ]
    teGenOrbsC = [genuinePairsCLBPHoG[i]+genuinePairsC[i] for i in genuinePairsCLBPHoG if getUser(i,3) in samplesC[int(0.75*55):] ]
    print('Test orbs gen ', len(teGenOrbsB),' ',len(teGenOrbsH),' ',len(teGenOrbsC))

    teForgOrbsB = [forgeriesPairsBLBPHoG[i]+forgeriesPairsB[i] for i in forgeriesPairsBLBPHoG if getUserF(i,1) in samplesB[int(0.75*100):] ]
    teForgOrbsH = [forgeriesPairsHLBPHoG[i]+forgeriesPairsH[i] for i in forgeriesPairsHLBPHoG if getUserF(i,2) in samplesH[int(0.75*160):] ]
    teForgOrbsC = [forgeriesPairsCLBPHoG[i]+forgeriesPairsC[i] for i in forgeriesPairsCLBPHoG if getUserF(i,3) in samplesC[int(0.75*55):] ]
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

  
    teGenOrbs = pca.transform(np.concatenate((teGenOrbsB,teGenOrbsH,teGenOrbsC),axis=0))
    teForgOrbs = pca.transform(np.concatenate((teForgOrbsB,teForgOrbsH,teForgOrbsC),axis=0))
    teYGen = [1] * len(teGenOrbs)
    teYForg = [0] * len(teForgOrbs)
    
    
        
    results = {}
    
    
    print('Ajustando el Random Forest\n ')
    
    rFrst = RandomForestClassifier(max_depth=9, random_state=0)
    rFrst.fit(trX, trY)
    genOrbsVal = rFrst.predict(teGenOrbs)
    forgOrbsVal = rFrst.predict(teForgOrbs)
    results['rForest'+str(it)]=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print((1-modelAccuraccy(genOrbsVal,1))+ (1- modelAccuraccy(forgOrbsVal,0)))
    rFrst = None
    
    
    
    print('Ajustando el k-NN (N=3)\n ')
    
    neigh = KNeighborsClassifier(n_neighbors=29,n_jobs=4)
    neigh.fit(trX, trY) 
    genOrbsVal = neigh.predict(teGenOrbs)
    forgOrbsVal = neigh.predict(teForgOrbs)
    results['kNN'+str(it)]=[modelAccuraccy(genOrbsVal,1), modelAccuraccy(forgOrbsVal,0)]
    print((1-modelAccuraccy(genOrbsVal,1))+ (1- modelAccuraccy(forgOrbsVal,0)))
    neigh = None
    json.dump(results,open(args.path+'results4','w+' ))

            

    