from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from models import UsuarioModel, TipoUsuario
from marshmallow_enum import EnumField

class UsuarioRequestDto(SQLAlchemyAutoSchema):
    correo = fields.Email()
    class Meta:
        model = UsuarioModel

class UsuarioResponseDto(SQLAlchemyAutoSchema):
    tipoUsuario = EnumField(TipoUsuario)
    class Meta:
        model = UsuarioModel