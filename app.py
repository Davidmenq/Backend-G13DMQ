from flask import Flask
from base_de_datos import conexion
from models.mascota import MascotaModel
# convierte caracteres especiales a un formato 'seguro'
from urllib.parse import quote_plus
from flask_migrate import Migrate
from flask_restful import Api
from controllers.usuario import UsuariosController, UsuarioController
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
# origins indica los dominios que pueden acceder a mi API
CORS(app, origins=['https://editor.swagger.io', 'http://mifrontend.com'], methods=['GET','POST','PUT','DELETE'], 
     allow_headers=['authorization','content-type','accept'])


# enpoint donde se podra acceder a la documentacion
SWAGGER_URL= '/docs'
# donde se almacena mi archivo de la documentacion
API_URL='/static/documentacion_swagger.json'

configuracionSwagger = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={
    'app_name':'Documentacion de Directorio de Mascotas'
})

#agregar otra aplicacion  que no sea Flask a nuestro proyecto de Flask
app.register_blueprint(configuracionSwagger)

# config > se van a guardar todas las variables de nuestro proyecto de flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:%s@localhost:5432/directorio' % quote_plus('root')

#inicializar mi aplicacion de flask sql alchemy
#dentro de la aplicacion de flask tendremos nuestra conexion a  la base de datos
conexion.init_app(app)
api.init_app(app)

Migrate(app=app, db=conexion)

# @app.route('/crear-tablas', methods=['GET'])
# def crearTablas():
#     # creara todas las tablas declaradas en el proyecto
#     conexion.create_all()
#     return {
#         'message':'Creacion ejecutada exitosamente'
#     }

api.add_resource(UsuariosController, '/usuarios')
api.add_resource(UsuarioController, '/usuario/<int:id>')

if __name__=='__main__':
    app.run(debug=True)
    