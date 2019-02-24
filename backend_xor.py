import cv2
import numpy as np
import pbcvt
import characteristicsExtractor as ce
import math
from skimage.feature import *
from sklearn.metrics.pairwise import chi2_kernel
from sklearn.externals import joblib
import time
from keras.models import load_model
import json
def getDistance(boundPoints,genPoints):
    totalDistance = 0
    for numPoint,point in enumerate(genPoints):
        totalDistance += (point[0]-boundPoints[numPoint][0]) **2 + (point[1] - boundPoints[numPoint][1])**2
    return math.sqrt(totalDistance)

def applyMorphology(img):
    img = cv2.erode(img, np.ones((3,3),np.uint8),iterations =1)
    erosionR = cv2.erode(img,np.ones((6,6),np.uint8),iterations = 1)
    erosionG = cv2.erode(erosionR,np.ones((10,10),np.uint8),iterations = 1)
    erosionB = cv2.erode(erosionG,np.ones((16,16),np.uint8),iterations = 1 )
    diff1 = cv2.bitwise_not(cv2.subtract(img,erosionR))
    diff2 = cv2.bitwise_not(cv2.subtract(erosionR,erosionG))
    diff3 = cv2.bitwise_not(cv2.subtract(erosionG, erosionB))
    diff1[np.where((diff1 == [0,0,0]).all(axis = 2))] = [0,0,255]
    diff2[np.where((diff2 == [0,0,0]).all(axis = 2))] = [0,255,0]
    diff3[np.where((diff3 == [0,0,0]).all(axis = 2))] = [255,0,0]
    res = cv2.bitwise_and(diff1,img)
    res = cv2.bitwise_and(res,diff2)
    res = cv2.bitwise_and(diff3,res)
    res[np.where((res==[255,255,255]).all(axis = 2))]= [96,100,0]
    return res

