import cv2
import numpy as np
import characteristicsExtractor as ce
import os
import argparse

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
    ##img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    rt, img =  cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    bbImgF = np.where(img == 0)
    dim = (min(bbImgF[0]),max(bbImgF[0]),min(bbImgF[1]),max(bbImgF[1]))
    
    return (img,dim)
    


def applyCropDenoise(route):
    print(route[0:-1])
    
    img2 = cv2.imread(route[0:-1],0)
    kernel = np.ones((5,5),np.uint8)
    ##img2 = cv2.GaussianBlur(img2,(5,5),0)
    aux = treshAndDim(img2)
    
    dims = aux[1]
    
    img = cropAndResize(aux[0])
    ##img1 = cropAndResize(img1)
    cv2.imwrite(route[0:-5]+'.tif',img)
    ##os.remove(route[0:-5]+'-for_fix.png')
    

   



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("file")
    args = parser.parse_args()

with open(args.path + args.file) as f:
    count = 0
    total = 2400
    ##lines = f.readlines()[ :(1+24*124)]
    for line in f:
        if (count % 24 == 0 ):
            print(count / total)
        applyCropDenoise(args.path+line)
        ##os.remove(route+line[0:-5]+'-M.png')
        ##os.remove(route+line[0:-5]+'-M2.png')
        ##os.remove(route+line[0:-5]+'-for_fix.png')
        count += 1


    
    
    ##for line in f:
        ##print(line)
      ##  applyCropDenoise(route+line)