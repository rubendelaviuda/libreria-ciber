from flask import request, make_response, escape
import json
import decimal
from __main__ import app
from funciones import prepare_response_extra_headers,validar_session_normal,validar_session_admin
import controlador_libros

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

response_extra_headers = prepare_response_extra_headers(True)

@app.route("/libros",methods=["GET"])
def libros():
    if (validar_session_normal()):
        ret,code= controlador_libros.obtener_libros()
    else:
        ret={"status":"Forbidden"}
        code=403
    response=make_response(json.dumps(ret, cls = Encoder),code)
    return response

@app.route("/libro/<id>",methods=["GET"])
def libro_por_id(id):
    if (validar_session_normal()):
        ret,code = controlador_libros.obtener_libro_por_id(id)
    else:
        ret={"status":"Forbidden"}
        code=403
    response=make_response(json.dumps(ret, cls = Encoder),code)
    return response

@app.route("/libros",methods=["POST"])
def guardar_libro():
    if (validar_session_admin()):
        code = 200
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            libro_json = request.json
            nombre = libro_json["nombre"].strip().replace('"', "")
            nombre = f"{escape(nombre)}"
            descripcion = libro_json["descripcion"].strip().replace('"', "")
            descripcion = f"{escape(descripcion)}"
            precio = libro_json["precio"].strip().replace('"', "")
            precio = f"{escape(precio)}"
            autor = libro_json["autor"].strip().replace('"', "")
            autor = f"{escape(autor)}"
            foto = libro_json["foto"].strip().replace('"', "")
            foto = f"{escape(foto)}"
            if (len(nombre) ==0 or len(nombre) > 256):
                ret={"status":"Bad request n"}
                code=401
            if (code == 200 and len(descripcion) > 256):
                ret={"status":"Bad request d"}
                code=401
            if (code == 200 and len(foto) > 256):
                ret={"status":"Bad request f"}
                code=401
            if (code == 200 and not precio.replace(".", "").isdecimal()):
                ret={"status":"Bad request p"}
                code=401
            if (code == 200 and len(autor) > 256):
                ret={"status":"Bad Request a"}
                code=401
            if (code == 200):
                try:
                    precio = float(precio)
                except:
                    ret={"status":"Bad request pf"}
                    code=401 
            if (code == 200):
                ret,code=controlador_libros.insertar_libro(nombre,descripcion,precio,autor,foto)
        else:
            ret={"status":"Bad request"}
            code=401
    else:
        ret={"status":"Forbidden"}
        code=403
    
    response=make_response(json.dumps(ret),code)
    return response

@app.route("/libros/<id>", methods=["DELETE"])
def eliminar_libro(id):
    if (validar_session_admin()):
        ret,code=controlador_libros.eliminar_libro(id)
    else:
        ret={"status":"Forbidden"}
        code=403
    
    response=make_response(json.dumps(ret),code)
    return response

@app.route("/libros", methods=["PUT"])
def actualizar_libro():
    if (validar_session_admin()):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            libro_json = request.json
            ret,code=controlador_libros.actualizar_libro(libro_json["id"],libro_json["nombre"], libro_json["descripcion"], float(libro_json["precio"]), libro_json["autor"], libro_json["foto"])
        else:
            ret={"status":"Bad request"}
            code=401
    else:
        ret={"status":"Forbidden"}
        code=403

    response=make_response(json.dumps(ret),code)
    return response
