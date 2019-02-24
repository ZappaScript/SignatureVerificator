def getVotingClass(predictions):
                             
    classZero = 0
    classOne = 0
    for t in range(len(predictions)-1) :
        if t != 5:
            if predictions[t] == 0:
                classZero += 1
            if predictions[t] == 1:
                classOne += 1
        else:
            if(predictions[t]>predictions[t+1]):
                classZero += 1
            if(predictions[t+1]>predictions[t]):
                classOne += 1
    if(classZero > classOne ):
        return 0
    if(classZero < classOne):
        return 1
    if(classZero == classOne):
        return 0

b = []
for i in bTeData:                                                                                                                                   
    b.append(bTeData[i]['genuineOrbs'])
allGenuineOrbs = []
allForgeryOrbs = []

for y in range(len(b[0])):     
    c = []                 
    for x in range(len(b)):      
        if x == 5:
            c.append(b[x][y][0])
            c.append(b[x][y][1])
        else:
            c.append(b[x][y])
    allGenuineOrbs.append(c)
trYGen = [1]*len(allGenuineOrbs)


b = []                                                                                                                                        
for i in bTeData:                                                                                                                                   
    b.append(bTeData[i]['forgOrbs'])

for y in range(len(b[0])):     
        
    c = []                 
                        
    for x in range(len(b)):      
        if x == 5:
            c.append(b[x][y][0])
            c.append(b[x][y][1])
        else:
            c.append(b[x][y])
    allForgeryOrbs.append(c)

varSignatures = {}
gengenMorph = None
forgenMorph = None
gengenLBP32 = None
forgenLBP32 = None
gengenLBP64 = None
forgenLBP64 = None

for prefix in ["signatures/","BHSig260FIX/Bengali/","BHSig260FIX/Hindi/"]:
    gengenMorph = json.load(open(prefix+'Vectores_Característicos/gengenVectors'))
    forgenMorph = json.load(open(prefix+'Vectores_Característicos/forgenVectors'))
    gengenLBP32 = json.load(open(prefix+'Vectores_Característicos/gengenVectors.LBPHoG'))
    forgenLBP32 = json.load(open(prefix+'Vectores_Característicos/forgenVectors.LBPHoG'))
    gengenLBP64 = json.load(open(prefix+'Vectores_Característicos/gengenVectors.LBPHoG64'))
    forgenLBP64 = json.load(open(prefix+'Vectores_Característicos/forgenVectors.LBPHoG64'))

    gengenMorphChars = [ gengenMorph[x][:10] for x in gengenMorph]
    forgenMorphChars = [ forgenMorph[x][:10] for x in forgenMorph]
    gengenMorphGChars = [ gengenMorph[x][10:] for x in gengenMorph]
    forgenMorphGChars = [ forgenMorph[x][10:] for x in forgenMorph]
    gengenMorphTChars = [ gengenMorph[x] for x in gengenMorph]
    forgenMorphTChars = [ forgenMorph[x] for x in forgenMorph]


    gengenLBP32Chars = [ gengenLBP32[x][150:] for x in gengenLBP32]
    forgenLBP32Chars = [ forgenLBP32[x][150:] for x in forgenLBP32]
    gengenLBP64Chars = [ gengenLBP64[x][150:] for x in gengenLBP64]
    forgenLBP64Chars = [ forgenLBP64[x][150:] for x in forgenLBP64]

    gengenHoG32Chars = [ gengenLBP32[x][:150] for x in gengenLBP32]
    forgenHoG32Chars = [ forgenLBP32[x][:150] for x in forgenLBP32]
    gengenHoG64Chars = [ gengenLBP64[x][:150] for x in gengenLBP64]
    forgenHoG64Chars = [ forgenLBP64[x][:150] for x in forgenLBP64]

    gengenHL32Chars = [ gengenLBP32[x] for x in gengenLBP32]
    forgenHL32Chars = [ forgenLBP32[x] for x in forgenLBP32]
    gengenHL64Chars = [ gengenLBP64[x] for x in gengenLBP64]
    forgenHL64Chars = [ forgenLBP64[x] for x in forgenLBP64]

    varSignatures[prefix] = {"xOrVar_gengen":np.average(np.var(gengenMorphChars,axis=0) ),
    "xOrVar_forgen":np.average(np.var(forgenMorphChars,axis=0) ),
    "g_metrics_gengen":np.average(np.var(gengenMorphGChars,axis=0)),
    "g_metrics_forgen":np.average(np.var(forgenMorphGChars,axis=0)),
    "morph_gengen":np.average(np.var(gengenMorphTChars,axis=0)),
    "morph_forgen":np.average(np.var(forgenMorphTChars,axis=0)),
    "LBP32_gengen":np.average(np.var(gengenLBP32Chars,axis=0) ),
    "LBP32_forgen":np.average(np.var(forgenLBP32Chars,axis=0) ),
    "LBP64_gengen":np.average(np.var(gengenLBP64Chars,axis=0) ),
    "LBP64_forgen":np.average(np.var(forgenLBP64Chars,axis=0) ),
    "HoG32_gengen":np.average(np.var(gengenHoG32Chars,axis=0) ),
    "HoG32_forgen":np.average(np.var(forgenHoG32Chars,axis=0) ),
    "HoG64_gengen":np.average(np.var(gengenHoG64Chars,axis=0) ),
    "HoG64_forgen":np.average(np.var(forgenHoG64Chars,axis=0) ),
    "HL32_gengen":np.average(np.var(gengenHL32Chars,axis=0) ),
    "HL32_forgen":np.average(np.var(forgenHL32Chars,axis=0) ),
    "HL64_gengen":np.average(np.var(gengenHL64Chars,axis=0) ),
    "HL64_forgen":np.average(np.var(forgenHL64Chars,axis=0) )}
    gengenMorph = None
    forgenMorph = None
    gengenLBP32 = None
    forgenLBP32 = None
    gengenLBP64 = None
    forgenLBP64 = None
    gengenLBP32Chars = None
    forgenLBP32Chars = None 
    gengenLBP64Chars = None 
    forgenLBP64Chars = None
    gengenHoG32Chars = None 
    forgenHoG32Chars = None 
    gengenHoG64Chars = None 
    forgenHoG64Chars = None
    gengenHL32Chars = None
    forgenHL32Chars = None
    gengenHL64Chars = None
    forgenHL64Chars = None
    gengenMorphChars = None
    forgenMorphChars = None
    gengenMorphGChars = None
    forgenMorphGChars = None
    gengenMorphTChars = None
    forgenMorphTChars = None