from characteristicsExtractor import *
import json 
import os.path

def euclideanCentroids(route,fileName):
    
    img = cv2.imread(route+fileName[0:-1],1)
    height,width = img.shape[0:2]
    vPoints = verticalS2(img,0,width,0,height,5)
    hPoints = horizontalS2(img,0,width,0,height,5)
    data = {}
    if(os.path.isfile(route+fileName[:3]+".json")):
        with open(route+fileName[:3]+".json") as f:
            data = json.load(f)
    
    a_dict = { str(int(fileName[-7:-5])):{'vPoints': vPoints,'hPoints': hPoints } }
    data.update(a_dict)

    with open(route+fileName[:3]+".json", 'w') as f:
        json.dump(data, f)
     
    


    ##with open( route+fileName[:3]+".txt", "a") as charFile:
      ##  charFile.write('vPoints_'+fileName[-7:-5]+'\n')
        ##for i in range(len(vPoints)):
          ##  charFile.write(str(vPoints[i][0])+" "+str(vPoints[i][1])+" ")
        ##charFile.write('\n' + 'hPoints_'+fileName[-7:-5]+'\n')
        ##for i in range(len(hPoints)):
          ##  charFile.write(str(hPoints[i][0])+" "+str(hPoints[i][1]) + " ")
        ##charFile.write('\n' )


route = 'BHSig260/Hindi/'
with open(route + 'list.genuine') as f:
    for i in range(300):
        line=f.readline()
        euclideanCentroids(route,line)
    
    