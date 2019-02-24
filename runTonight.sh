#!/bin/sh

python3 histModels-nonLBP.py 'signatures/Modelos_Hist_sin_LBP_64/' 'signatures/Vectores_Característicos/gengenVectors.LBPHoG64' 'signatures/Vectores_Característicos/forgenVectors.LBPHoG64' '55' '3'
python3 histModels-nonLBP.py 'BHSig260FIX/Hindi/Modelos_Hist_sin_LBP_64/' 'BHSig260FIX/Hindi/Vectores_Característicos/gengenVectors.LBPHoG64' 'BHSig260FIX/Hindi/Vectores_Característicos/forgenVectors.LBPHoG64' '160' '2'
python3 histModels-nonLBP.py 'BHSig260FIX/Bengali/Modelos_Hist_sin_LBP_64/' 'BHSig260FIX/Bengali/Vectores_Característicos/gengenVectors.LBPHoG64' 'BHSig260FIX/Bengali/Vectores_Característicos/forgenVectors.LBPHoG64' '100' '1'

# etc.