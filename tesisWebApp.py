from flask import Flask, request, jsonify,send_from_directory, make_response
from backend_xor import *
import os 
from flask_cors import CORS
import re
import string
from io import BytesIO
import random

app = Flask(__name__,static_folder='view/build')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
##app.run(host= '0.0.0.0')
globalDict = {} ##just a test

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getModel(opt,param):
    if opt == 'morph':
        if param:
            return 'Model_Morph_Centered/'
        else:
            return 'Model_Morph/'
    if opt == 'hist':
        if param == 32:
            return 'Modelos_Hist_32PX/'
        if param == 64:
            return 'Modelos_Hist_64PX/'
    if opt == 'eucl':
        if param == 12:
            return 'list.genuine.points.12Gen'
        if param == 18:
            return 'list.genuine.points.18Gen'
        if param == 24:
            return 'list.genuine.points.24Gen'
            

@app.route('/', defaults = {'path':''})
@app.route('/<path:path>')
def serve(path):
    if (path == ""):
        return send_from_directory('view/build','index.html')
    else:
        if(os.path.exists('view/build/' + path ) ):
            print (request)
            print('wut1')
            return send_from_directory('view/build/',path)
        else:
            print (request)
            print('wut2')
            return send_from_directory('view/build', 'index.html')

@app.route('/test',methods=["GET","POST"])
def runPrediction():
    if request.method == "POST" :
        file = request.files['media'].read()

        user = request.form['user']
        npimg = np.fromstring(file, np.uint8)
        if(re.match('^[BHC]\-[\d]+$',user)):
            database = re.search('^(.+?)\-[\d]+$',user).group(1)
            
            if (database == 'H' ):
                modelPath = 'BHSig260FIX/Hindi/'
                databasePath = 'BHSig260FIX/Hindi/'+re.search('^[BHC]?\-(.+?)$',user).group(1).zfill(3)
                userNum = re.search('^[BHC]?\-(.+?)$',user).group(1)
                file = '/H-S-'+userNum+'-G-'+str(int(random.uniform(1,24))).zfill(2)+'.tif'    
            if (database == 'B' ):
                modelPath = 'BHSig260FIX/Bengali/'
                databasePath = 'BHSig260FIX/Bengali/'+re.search('^[BHC]?\-(.+?)$',user).group(1).zfill(3)
                userNum = re.search('^[BHC]?\-(.+?)$',user).group(1)
                file = '/B-S-'+userNum+'-G-'+str(int(random.uniform(1,24))).zfill(2)+'.tif'    
            if (database == 'C' ):
                modelPath = 'signatures/'
                databasePath = 'signatures/'+re.search('^[BHC]?\-(.+?)$',user).group(1)
                userNum = re.search('^[BHC]?\-(.+?)$',user).group(1)
                file = '/C-S-'+userNum+'-G-'+str(int(random.uniform(1,24))    )+'.tif'
            
        print(request.form)
        params = [request.form['morphologySettings']=='true',int(request.form['histogramSettings']),int(request.form['euclideanSettings'])]
        print (params)
        imgQ = cv2.imdecode(npimg,0)
        imgS = cv2.imread(databasePath+file,0)
        results = testSignature(imgS,imgQ,[ modelPath+getModel('morph',params[0]), modelPath+getModel('hist',params[1]),modelPath+'Modelos_combinados/' ],params) 
        
        id_ = id_generator()
        globalDict[id_] = results[4]
        id_2 = id_generator()
        globalDict[id_2] = results[5]
        
        toReturn = [results[0]] + [results[1]] + [results[2]] + [{'Euclidian':testSignatureEuclidean(imgQ,modelPath+getModel('eucl',params[2]),userNum  )}] + [{'charsMorph':results[3]}] + [{'idMorph':id_,'idHist':id_2}]
        
        
        return jsonify(toReturn)
            
        
@app.route('/getImage/<image>',methods=["GET","POST"])
def getImage(image):   
    if request.method == "GET" :
        print('Got in, received ',image )
        for i in globalDict:
            print (i)

        for i in request.form:
            print(i)
        print(request)
        
        
        _, img_encoded = cv2.imencode('.png', globalDict[image])
        response = make_response(img_encoded.tobytes())
        response.headers['Content-Type'] = 'image/png'
        return response
        