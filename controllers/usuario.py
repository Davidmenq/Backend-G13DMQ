from models import UsuarioModel
from utilitarios import conexion
from flask_restful import Resource, request
from dtos import UsuarioRequestDto, UsuarioResponseDto
from bcrypt import gensalt, hashpw

class RegistroController(Resource):
    def post(self):
        try:
            dto = UsuarioRequestDto()
            dataValidada = dto.load(request.get_json())
           

            salt =gensalt()

            password = dataValidada.get('password')

            passwordBytes = bytes(password, 'utf-8')

            passwordHasheada = hashpw(passwordBytes,salt).decode('utf-8')

            dataValidada['password']=passwordHasheada

            nuevoUsuario = UsuarioModel(**dataValidada)

            conexion.session.add(nuevoUsuario)
            conexion.session.commit()

            dtoResponse = UsuarioResponseDto()

            return {
                'message': 'Usuario creado exitosamente',
                'conten': dtoResponse.dump(nuevoUsuario)
            }, 201
        except Exception as e:
            return {
                'message': 'Error al crear el usuario',
                'content': e.args
            }, 400