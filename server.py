from flask import Flask,request,render_template,Response
from flask_uploads import UploadSet,SCRIPTS,configure_uploads
import os
from random import *
import subprocess

TOP_LEVEL_DIR = os.path.abspath(os.curdir)
app =Flask(__name__)

Destination_folder= '/home/rahul/Desktop/python'

app.config['UPLOADED_DATA_DEST'] =  Destination_folder
app.config['UPLOADS_DEFAULT_DEST']  = Destination_folder

data = UploadSet('data',SCRIPTS)
configure_uploads(app, data)

filesdata ={}               #file_id-file_name pair of files dictionary that are in server

@app.route('/api/v1/scripts', methods=['POST'])                    #POST
def upload():
    if request.method == 'POST' and 'data' in request.files:      
        filename =data.save(request.files['data'])                  #save the incoming file
        fileid = str(randint (1,10000000))                          #create a randomn id for the file
        while fileid in filesdata.keys():                           #if the file id already exists , create again
            fileid = str(randint(1,10000000))
        filesdata[fileid]=filename                                  #store the id and name of file 
        resp = "{\n     script-id: "+fileid+"\n}\n"                 #response to the client
        return Response(resp,status=201,mimetype='text/plain')

@app.route('/api/v1/scripts/<fid>',methods=['GET'])                #GET
def invoke(fid):
    if request.method == 'GET' and fid in filesdata.keys():        #if the requested file id is stored
        fn = filesdata[fid]                                        #retrieve the name of the file
        command = "python "+Destination_folder+"/"+fn         #command to run the requested python script
        res=subprocess.Popen(command,shell =True,stdout=subprocess.PIPE)     #create a subprocess
        for line in res.stdout:
            data=line                                             #capture the output of requested script
        return Response(data,status =200,mimetype ="text/plain")    #send the response to the client
    else:
        return "File not in the server"                           #requested script(file) is not stored in the server
if __name__ == '__main__':                                        
    app.run(host='0.0.0.0',port=8000)

