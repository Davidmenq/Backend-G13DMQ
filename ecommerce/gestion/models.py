from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CategoriaModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    nombre = models.TextField(null=False, unique=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')

    class Meta:
        db_table = 'categorias'

class VehiculoModel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    placa = models.CharField(max_length=6, unique=True, null=False)
    numeroSerie = models.TextField(unique=True, null=False, db_column='num_serie')
    color = models.TextField()
    puertas = models.IntegerField(null=False)
    peso = models.FloatField()
    dimensiones = models.JSONField()
    anioFabricacion = models.TextField(db_column='anio_fabricaion')
    categoria = models.ForeignKey(to=CategoriaModel, on_delete=models.PROTECT, db_column='categoria_id')

    class Meta:
        db_table = 'vehiculos'

class UsuarioModel(AbstractBaseUser):
    tipoUsuario = [('ADMINISTRADOR', 'ADMINISTRADOR'), ('CLIENTE', 'CLIENTE')]

    id = models.UUIDField(default=uuid4, primary_key=True)
    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)
    correo = models.EmailField(unique=True, null=False)
    password = models.TextField(null=False)
    fechaCreacion = models.DateTimeField(auto_now_add=True,db_column='fecha_creacion')
    fechaActualizacion = models.DateTimeField(auto_now=True,db_column='fecha_actualizacion')
    tipo = models.TextField(choices=tipoUsuario, default='CLIENTE')
    tipoDocumento = models.TextField(db_column='tipo_documento')
    numeroDocumento = models.TextField(db_column='numero_documento')
    telefono = PhoneNumberField(region='PE')
    
    # Columnas necesarias para trabajar con el panel administrativo
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # para realizar el login en el panel administrativo le indico cual sera la columna para identificar al usuario
    USERNAME_FIELD = 'correo'
    
    #indicara los campos que se deben pedir al momento de crear el super usuario por la terminal
    REQUIRED_FIELDS = ['nombre', 'apellido']
    class Meta:
        db_table = 'usuarios'

class CitaModel(models.Model):
    id = models. UUIDField(default=uuid4, primary_key=True)
    dia = models.IntegerField(null=False)
    hora = models.TimeField(null=False)
    vehiculo = models.ForeignKey(to=VehiculoModel,on_delete=models.CASCADE, db_column='vehiculo_id')
    usuario = models.ForeignKey(to=UsuarioModel, on_delete=models.CASCADE, db_column='usuario_id')

    class Meta:
        db_table = 'citas'
        unique_together = [['usuario', 'dia', 'hora']]