def xOr_Images(imgG,imgQ,centered):
    imgGt = pbcvt.applyThinning(imgG)
    imgQt = pbcvt.applyThinning(imgQ)
    imgGm = applyMorphology(cv2.copyMakeBorder(imgGt,16,16,16,16,cv2.BORDER_CONSTANT,None,[255,255,255]))
    cmImgG = ce.centerOfMass(cv2.copyMakeBorder(imgGt,16,16,16,16,cv2.BORDER_CONSTANT,None,[255,255,255]))
    cmImgQ = ce.centerOfMass(imgQt)
    cv2.imwrite('imgGm.png',imgGm)
    cv2.imwrite('imgQt.png',imgQt)
    d = (int(round(cmImgG[0]-cmImgQ[0])),int(round(cmImgG[1]-cmImgQ[1])))
    tb = 0
    lr = 0
    if(d[0]>0 ):
        tb = (0,d[0])
    else:
        tb = (abs(d[0]),0)
    if(d[1]>0):
        lr = (0,d[1])
    else:
        lr = (abs(d[1]),0)
    if(centered):    
        imgQt = cv2.copyMakeBorder(imgQt,tb[0],tb[1],lr[0],lr[1],cv2.BORDER_CONSTANT,None,[255,255,255])
    h1,w1 = imgGm.shape[:2]
    h2,w2 = imgQt.shape[:2]
    hResize = max(h1,h2)
    wResize = max(w1,w2)

    if(hResize - h1 !=0):
        if((hResize-h1)%2 == 0):
            imgGm = cv2.copyMakeBorder(imgGm,(hResize - h1)//2,(hResize - h1)//2,0,0,cv2.BORDER_CONSTANT,None,[96,100,0])
        else:
            imgGm = cv2.copyMakeBorder(imgGm,(hResize-h1)//2+1,(hResize-h1)//2,0,0,cv2.BORDER_CONSTANT,None,[96,100,0])
    if (hResize-h2 != 0 ):
        if((hResize-h2)%2 == 0 ):
            imgQt = cv2.copyMakeBorder(imgQt,(hResize-h2)//2,(hResize-h2)//2,0,0,cv2.BORDER_CONSTANT,None,[255,255,255] )
        else:
            imgQt = cv2.copyMakeBorder(imgQt,(hResize-h2)//2+1,(hResize-h2)//2,0,0,cv2.BORDER_CONSTANT,None,[255,255,255])
    if(wResize -w1 != 0):
        if((wResize - w1)%2 == 0):
            imgGm = cv2.copyMakeBorder(imgGm,0,0,(wResize-w1)//2,(wResize-w1)//2,cv2.BORDER_CONSTANT,None,[96,100,0])
        else:
            imgGm = cv2.copyMakeBorder(imgGm,0,0,(wResize-w1)//2+1,(wResize-w1)//2,cv2.BORDER_CONSTANT,None,[96,100,0])
    if(wResize - w2 !=0):
        if((wResize-w2)%2 ==0):
            imgQt = cv2.copyMakeBorder(imgQt,0,0,(wResize - w2)//2,(wResize - w2)//2,cv2.BORDER_CONSTANT,None,[255,255,255])
        else:
            imgQt = cv2.copyMakeBorder(imgQt,0,0,(wResize - w2)//2 +1, (wResize - w2) //2, cv2.BORDER_CONSTANT,None,[255,255,255])
    ##imgQt = cv2.cvtColor(imgQt,cv2.COLOR_GRAY2BGR)
    res = cv2.bitwise_xor(imgGm,imgQt)
    
    resVector = pbcvt.countColors(res)
    return list(resVector) + [res]

def getRatio(fc,sc):
    return abs(fc-sc) / ((fc+sc)/2)

def imageCharacteritics(imgG,imgQ):

    Gc=[ ce.centerOfMass(imgG), ce.occupancyRatio(imgG), ce.aspectRatio(imgG), ce.densityRatio(imgG), ce.harrisCorners(cv2.cvtColor(imgG,cv2.COLOR_BGR2GRAY)) ]
    Qc=[ ce.centerOfMass(imgQ), ce.occupancyRatio(imgQ), ce.aspectRatio(imgQ), ce.densityRatio(imgQ), ce.harrisCorners(cv2.cvtColor(imgQ,cv2.COLOR_BGR2GRAY))]
    return [math.sqrt((Gc[0][0]-Qc[0][0])**2 + (Gc[0][1]-Qc[0][1])**2),getRatio(Gc[1],Qc[1]),getRatio(Gc[2],Qc[2]),getRatio(Gc[3],Qc[3]),getRatio(Gc[4],Qc[4])]

def HoGLBP(points,image,windowSize):
    pointsHoGHistograms = []
    pointsLBPHistograms = []
    imageSurroundingPointsH = []
    imageSurroundingPointsV = []
    image = cv2.copyMakeBorder(image,windowSize,windowSize,windowSize,windowSize,cv2.BORDER_CONSTANT,None,[255,255,255])

    for it,i in enumerate(points[0]):
            imageSurroundingPointsH.append(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize])
            h = hog(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize],orientations=8, pixels_per_cell=(windowSize//2, windowSize//2),cells_per_block=(1, 1),multichannel=False)
            h2 = [(h[i]+ h[i+8] +h[i+16]+h[i+24])/4 for i in range(0,8) ]
            lbp = local_binary_pattern(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize],8,1,'uniform')
            lbp = np.histogram(lbp,bins=np.arange(0,11),range=(0,10))[0].astype('float')
            lbp /= sum(lbp) 
            pointsHoGHistograms = np.concatenate((pointsHoGHistograms,h2,h), axis = 0)
            pointsLBPHistograms = np.concatenate((pointsLBPHistograms,lbp),axis = 0)
    
    for it,i in enumerate(points[1]):
            imageSurroundingPointsV.append(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize])
            h = hog(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize],orientations=8, pixels_per_cell=(windowSize//2,windowSize//2),cells_per_block=(1, 1),multichannel=False)
            h2 = [(h[i]+ h[i+8] +h[i+16]+h[i+24])/4 for i in range(0,8) ]
            lbp = local_binary_pattern(image[i[0]:i[0]+windowSize,i[1]:i[1]+windowSize],8,1,'uniform')
            lbp = np.histogram(lbp,bins=np.arange(0,11),range=(0,10))[0].astype('float')
            lbp /= sum(lbp) 
            pointsHoGHistograms = np.concatenate((pointsHoGHistograms,h2,h), axis = 0)
            pointsLBPHistograms = np.concatenate((pointsLBPHistograms,lbp),axis = 0)
    return {"HoG":np.concatenate((pointsHoGHistograms,pointsLBPHistograms),axis = 0).tolist(),"imageSurroundingPointsH":imageSurroundingPointsH,"imageSurroundingPointsV":imageSurroundingPointsV}



def chi2Vector(imgG,imgQ,windowSize):
    hImgG = ce.horizontalS2(imgG,0,imgG.shape[1],0,imgG.shape[0],4)
    vImgG = ce.verticalS2(imgG,0,imgG.shape[1],0,imgG.shape[0],4)        
    hImgQ = ce.horizontalS2(imgQ,0,imgQ.shape[1],0,imgQ.shape[0],4)
    vImgQ = ce.verticalS2(imgQ,0,imgQ.shape[1],0,imgQ.shape[0],4)            

    histG = HoGLBP([hImgG,vImgG],imgG,windowSize)
    histQ = HoGLBP([hImgQ,vImgQ],imgQ,windowSize)

    fFHoG = histG["HoG"][:1200]
    fFLBP = histG["HoG"][1200:]
    sFHoG = histQ["HoG"][:1200]
    sFLBP = histQ["HoG"][1200:]
    
    HoG_chi2 = [chi2_kernel([fFHoG[i*8:(i+1)*8]],[sFHoG[i*8:(i+1)*8 ]]).ravel()[0] for i in range (0,150) ]
    LBP_chi2 = [chi2_kernel([fFLBP[i*10:(i+1)*10]],[sFLBP[i*10:(i+1)*10 ]]).ravel()[0] for i in range (0,30) ]
    t1H = np.concatenate(histG["imageSurroundingPointsH"],axis = 1)
    t2H = np.concatenate(histQ["imageSurroundingPointsH"],axis = 1)
    tH = np.concatenate((t1H,t2H),axis = 0)
    t1V = np.concatenate(histG["imageSurroundingPointsV"],axis = 1)
    t2V = np.concatenate(histQ["imageSurroundingPointsV"],axis = 1)
    tV = np.concatenate((t1V,t2V),axis = 0)
    tT = np.concatenate((tH,tV),axis = 0)
    
    return {"chi2_vector":np.concatenate((HoG_chi2,LBP_chi2),axis = 0).tolist(),"combined_image":tT}

def getPrediction(vector,pathToModel):
    results = {}   
    
    mRbf = joblib.load(pathToModel  + 'rbfSVC.pkl')    
    results['SVC-RBF'] = mRbf.predict(vector).tolist()
    
    mLinear = joblib.load(pathToModel  + 'lSVC.pkl')
    results['SVC-L'] = mLinear.predict(vector).tolist()
    
    rFrst =joblib.load(pathToModel  + 'rForest.pkl')        
    results['rForest'] = rFrst.predict(vector).tolist()
    
    neigh = joblib.load(pathToModel  + 'kNN.pkl')
    results['k-NN'] = neigh.predict(vector).tolist()
   
    model = load_model(pathToModel  + 'mlp.h5')
    results['mlp'] = model.predict(np.array(vector)).tolist()
    
  
    
    return results
    
    
def testSignature(sigG,sigQ,paths,params):
    vectorXor = xOr_Images(cv2.cvtColor(sigG,cv2.COLOR_GRAY2BGR),cv2.cvtColor(sigQ,cv2.COLOR_GRAY2BGR),params[0] )
    imgChars = imageCharacteritics(cv2.cvtColor(sigG,cv2.COLOR_GRAY2BGR),cv2.cvtColor(sigQ,cv2.COLOR_GRAY2BGR))
    xOrVector = vectorXor[:10]  + imgChars
    HoGVector = chi2Vector(sigG,sigQ,params[1])
    return [getPrediction([xOrVector],paths[0]),getPrediction([HoGVector["chi2_vector"]],paths[1]),getPrediction([HoGVector["chi2_vector"][:180]+xOrVector],paths[2]),imgChars,vectorXor[10],HoGVector['combined_image']]

def testSignatureEuclidean(sigQ,paths,user):
    bounds = json.load(open(paths))
    hImgQ = ce.horizontalS2(sigQ,0,sigQ.shape[1],0,sigQ.shape[0],5)
    vImgQ = ce.verticalS2(sigQ,0,sigQ.shape[1],0,sigQ.shape[0],5) 
    print(paths)
    resForg18 = (getDistance(bounds[user]['vertical'][0], vImgQ) <= bounds[user]['vertical'][1]) and (getDistance(bounds[user]['horizontal'][0], hImgQ) <= bounds[user]['horizontal'][1]) 
    return int(resForg18)
