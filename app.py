from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from utilitarios import conexion
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
from models import *
from flasgger import Swagger
from controllers import CategoriasController, RegistroController, LoginController
from json import load
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv()
swaggerData =load(open('swagger_data.json', 'r'))

swaggerConfig ={
    'headers':[],
    'specs':[
        {
            'endpoint':'documentacion',
            'route':'/'
        }
    ],
    'static_url_path':'/flasgger_static',
    'specs_route':'/documentacion'
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DATABASE_URL')

app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1,minutes=15)

JWTManager(app)

Swagger(app, template=swaggerData, config=swaggerConfig)

CORS(app, origins='*')
api=Api(app)

conexion.init_app(app)

Migrate(app, conexion)

api.add_resource(CategoriasController, '/categorias')
api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, '/login')

if __name__=='__main__':
    app.run(debug=True)

