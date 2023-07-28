from base_de_datos import conexion
from models.usuario import UsuarioModel
from flask_restful import Resource, request

class UsuariosController(Resource):
    def get(self):
        return{
            'message': 'Hola desde usuarios controller'
        }

    def post(self):
        data:dict = request.get_json()
        print(data)
        nuevoUsuario = UsuarioModel(nombre = data.get('nombre',''), 
                                    apellido = data.get('apellido',''), 
                                    correo = data.get('correo'), 
                                    telefono = data.get('telefono'), 
                                    linkedinUrl = data.get('linkedinUrl')
                                    )

        conexion.session.add(nuevoUsuario)
        conexion.session.commit()
        return{
            'message': 'Hola desde usuarios controller'
        }