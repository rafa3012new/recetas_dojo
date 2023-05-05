import os
# from re import T
# from tkinter import ttk
from flask import flash
from datetime import datetime
from flask_recetas_dojo.config.mysqlconnection import connectToMySQL
from flask_recetas_dojo.models import modelo_base
from flask_recetas_dojo.models import recetas
from flask_recetas_dojo.utils.regex import REGEX_CORREO_VALIDO
from flask_recetas_dojo.utils.myfunctions import diferencia_tiempo

class Usuario(modelo_base.ModeloBase):

    modelo = 'usuarios'
    campos = ['usuario', 'nombre','apellido','email','password']

    def __init__(self, data):
        self.id = data['id']
        self.usuario = data['usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.recetas = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def buscar(cls, dato):
        query = "select * from usuarios where usuario = %(dato)s OR email = %(dato)s"
        data = { 'dato' : dato }
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, data)

        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_usuarios_enviar(cls, dato):

        query = "select * from usuarios where id <> %(id)s"

        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db(query, dato)


        all_data = []

        if results:
            #convertimos la lista de json (diccionarios) en una lista de objetos python
            for data in results:
                all_data.append(cls(data))

        return all_data


    @staticmethod
    def validar_largo(data, campo, largo):
        is_valid = True
        if len(data[campo]) <= largo:
            flash(f'El largo del {campo} no puede ser menor o igual {largo}', 'error')
            is_valid = False
        return is_valid

    @classmethod
    def validar(cls, data):

        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid

        if 'user' in data:
            is_valid = cls.validar_largo(data, 'user', 3)

            if is_valid == False: no_create = False

            if cls.validar_existe('usuario', data['user']):
                flash('el usuario ya esta ingresado', 'error')
                is_valid = False

            if is_valid == False: no_create = False


        if 'name' in data:
            is_valid = cls.validar_largo(data, 'name', 1)
            if is_valid == False: no_create = False

        if 'lastname' in data:
            is_valid = cls.validar_largo(data, 'lastname', 1)
            if is_valid == False: no_create = False

        if 'password_reg' in data:
            is_valid = cls.validar_largo(data, 'password_reg', 7)
            if is_valid == False: no_create = False

            if 'cpassword_reg' in data:
                if data['password_reg'] != data['cpassword_reg']:
                    flash('la contraseña de confirmacion no concide con la contraseña', 'error')
                    is_valid = False
                if is_valid == False: no_create = False

        if 'email' in data:
            if not REGEX_CORREO_VALIDO.match(data['email']):
                flash('El correo no es válido', 'error')
                is_valid = False

            if is_valid == False: no_create = False

            if cls.validar_existe('email', data['email']):
                flash('el correo ya fue ingresado', 'error')
                is_valid = False

            if is_valid == False: no_create = False


        return no_create



    #relacion uno (1) a muchos
    #Metodo de clase de 1 a muchos = 1 usuario es autor de varias mensajes
    #Este metodo obtiene todos las recetas de las que un usuario es autor
    #Se obtinene los datos del usuario consultado...
    #Y luego se le agregan las recetas de las que el usuario es autor
    #La propiedad recetas, alamcenaran una lista de objetos...
    @classmethod
    def get_recetas_de_usuario( cls , dato):

        #Se obtienen los datos del usuario que consultamos
        query = 'SELECT * FROM usuarios where id = %(id)s'
        results = []
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db( query , dato)

        usuario = cls(results[0])


        #Se obtienen las recetas de las que el usuario es autor
        query = 'SELECT r.id, r.nombre,, r.descripcion, r.instrucciones, CONCAT(u.nombre, " ", u.apellido) as autor, r.created_at, r.updated_at FROM recetas r LEFT JOIN usuarios u ON r.autor = u.id WHERE u.id = %(id)s'
        results = []
        results = connectToMySQL(os.environ.get("BASEDATOS_NOMBRE")).query_db( query , dato)

        #Almacenamos los datos de los mensajes de usuarios en la propiedad 
        if results:
            for row_from_db in results:
                # ahora parseamos los datos de los mensajes para crear instancias de usuarios y agregarlas a nuestra lista

                receta_data = {
                    "id" : row_from_db["id"],
                    "autor" : row_from_db["autor"],
                    "nombre" : row_from_db["nombre"],
                    "descripcion" : row_from_db["descripcion"],
                    "instrucciones" : row_from_db["instrucciones"],
                    "under30" : row_from_db["under30"],
                    "date_made" : row_from_db["date_made"],
                    "created_at": row_from_db["created_at"],
                    "updated_at": row_from_db["updated_at"]
                }

                usuario.recetas.append( recetas.Receta( receta_data ) )

        return usuario