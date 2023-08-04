from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from utilitarios import conexion
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
from models import *

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DATABASE_URL')

CORS(app, origins='*')
api=Api(app)

conexion.init_app(app)

Migrate(app, conexion)

if __name__=='__main__':
    app.run(debug=True)

