from base_de_datos import conexion
from models.mascota import MascotaModel
from flask_restful import Resource, request

class MascotasController(Resource):
    def post(self):
        return{
            'message':'Mascotacreada exitosamente'
        },201