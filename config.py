#configuraciones de la aplicacion

import os
from dotenv import load_dotenv

#comenzamos tomando la ruta absoluta del directorio raiz (proyecto_isi)
basedir = os.path.abspath(os.path.dirname(__file__))
#cargamos las variables de entorno definidas en el .env
#importante no subir al repositorio GitHub dicho .env ya que puede contener informacion confidencial --> gitignore
#una vez haya cargado el repositorio en el servidor remoto, crear ahí dentro del directorio raiz de mi aplicacion el archivo '.env'
load_dotenv(os.path.join(basedir,'.env'))

class Config:
    #definimos variables de configuracion

    #ubicacion de la base de datos relacional a usar con nuestra aplicacion flask
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')