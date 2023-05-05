import os
from flask import flash
from flask_recetas_dojo.config.mysqlconnection import connectToMySQL
from flask_recetas_dojo.models import modelo_base
from flask_recetas_dojo.models import usuarios
from flask_recetas_dojo.utils.regex import REGEX_CORREO_VALIDO
from datetime import datetime


class Receta(modelo_base.ModeloBase):

    modelo = 'recetas'
    campos = ['autor', 'nombre', 'descripcion','instrucciones','under30','date_made']

    def __init__(self, data):
        self.id = data['id']
        self.autor = data['autor']
        self.nombre_autor = data['nombre_autor']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def buscar(cls, dato):
        query = "select * from recetas where id = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def update(cls,data):
        query = 'UPDATE recetas SET nombre = %(nombre)s, descripcion = %(descripcion)s, instrucciones = %(instrucciones)s, under30 = %(under30)s, date_made = %(date_made)s WHERE id = %(id)s;'
        resultado = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return resultado


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del campo {campo} no puede ser menor o igual a {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid


        if 'descripcion' in data:
            is_valid = cls.validar_largo(data, 'descripcion', 3)
            if is_valid == False: no_create = False

        if 'instrucciones' in data:
            is_valid = cls.validar_largo(data, 'instrucciones', 3)
            if is_valid == False: no_create = False

        return no_create

    @classmethod
    def get_all_extra(cls):
        query = 'SELECT r.id, r.nombre, r.descripcion, r.instrucciones, r.under30, r.date_made, r.autor, r.created_at, r.updated_at, CONCAT(u.nombre, " ", u.apellido) as nombre_autor FROM recetas r left join usuarios u on r.autor = u.id'
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query)
        # print("query get_all_extra ",results,flush=True)
        all_data = []
        for data in results:
            all_data.append(cls(data))

        return all_data


    @classmethod
    def get_by_id_extra(cls, id):
        query = 'SELECT r.id, r.nombre, r.descripcion, r.instrucciones, r.under30, r.date_made, r.autor, r.created_at, r.updated_at, CONCAT(u.nombre, " ", u.apellido) as nombre_autor FROM recetas r left join usuarios u on r.autor = u.id where r.id = %(id)s'
        # print(query,flush=True)
        data = { 'id' : id }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)
        return cls(results[0])