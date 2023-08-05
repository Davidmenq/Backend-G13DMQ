from models import UsuarioModel
from utilitarios import conexion
from flask_restful import Resource, request
from dtos import UsuarioRequestDto, UsuarioResponseDto, LoginRequestDto
from bcrypt import gensalt, hashpw, checkpw

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
        
class LoginController(Resource):
    def post(self):
        dto = LoginRequestDto()
        try:
            dataValidada = dto.load(request.get_json())
            usuarioEncontrado = conexion.session.query(UsuarioModel).filter_by(correo = dataValidada.get('correo')).first()
            if not usuarioEncontrado:
                return {
                    'message': 'El usuario no existe'
                },400
            
            password = bytes(usuarioEncontrado.password, 'utf-8')
            passwordEntrante = bytes(dataValidada.get('password'), 'utf-8')

            resultado = checkpw(passwordEntrante, password)

            if resultado == False:
                return{
                    'message': 'credenciales incorrectas'

                },400
            return{
                'message': 'Bienvenido si eres'
            }
            
        except Exception as e:
            return {
                'message': 'error al hacer login',
                'content': e.args
            }, 400
           

