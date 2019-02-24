import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, exposure
import cv2
import json
import os
def pHoG(route,fileName):
    
    image = cv2.imread(route+fileName[0:-1],1)
    
    ##image = data.astronaut()
    ##for division in divs:
    fd = hog(image, orientations=8, pixels_per_cell=(32, 32),
                            cells_per_block=(1, 1), visualize=False, multichannel=True)

    data = {}
    print("fd",fd)
    if(os.path.isfile(route+fileName[:3]+"HoG.json")):
        with open(route+fileName[:3]+"HoG.json") as f:
            data = json.load(f)
    fd = fd.tolist()
    
    a_dict = { str(int(fileName[-7:-5])):{'HoG_Vector': fd} }
    data.update(a_dict)

    with open(route+fileName[:3]+"HoG.json", 'w') as f:
        json.dump(data, f)
     
        
    ##fig, (ax1, ax2,ax3,ax4) = plt.subplots(1, 4, figsize=(8, 4), sharex=True, sharey=True)

    ##ax1.axis('off')
    ##ax1.imshow(image, cmap=plt.cm.gray)
    ##ax1.set_title('Input image')

    # Rescale histogram for better display
    ##hog_image_rescaled1 = exposure.rescale_intensity(hog_image[0], in_range=(0, 10))
    ##hog_image_rescaled2 = exposure.rescale_intensity(hog_image[1], in_range=(0, 10))
    ##hog_image_rescaled3 = exposure.rescale_intensity(hog_image[2], in_range=(0, 10))


    ##ax2.axis('off')
    ##ax2.imshow(hog_image_rescaled1, cmap=plt.cm.gray)
    ##ax3.imshow(hog_image_rescaled2, cmap=plt.cm.gray)
    ##ax4.imshow(hog_image_rescaled3, cmap=plt.cm.gray)
    ##ax2.set_title('Histogram of Oriented Gradients')
    ##ax3.set_title('Histogram of Oriented Gradients')
    ##ax4.set_title('Histogram of Oriented Gradients')
    ##plt.show()




route = 'BHSig260/Hindi/'
with open(route + 'list.genuine') as f:
    count = 0
    total = 3840
    for line in f:
        if (count % 38 == 0 ):
            print("va", count / total * 100,"%")
        pHoG(route,line)
        count += 1

with open(route + 'list.forgery') as f:
    count = 0
    total = 4800
    for line in f:
        if (count % 48 == 0 ):
            print("va", count / total * 100,"%")    
        pHoG(route,line)
        count += 1