import cv2
import numpy as np
import characteristicsExtractor as ce
import os

def cropAndResize(img):
    ##imgF = cv2.imread(route+subroute1,1)
    ##imgG = cv2.imread(route+subroute2,1)


    bbImgF = np.where(img == 0 )
    cropImgF = img[min(bbImgF[0]):max(bbImgF[0]),min(bbImgF[1]):max(bbImgF[1])]
    ##res = cv2.resize(cropImgF,(500,200), interpolation = cv2.INTER_NEAREST)
    res = cv2.copyMakeBorder(cropImgF, 4, 4, 10, 10, cv2.BORDER_CONSTANT,None, [255,255,255]) 
    return res

def denoisingThinning(img):
    kernel2 = np.ones((3,3),np.uint8)
    img = cv2.dilate(img,kernel2,iterations=1)
    img = cv2.erode(img,kernel2,iterations=1)
    img = cv2.GaussianBlur(img,(5,5),0)
    return img

def treshAndDim(img):
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    bbImgF = np.where(img == 0)
    dim = (min(bbImgF[0]),max(bbImgF[0]),min(bbImgF[1]),max(bbImgF[1]))
    return (img,dim)
    


def applyMorphology(route):
    
    img1 = cv2.imread(route[0:-1],0)
    img2 = cv2.imread(route[0:-1],0)
    kernel = np.ones((5,5),np.uint8)
    img2 = denoisingThinning(img2)
    aux = treshAndDim(img2)
    dims = aux[1]
    
    img1 = img1[dims[0]-3:dims[1]+3,dims[2]-3:dims[3]+3]
    img1 = cropAndResize(img1)
    cv2.imwrite(route[0:-5]+'.tif',img1)
    ##os.remove(route[0:-5]+'-for_fix.png')
    

   




route = 'BHSig260FIX/Bengali/'

with open(route + 'list.forgery') as f:
    count = 0
    total = 3000
    ##lines = f.readlines()[ :(1+30*115)]
    for line in f:
        if (count % 30 == 0 ):
            print(count / total)    
        applyMorphology(route+line)
        
        count +=1
    
    

with open(route + 'list.forgery') as f:
    count = 0
    total = 4800
    lines = f.readlines()[ (1+30*117):]
    for line in lines:
        if (count % 48 == 0 ):
            print(count / total)    
        applyMorphology(route+line)
        
        count +=1

    ##for line in f:
        ##print(line)
      ##  applyMorphology(route+line)