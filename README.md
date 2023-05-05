#Esta version de Recetas Dojo hace uso de:

#Front End

HTML, CSS, JAVASRIPT Y BOOTSTRAP

#Back End

PYTHON, FLASK y MYSQL 

Hace uso del Modelo Vista Controlador (MVC)

#Archivos de Modelo:
base.py
usuarios.py

#Archivos de Vista (Templates, Static)

Templates:

base.html
main.html
form.html
detail.html
login.html
_menu.html

Static

recetas.css
recetas.js
archios de bootstrap...
utilidad toaster.css y js para modificar a apariencia de los mensajes flash llamada toastr


#Archivo Controlador
Controller.py

#Uso de blueprints

Hace uso de archivo .env, pero no se incluye debido a la seguridad de Github
contenido del archivo .env  a continuacion:

APP_SECRET_KEY="user_login"
BASEDATOS_HOST="localhost"
BASEDATOS_USER="root"
BASEDATOS_PASSWORD="root"
BASEDATOS_NOMBRE="user_login"
NOMBRE_SISTEMA="Sistema de Recetas"


crear las tablas y db desde la carpeta db