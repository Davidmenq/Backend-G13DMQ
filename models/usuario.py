from sqlalchemy import Column, types
from base_de_datos import conexion

#Model > sirve para indicar que esta clase se convertira en un modelo y por
#ende creara la tabla respectiva en la base de datos
class UsuarioModel(conexion.Model):
    id= Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    apellido = Column(type_=types.Text)
    correo = Column(type_=types.Text, unique=True, nullable=False)
    telefono = Column(type_=types.Text, nullable=True)
    linkedinUrl = Column(name='linkedin_url', type_=types.Text)

#__tablename__ > sirve para indicar el nombre de la tabla en la base de datos, si no
#se le proporciona usara el nombre de la clase
__tablename__='usuarios'
