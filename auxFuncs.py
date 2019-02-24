def getName(name):
    if(name=='kNN' or name == 'k-NN'):
        return 'k-NN'
    if(name=='lSVC' or name=='SVC-l' or name =='SVC-L'):
        return 'SVC-Lineal'
    if(name=='mlp' or name == 'MLP' ):
        return 'MLP'
    if(name=='rForest' or name=='Random Forest'):
        return 'Random Forest'
    if(name=='rbfSVC' or name=='SVC-rbf' or name == 'SVC-RBF'):
        return 'SVC-Radial Basis'
    if(name=='bSVC' or name == 'B-SVC-RBF'):
        return 'SVC-Bagging'
    print(name)
    return name

def getNameTrue(name):
    if name == "SVC-Radial Basis" or name == 'SVC-RBF': 
        return 'rbfSVC'
    if name == "SVC-Lineal" or name == 'SVC-L':  
        return 'lSVC'
    if name == "SVC-Bagging" or name == 'B-SVC-RBF': 
        return 'bSVC'
    if name == "Random Forest" or name == 'rForest': 
        return "rForest"
    if name == "k-NN" or name =='kNN': 
        return 'kNN'
    if name == "MLP" or name =='mlp' : 
        return 'mlp'
    
    
    
    
    
    
    
    
    
    
    
    print(name)
    return name

def getName2(name):
    if( name == 'k-NN'):
        return 'kNN'
    if(name=='lSVC' or name=='SVC-l'):
        return 'lSVC'
    if(name=='mlp' or name == 'MLP' ):
        return 'mlp'
    if(name=='rForest' or name=='Random Forest'):
        return 'rForest'
    if(name=='rbfSVC' or name=='SVC-rbf'):
        return 'rbfSVC'
    if(name=='bSVC'):
        return 'bSVC'
    print(name)
    return name


def getMethodName(name):
    if(name=='xOrVar'):
        return 'MM'
    if(name=='g_metrics'):
        return 'Globales'
    if(name=='morph'):
        return 'MM+Globales'
    if(name=='LBP32'):
        return 'LBP 32PX'
    if(name=='LBP64'):
        return 'LBP 64PX'
    if(name=='HoG32'):
        return 'HoG 32PX'
    if(name=='HoG64'):
        return 'HoG 64PX'
    if(name=='HL32' ):
        return 'HoG+LBP 32PX'
    if(name=='HL64'):
        return 'HoG+LBP 64PX'
    print(name)
    return name

