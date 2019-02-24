import cv2
def applyThiningProcedure(img,x,y,even):
    change = False
    if ( (img[y][x]==[255,255,255]).all()):
        return False
    if (even):
        if(firstCondition(x,y,img) and secondCondition(x,y,img) and evenThirdFourthCondition(x,y,img)):
            
            img[y][x] = [255,255,255]
            change = True
            
    else:
        if(firstCondition(x,y,img) and secondCondition(x,y,img) and unevenThirdFourthCondition(x,y,img)):
            
            img[y][x] = [255,255,255]
            change = True
            
    return change

def zhThinning(route):
    
    try:
        img = cv2.imread(route,1)
        changes = 1
        height,width = img.shape[:2]
        img2 = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_CONSTANT,None, [255,255,255])
        while(changes > 0):
            changes = 0
            for even in [False,True]:
                for y in range(0,height):
                    for x in range(0,width):
                        
                        if (applyThiningProcedure(img2,x,y,even)):
                            changes += 1 
        cv2.imwrite(route[:-4]+'_t.tif',img2)    
        return route[:-4]+'_t.tif'       
    except Exception as exception:
        print(route,exception)


patternArray= [0,0,0]
backgroundArray = [255,255,255]
points= { 
    'p2':(-1,0),
    'p3':(-1,1),
    'p4':(0,1), 
    'p5': (1,1),
    'p6': (1,0),
    'p7':(1,-1),
    'p8':(0,-1),
    'p9':(-1,-1)  
    }

def getPositiveNeighbors(x,y,img):
    numPN = 0
    for i in range (-1,2):
        for z in range (-1,2):
            if(i==0 and z==0):
                continue
            if ( (img[y+i][x+z]==patternArray).all() ) :
                numPN+=1 
         
    return numPN

def firstCondition(x,y,img):
    if (2 <= getPositiveNeighbors(x,y,img) <= 6):
        
        return True
    return False

def secondCondition(x,y,img):
    numberTransitions = 0
    
    if ((img[y + points['p9'][0]][ x+points['p9'][1] ]==backgroundArray).all() and (img[y + points['p2'][0] ][ x + points['p2'][1]]==patternArray).all() ): ##p9-p2
        numberTransitions+=1
    
    if ((img[y + points['p2'][0] ][ x + points['p2'][1]]==backgroundArray).all() and (img[y + points['p3'][0] ][ x + points['p3'][1]]==patternArray).all() ): ##p2-p3
        numberTransitions+=1
    
    if ((img[y + points['p3'][0] ][ x + points['p3'][1]]==backgroundArray).all() and (img[y + points['p4'][0] ][ x + points['p4'][1]]==patternArray).all() ): ##p3-p4
        numberTransitions+=1

    if ((img[y + points['p4'][0] ][ x + points['p4'][1]]==backgroundArray).all() and (img[y + points['p5'][0] ][ x + points['p5'][1]]==patternArray).all() ): ##p4-p5
        numberTransitions+=1

    if ((img[y + points['p5'][0] ][ x + points['p5'][1]]==backgroundArray).all() and (img[y + points['p6'][0] ][ x + points['p6'][1]]==patternArray).all() ): ##p5-p6
        numberTransitions+=1

    if ((img[y + points['p6'][0] ][ x + points['p6'][1]]==backgroundArray).all() and (img[y + points['p7'][0] ][ x + points['p7'][1]]==patternArray).all() ): ##p6-p7
        numberTransitions+=1

    if ((img[y + points['p7'][0] ][ x + points['p7'][1]]==backgroundArray).all() and (img[y + points['p8'][0] ][ x + points['p8'][1]]==patternArray).all() ): ##p7-p8
        numberTransitions+=1

    if ((img[y + points['p8'][0] ][ x + points['p8'][1]]==backgroundArray).all() and (img[y + points['p9'][0] ][ x + points['p9'][1]]==patternArray).all() ): ##p9
        numberTransitions+=1
        
    return (numberTransitions==1)
        
        

def unevenThirdFourthCondition(x,y,img):
    ##thirdCond = int(img[y + points['p2'][0] ][ x + points['p2'][1]][0]) * int(img[y + points['p4'][0] ][ x + points['p4'][1]][0]) * int(img[y + points['p6'][0] ][ x + points['p6'][1]][0])
    thirdCond = (img[y + points['p2'][0] ][ x + points['p2'][1]][0]==backgroundArray).all() or (img[y + points['p4'][0] ][ x + points['p4'][1]]==backgroundArray ).all() or (img[y + points['p6'][0] ][ x + points['p6'][1]]==backgroundArray).all()
    ##fourthCond = int(img[y + points['p4'][0] ][ x + points['p4'][1]][0]) * int(img[y + points['p6'][0] ][ x + points['p6'][1]][0]) * int(img[y + points['p8'][0] ][ x + points['p8'][1]][0])
    fourthCond = (img[y + points['p4'][0] ][ x + points['p4'][1]][0]==backgroundArray).all() or (img[y + points['p6'][0] ][ x + points['p6'][1]]==backgroundArray ).all() or (img[y + points['p8'][0] ][ x + points['p8'][1]]==backgroundArray).all()
    return ( thirdCond and fourthCond )

def evenThirdFourthCondition(x,y,img):
    #thirdCond = int(img[y + points['p2'][0] ][ x + points['p2'][1]][0]) * int(img[y + points['p4'][0] ][ x + points['p4'][1]][0]) * int(img[y + points['p8'][0] ][ x + points['p8'][1]][0])
    #fourthCond = int(img[y + points['p2'][0] ][ x + points['p2'][1]][0]) * int(img[y + points['p6'][0] ][ x + points['p6'][1]][0]) * int(img[y + points['p8'][0] ][ x + points['p8'][1]][0])
   
    thirdCond = (img[y + points['p2'][0] ][ x + points['p2'][1]][0]==backgroundArray).all() or (img[y + points['p4'][0] ][ x + points['p4'][1]]==backgroundArray ).all() or (img[y + points['p8'][0] ][ x + points['p8'][1]]==backgroundArray).all()
    ##fourthCond = int(img[y + points['p4'][0] ][ x + points['p4'][1]][0]) * int(img[y + points['p6'][0] ][ x + points['p6'][1]][0]) * int(img[y + points['p8'][0] ][ x + points['p8'][1]][0])
    fourthCond = (img[y + points['p2'][0] ][ x + points['p2'][1]][0]==backgroundArray).all() or (img[y + points['p6'][0] ][ x + points['p6'][1]]==backgroundArray ).all() or (img[y + points['p8'][0] ][ x + points['p8'][1]]==backgroundArray).all()
   
    return ( thirdCond and fourthCond )