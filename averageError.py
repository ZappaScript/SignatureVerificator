for model in ["Model_Morph_Centered", "Modelos_combinados", "Modelos_Hist_sin_LBP", "Modelos_Morph_xOr", "Modelos_Hist_32PX", "Modelos_Hist_64PX" ]:
    resultC = json.load(open('signatures/'+model+'/Def_Results'))
    resultB = json.load(open('BHSig260FIX/Bengali/'+model+'/Def_Results'))
    resultH = json.load(open('BHSig260FIX/Hindi/'+model+'/Def_Results'))
    print(model)
    for file in [[resultC,'resultC'],[resultB,'resultB'],[resultH,'resultH' ]]:                                         
        minErrorRate =9999 
        minErrorRateObject = {}
                                                                                                      
        for key in file[0]:
            if (( 1 - file[0][key][0])+( 1 - file[0][key][1]) )/2 < minErrorRate:
                minErrorRate = (( 1 - file[0][key][0])+( 1 - file[0][key][1]) )/2
                minErrorRateObject = {'model':model,'file':file[1],'ER':minErrorRate, 'method':key }
            
        print(minErrorRateObject)


for model in ["Model_Morph_Centered", "Modelos_combinados", "Modelos_Hist_sin_LBP", "Modelos_Morph_xOr", "Modelos_Hist_32PX", "Modelos_Hist_64PX" ]:
    resultC = json.load(open('signatures/'+model+'/simpleForgeriesResult2'))
    resultB = json.load(open('BHSig260FIX/Bengali/'+model+'/simpleForgeriesResult2'))
    resultH = json.load(open('BHSig260FIX/Hindi/'+model+'/simpleForgeriesResult2'))
    print(model)
    for file in [[resultC,'resultC'],[resultB,'resultB'],[resultH,'resultH' ]]:                                         
        minErrorRate =9999 
        minErrorRateObject = {}
                                                                                                      
        for key in file[0]:
            if ( 1 - file[0][key]) < minErrorRate:
                minErrorRate =  1 - file[0][key]
                minErrorRateObject = {'model':model,'file':file[1],'ER':minErrorRate, 'method':key }
            
        print(minErrorRateObject)