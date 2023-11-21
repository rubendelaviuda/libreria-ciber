from __future__ import print_function
from bd import obtener_conexion
import sys

def insertar_libro(nombre, descripcion, precio,foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO libros(nombre, descripcion, precio,autor,foto) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio,foto))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret = {"status": "Failure" }
        code=200
        conexion.commit()
        conexion.close()
    except:
        print("Excepcion al insertar un libro", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def convertir_libro_a_json(libro):
    d = {}
    d['id'] = libro[0]
    d['nombre'] = libro[1]
    d['descripcion'] = libro[2]
    d['precio'] = libro[3]
    d['autor'] = libro[4]
    d['foto'] = libro[5]
    return d

def obtener_libros():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, autor, foto FROM libros")
            libros = cursor.fetchall()
            librosjson=[]
            if libros:
                for libro in libros:
                    librosjson.append(convertir_libro_a_json(libro))
        conexion.close()
        code=200
    except:
        print("Excepcion al obtener los libros", file=sys.stdout)
        librosjson=[]
        code=500
    return librosjson,code

def obtener_libro_por_id(id):
    librojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            #cursor.execute("SELECT id, nombre, descripcion, precio,foto FROM libros WHERE id = %s", (id,))
            cursor.execute("SELECT id, nombre, descripcion, precio, autor, foto FROM libros WHERE id =" + id)
            libro = cursor.fetchone()
            if libro is not None:
                librojson = convertir_libro_a_json(libro)
        conexion.close()
        code=200
    except:
        print("Excepcion al recuperar un libro", file=sys.stdout)
        code=500
    return librojson,code


def eliminar_libro(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un libro", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code

def actualizar_libro(id, nombre, descripcion, precio, foto):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("UPDATE libros SET nombre = %s, descripcion = %s, precio = %s,autor = %s, foto=%s WHERE id = %s",
                       (nombre, descripcion, precio, foto,id))
            if cursor.rowcount == 1:
                ret={"status": "OK" }
            else:
                ret={"status": "Failure" }
        conexion.commit()
        conexion.close()
        code=200
    except:
        print("Excepcion al eliminar un libro", file=sys.stdout)
        ret = {"status": "Failure" }
        code=500
    return ret,code
