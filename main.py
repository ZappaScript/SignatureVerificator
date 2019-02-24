import cv2
import numpy as np
import characteristicsExtractor as ce

def cropAndResize(img):
    ##imgF = cv2.imread(route+subroute1,1)
    ##imgG = cv2.imread(route+subroute2,1)


    bbImgF = np.where((img == [0,0,0]).all(axis = 2))
    cropImgF = img[min(bbImgF[0]):max(bbImgF[0]),min(bbImgF[1]):max(bbImgF[1])]
    res = cv2.resize(cropImgF,(500,200), interpolation = cv2.INTER_NEAREST)
    res = cv2.copyMakeBorder(res, 8, 8, 20, 20, cv2.BORDER_CONSTANT,None, [255,255,255]) 
    return res

def denoisingThinning(img):
    kernel2 = np.ones((2,2),np.uint8)
    img = cv2.dilate(img,kernel2,iterations=1)
    img = cv2.erode(img,kernel2,iterations=1)
    return img



    


def applyMorphology(route):
    ##print(route)
    img = cv2.imread(route[0:-1],1)
    ##print(len(route))
    ##cv2.imshow("image",img)
    kernel = np.ones((5,5),np.uint8)
    img = cv2.copyMakeBorder(img, 8, 8, 20, 20, cv2.BORDER_CONSTANT,None, [255,255,255])
    ##img = denoisingThinning(img)
    ##img = cropAndResize(img)
    erosionR = cv2.erode(img,kernel,iterations = 1)
    erosionG = cv2.erode(erosionR,kernel,iterations = 1)
    erosionB = cv2.erode(erosionG,kernel,iterations = 1)
    diff1 = cv2.bitwise_not(cv2.subtract(img,erosionR))
    diff2 = cv2.bitwise_not(cv2.subtract(erosionR,erosionG))
    diff3 = cv2.bitwise_not(cv2.subtract(erosionG,erosionB))
    diff1[np.where((diff1 == [0,0,0]).all(axis = 2))] = [0,0,255]
    diff2[np.where((diff2 == [0,0,0]).all(axis = 2))] = [0,255,0]
    diff3[np.where((diff3 == [0,0,0]).all(axis = 2))] = [255,0,0]
    res = cv2.bitwise_and(diff1,img)
    res = cv2.bitwise_and(res,diff2)
    res = cv2.bitwise_and(diff3,res)
    res[np.where((res == [255,255,255]).all(axis = 2))] = [96,100,0]
    b_channel, g_channel, r_channel = cv2.split(res)
    ##alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
    ##img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    
    cv2.imwrite(route[0:-5]+'-for_fix.png',res)

   



route = 'BHSig260FIX/Bengali/'
with open(route + 'list.genuine') as f:
    count = 0
    total = 2400
    for line in f:
        if (count % 24 == 0 ):
            print(count / total)
        applyMorphology(route+line)
        count += 1

