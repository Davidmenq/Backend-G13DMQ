from base_de_datos import conexion
from models.usuario import UsuarioModel
from flask_restful import Resource, request
from dtos.usuario import UsuarioRequestDTO
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

class UsuariosController(Resource):
    def get(self):
        usuarios = conexion.session.query(UsuarioModel).all()
        dto = UsuarioRequestDTO()
        resultado = dto.dump(usuarios, many =True)
        
        print(usuarios)
        print(resultado)
        # for usuario in usuarios:
        #     print(usuario.nombre)
        #     print(usuario.correo)        
        return{
            'content': resultado
        }

    def post(self):
        data:dict = request.get_json()
        print(data)
        dto = UsuarioRequestDTO()
        try:
            dataValidada = dto.load(data)
            print(dataValidada)

            nuevoUsuario = UsuarioModel(**dataValidada)
            # nuevoUsuario = UsuarioModel(nombre = data.get('nombre',''), 
            #                             apellido = data.get('apellido',''), 
            #                             correo = data.get('correo'), 
            #                             telefono = data.get('telefono'), 
            #                             linkedinUrl = data.get('linkedinUrl')
            #                             )

            conexion.session.add(nuevoUsuario)
            conexion.session.commit()
            return{
                'message': 'usuario creado exitosamente'
            }, 201
        
        except ValidationError as error:
            return{
                'message':"Error al crear el usuario",
                'content': error.args
            }, 400
        
        except IntegrityError as error:
            return {
                'message': 'Error al crear el usuario',
                'content': 'El usuario ya existe'
            }, 400
        
        except Exception as error:
            return{
                'message': 'Error al crear el usuario',
                'content': error.args
            }, 400
        
class UsuarioController(Resource):
    def put(self, id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return{
                'message': 'El usuario a actualizar no existe'
            }, 404
        
        data =request.get_json()
        dto = UsuarioRequestDTO()
        try:
            dataValidada = dto.load(data)
            usuarioActualizados = conexion.session.query(UsuarioModel).filter_by(id=id).update(dataValidada)
            print(usuarioActualizados)
            conexion.session.commit()
            return{
                'message':'Usuario actualizado exitosamente'
            }
        except ValidationError as error:
            return{
                'message':'Error al actualizar el usuario',
                'content': error.args
            }
        except IntegrityError as error:
            return{
                'message':'Error al actualizar el usuario',
                'content':'Usuario con ese correo ya existe'
            }
        
    def delete(self, id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return{
                'message':'El usuario no existe'
            }, 404
        
        conexion.session.query(UsuarioModel).filter_by(id=id).delete()
        conexion.session.commit()
        return{
            'message': 'Usuario eliminado exitosamente'
        }
    
    def get(self, id):
        usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(id=id).first()
        if not usuarioEncontrado:
            return{
                'message':'El usuario no existe'
            },404
        
        dto = UsuarioRequestDTO()
        usuarioConvertido = dto.dump(usuarioEncontrado)

        return{
            'content': usuarioConvertido
        }
