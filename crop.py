import cv2
import numpy as np 

route = 'BHSig260/Hindi/010/'
subroute1 = 'H-S-10-F-01.tif'
subroute2 = 'H-S-10-G-01-M.png'

def cropAndResize(img):
    imgF = cv2.imread(route+subroute1,1)
    imgG = cv2.imread(route+subroute2,1)


bbImgF = np.where((imgF == [0,0,0]).all(axis = 2))
cropImgF = imgF[min(bbImgF[0]):max(bbImgF[0]),min(bbImgF[1]):max(bbImgF[1])]

res = cv2.resize(cropImgF,(500,200), interpolation = cv2.INTER_NEAREST)

cv2.imshow('result',res)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()