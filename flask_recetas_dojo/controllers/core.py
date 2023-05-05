import os
from flask import redirect, render_template, request, flash, session, url_for
from flask_recetas_dojo import app
from flask_bcrypt import Bcrypt
from flask_recetas_dojo.models.usuarios import Usuario
from flask_recetas_dojo.models.recetas import Receta
from datetime import datetime
# from flask_recetas_dojo.utils.decorators import login_required

bcrypt = Bcrypt(app)

@app.route("/")
# @login_required
def index():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")

    datos_recetas = []

    if 'idusuario' in session:
        datos_recetas = Receta.get_all_extra()

    return render_template("main.html", sistema=nombre_sistema, recetas=datos_recetas)

@app.route("/login")
def login():

    if 'usuario' in session:
        flash('Ya estás LOGEADO!', 'warning')
        return redirect('/')

    return render_template("login.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    #validaciones del objeto usuario
    if not Usuario.validar(request.form):
        return redirect('/login')

    pass_hash = bcrypt.generate_password_hash(request.form['password_reg'])

    data = {
        'usuario' : request.form['user'],
        'nombre' : request.form['name'],
        'apellido' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/login")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identification'])

    if not usuario:
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Usuario/Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['idusuario'] = usuario.id
    session['usuario'] = usuario.nombre + " " + usuario.apellido


    return redirect('/')

@app.route('/logout')
def logout():
    print("si log out")
    session.clear()
    return redirect('/login')


@app.route("/crearreceta")
def crearreceta():

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')


    operacion = "Nueva Receta"
    data = {
    'id':'',
    'nombre':'',
    'descripcion':'',
    'instrucciones':'',
    'under30' : 0,
    'date_made':datetime.date
    }
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template('form.html',operacion=operacion,receta=data,sistema=nombre_sistema)


@app.route("/editar_receta/<id>")
def editar_receta(id):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')


    operacion = "Editar Receta"
    datos_receta = Receta.get_by_id_extra(id)
    data = {
    'id':id,
    'nombre':datos_receta.nombre,
    'descripcion':datos_receta.descripcion,
    'instrucciones':datos_receta.instrucciones,
    'under30' : int(datos_receta.under30),
    'date_made': datos_receta.date_made.strftime("%Y-%m-%d")
    }
    return render_template('form.html',operacion=operacion,receta=data)



@app.route("/procesar_receta", methods=["POST"])
def procesar_receta():

    fecha = datetime.date
    date_format = '%Y-%m-%d %H:%M:%S'

    if type(request.form['date_made']) is str:
        fecha = datetime.strptime(request.form['date_made'] + " 00:00:00",date_format)

    data ={
            'autor':session['idusuario'],
            'nombre':request.form['nombre'],
            'descripcion':request.form['descripcion'],
            'instrucciones':request.form['instrucciones'],
            'under30':int(request.form['under30']),
            'date_made':fecha
           }

    if not Receta.validar(data):
        return redirect("/")

    try:
        if request.form['operacion'] == 'Nueva Receta':
            Receta.save(data)
        if  request.form['operacion'] == 'Editar Receta':
            data['id'] = int(request.form['id'])
            Receta.update(data)
        flash("Receta almacenada con exito!","success")
        print("receta guardado con exito!",flush=True)
    except Exception as error:
        print(f"error al guardar la receta, muy extrano, valor del error : {error}",flush=True)

    return redirect('/')


@app.route("/eliminar_receta/<id>")
def eliminar_receta(id):

    try:
        Receta.delete(int(id))
        print(f"Eliminacion de receta con exito {id}",flush=True)
    except Exception as error:
        print("error al eliminar la receta",flush=True)

    return redirect('/')

@app.route("/detalle_receta/<id>")
def detalle_receta(id):

    if 'usuario' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')


    datos_receta = Receta.get_by_id_extra(int(id))
    nombre_sistema = os.environ.get("NOMBRE_SISTEMA")
    return render_template('detail.html',receta=datos_receta,sistema=nombre_sistema)