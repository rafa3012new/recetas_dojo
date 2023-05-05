from flask import flash, redirect, session, url_for

def login_required(ruta):

    def wrapper(*args,**kwargs):
        if 'idusuario' not in session or session['idusuario'] is None:
            flash('Ud no tiene acceso a esta pagina', 'danger')
            return redirect("/login")
        resp = ruta(*args,**kwargs)
        return resp

    return wrapper
