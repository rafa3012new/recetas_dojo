from flask import Flask
import os

#se inicializa la aplicacion
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")