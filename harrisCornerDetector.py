import cv2
import numpy as np 


np.set_printoptions(threshold=np.inf)
def getVariance(mat):
    a = np.sqrt(sum(sum(np.square(mat)))/(len(mat)*len(mat[0])) - np.square(sum(sum(mat))/(len(mat)*len(mat[0])) ) )
    print (a)
    return a

def getCorners(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst> 0.5*dst.max()  ]=[0,0,255]
    print(len(img[dst>= (sum(sum(dst))/(len(dst)*len(dst[0])) + 10*getVariance(dst) )  ]))

    ##print("thing", sum(sum(dst))/(len(dst)*len(dst[0]) ) )
    return img

route = 'BHSig260/Hindi/010/H-S-10-F-01.tif'
img = cv2.imread(route,1)
img = getCorners(img)
cv2.imshow('result',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

