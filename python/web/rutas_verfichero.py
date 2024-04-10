from __main__ import app
from flask import request,make_response
import os
import sys
import json
import subprocess

@app.route ('/ver/<archivo>', methods=['GET']) 
def ver(archivo):
    try:    
        basepath = os.path.dirname(__file__) # ruta del archivo actual
        upload_path = os.path.join (basepath,'static',archivo) 
        if os.path.exists(upload_path):
            salida=subprocess.getoutput("cat " + upload_path)
            ret={"status":"OK", "contenido": salida}
            code=200
        else:
            ret={"status":"ERROR", "mensaje": "El archivo no existe"}
            code=200
    except:
        ret={"status":"ERROR"}
        code=500
    response=make_response(json.dumps(ret),code)
    return response
