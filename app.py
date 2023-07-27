from flask import Flask
from base_de_datos import conexion
from models.usuario import UsuarioModel
# convierte caracteres especiales a un formato 'seguro'
from urllib.parse import quote_plus
from flask_migrate import Migrate

app = Flask(__name__)

# config > se van a guardar todas las variables de nuestro proyecto de flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:%s@localhost:5432/directorio' % quote_plus('root')

#inicializar mi aplicacion de flask sql alchemy
#dentro de la aplicacion de flask tendremos nuestra conexion a  la base de datos
conexion.init_app(app)

Migrate(app=app, db=conexion)

# @app.route('/crear-tablas', methods=['GET'])
# def crearTablas():
#     # creara todas las tablas declaradas en el proyecto
#     conexion.create_all()
#     return {
#         'message':'Creacion ejecutada exitosamente'
#     }

if __name__=='__main__':
    app.run(debug=True)
    