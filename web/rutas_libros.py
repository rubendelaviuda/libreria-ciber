from flask import request, session
import json
import decimal
from __main__ import app
import controlador_libros

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

@app.route("/libros",methods=["GET"])
def libros():
    libros,code= controlador_libros.obtener_libros()
    return json.dumps(libros, cls = Encoder),code

@app.route("/libro/<id>",methods=["GET"])
def libro_por_id(id):
    libro,code = controlador_libros.obtener_libro_por_id(id)
    return json.dumps(libro, cls = Encoder),code

@app.route("/libros",methods=["POST"])
def guardar_libro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        libro_json = request.json
        ret,code=controlador_libros.insertar_libro(libro_json["nombre"], libro_json["descripcion"], float(libro_json["precio"]),libro_json["autor"], libro_json["foto"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

@app.route("/libros/<id>", methods=["DELETE"])
def eliminar_libro(id):
    ret,code=controlador_libros.eliminar_libro(id)
    return json.dumps(ret), code

@app.route("/libros", methods=["PUT"])
def actualizar_libro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        libro_json = request.json
        ret,code=controlador_libros.actualizar_libro(libro_json["id"],libro_json["nombre"], libro_json["descripcion"], float(libro_json["precio"]), libro_json["autor"],libro_json["foto"])
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code