from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.usuario import UsuarioModel

class UsuarioRequestDTO(SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        