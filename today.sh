##python3 xor_test.py 'BHSig260FIX/Hindi/' 'pairs.list.genuine'
##python3 xor_test.py 'BHSig260FIX/Bengali/' 'pairs.list.genuine'
##python3 characteristicsExtractor.py 'BHSig260FIX/Bengali/' '' '' 'pairs.list.genuine.xor' 'pairs.forgery_genuine.xor'
##python3 characteristicsExtractor.py 'BHSig260FIX/Hindi/' '' '' 'pairs.list.genuine.xor' 'pairs.forgery_genuine.xor' 
##
##python3 generateVector.py 'signatures/' 'pairs.forgery_genuine.xor.characteristics' 'pairs.list.genuine3.xor.characteristics' 'list.genuine3.characteristics' 'list.forgery3.characteristics'
##python3 generateVector.py 'BHSig260FIX/Bengali/' 'pairs.forgery_genuine.xor.characteristics' 'pairs.list.genuine.xor.characteristics' 'list.genuine.characteristics' 'list.forgery.characteristics'
##python3 generateVector.py 'BHSig260FIX/Hindi/' 'pairs.forgery_genuine.xor.characteristics' 'pairs.list.genuine.xor.characteristics' 'list.genuine.characteristics' 'list.forgery.characteristics'
##
##python3 modelTrainer_10Chars.py 'BHSig260FIX/Bengali/Model_Morph_Centered/' 'BHSig260FIX/Bengali/gengenVectors' 'BHSig260FIX/Bengali/forgenVectors' '100' '1'
##python3 modelTrainer_10Chars.py 'BHSig260FIX/Hindi/Model_Morph_Centered/' 'BHSig260FIX/Hindi/gengenVectors' 'BHSig260FIX/Hindi/forgenVectors' '160' '2'
#python3 modelTrainer_10Chars.py 'signatures/Model_Morph_Centered/' 'signatures/gengenVectors' 'signatures/forgenVectors' '55' '3'

python3 histModels.py '../BHSig260FIX/Bengali/Model_Morph_Centered/' '../BHSig260FIX/Bengali/Vectores_Característicos/gengenVectors' '../BHSig260FIX/Bengali/Vectores_Característicos/forgenVectors' '100' '1'
python3 histModels.py '../BHSig260FIX/Hindi/Model_Morph_Centered/' '../BHSig260FIX/Hindi/Vectores_Característicos/gengenVectors' '../BHSig260FIX/Hindi/Vectores_Característicos/forgenVectors' '160' '2'
python3 histModels.py '../signatures/Model_Morph_Centered/' '../signatures/Vectores_Característicos/gengenVectors' '../signatures/Vectores_Característicos/forgenVectors' '55' '3'