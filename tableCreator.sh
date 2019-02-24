experiment=$1
global=$2
if [ $global = n ]
then
    declare -a arr=("Model_Morph_Centered" "Modelos_combinados" "Modelos_Hist_sin_LBP" "Modelos_Morph_xOr" "Modelos_Hist_32PX" "Modelos_Hist_64PX" "Modelos_Hist_sin_LBP_64" )
    for i in "${arr[@]}"
    do
    a='signatures/'$i'/Def_Results'
    b='BHSig260FIX/Bengali/'$i'/Def_Results' 
    c='BHSig260FIX/Hindi/'$i'/Def_Results' 
    d='Tablas/'$i'_experiment_.png' 
    e=$i
    python3 tableCreator.py $a $b $c $d $e 
    done
elif [ $global = y ]
then
    declare -a arr=("Modelo_Global" "Modelo_Global_Combinado" "Modelo_Global_Combinado_PCA" "Modelo_Global_LBPHoG")
    for i in "${arr[@]}"
    do
    echo "$i"
    a=$i'/results'
    b='Tablas/'$i'_experiment_.png'
    c=$i
    python3 tabCreatorGlobalModels.py $a $b $c
    done
elif [ $global = ysf ]
then
    declare -a arr=("Modelo_Global" "Modelo_Global_Combinado" "Modelo_Global_Combinado_PCA" "Modelo_Global_LBPHoG")
    for i in "${arr[@]}"
    do
    echo "$i"
    a=$i'/simpleForgeriesResult'
    b='Tablas/'$i'_sf_experiment_.png'
    c=$i
    python3 tabCreatorGlobalModelsSF.py $a $b $c
    done
fi

if [ $global = sf ]
then
    #declare -a arr=("Model_Morph_Centered" "Modelos_combinados" "Modelos_Hist_sin_LBP" "Modelos_Morph_xOr" "Modelos_Hist_32PX" "Modelos_Hist_64PX" )
    declare -a arr=("Modelos_Hist_sin_LBP_64" )
    ##declare -a arr=("Model_Morph_Centered" "Modelos_combinados" "Modelos_Hist_sin_LBP" "Modelos_Morph_xOr" "Modelos_Hist_32PX")
    ## now loop through the above array
    for i in "${arr[@]}"
    do
        echo "$i"
        a='signatures/'$i'/Def_Results_SF'
        b='BHSig260FIX/Bengali/'$i'/Def_Results_SF' 
        c='BHSig260FIX/Hindi/'$i'/Def_Results_SF' 
        d='Tablas/'$i'_sf_experiment_.png' 
        e=$i
        python3 simpleForgeriesTableCreator.py $a $b $c $d $e 
    done
fi
if [ $global = ud ]
then
    declare -a arr=("MM" "xOr" "PCA" "MC" "HoGLBP32" "HoGLBP64" "HoG32" "HoG64" )
    ##declare -a arr=("Model_Morph_Centered" "Modelos_combinados" "Modelos_Hist_sin_LBP" "Modelos_Morph_xOr" "Modelos_Hist_32PX")
    ## now loop through the above array
    for i in "${arr[@]}"
    do
        echo "$i"
        a='Modelos_Dependientes_Usuario/CEDAR/'$i'/results'
        b='Modelos_Dependientes_Usuario/Bengali/'$i'/results' 
        c='Modelos_Dependientes_Usuario/Hindi/'$i'/results' 
        d='Tablas/'$i'_ud_experiment_.png' 
        e=$i
        python3 tableCreator.py $a $b $c $d $e 
    done
fi
if [ $global = sfud ]
then
    declare -a arr=("MM" "xOr" "PCA" "MC" "HoGLBP32" "HoGLBP64" "HoG32" "HoG64")
    ##declare -a arr=("Model_Morph_Centered" "Modelos_combinados" "Modelos_Hist_sin_LBP" "Modelos_Morph_xOr" "Modelos_Hist_32PX")
    ## now loop through the above array
    for i in "${arr[@]}"
    do
        echo "$i"
        a='Modelos_Dependientes_Usuario/CEDAR/'$i'/Def_SF_Results'
        b='Modelos_Dependientes_Usuario/Bengali/'$i'/Def_SF_Results' 
        c='Modelos_Dependientes_Usuario/Hindi/'$i'/Def_SF_Results' 
        d='Tablas/'$i'_sf_ud_experiment_.png' 
        e=$i
        python3 simpleForgeriesTableCreator.py $a $b $c $d $e 
    done
fi