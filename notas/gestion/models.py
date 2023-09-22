from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class ManejadorUsuario(BaseUserManager):
    def create_superuser(self, correo, nombre, password):
        if not correo:
            raise ValueError('El usuario debe tener un correo')
        
        correo_normalizado = self.normalize_email(correo)
        admin = self.model(correo=correo_normalizado, nombre=nombre)
        admin.set_password(password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()


class Usuario(AbstractBaseUser, PermissionsMixin):
    id= models.AutoField(primary_key=True)
    correo= models.EmailField(unique=True, null=False)
    nombre= models.TextField()
    apellido= models.TextField()
    fechaCreacion= models.DateField(
        auto_now_add=True, db_column='fecha_creacion')

    # Para trabajar con el panel administrativo
    is_taff= models.BooleanField(default=False)

    is_active= models.BooleanField(default=True)

    #hacer login en el panel administrativo
    USERNAME_FIELD= 'correo'

    # columnas requeridas para usuarios por consola
    REQUIRED_FIELDS = ['nombre']

    objects=ManejadorUsuario()

    class Meta:
        db_table = 'usuarios'

class Nota(models.Model):
    id= models.AutoField(primary_key=True)
    titulo= models.TextField(null=False)
    descripcion= models.TextField()
    tipo= models.TextField(choices=(('LISTA','LISTA'), ('TEXTO', 'TEXTO')))
    imagen= models.ImageField(upload_to='imagenes_notas/', null=True)
    fechaCreacion= models.DateTimeField(
        auto_now_add=True, db_column='fecha_creacion')
    fechaActualizacion= models.DateTimeField(
        auto_now=True, db_column='fecha_actualizacion')

    usuario =  models.ForeignKey(to=Usuario, on_delete=models.PROTECT, db_column='usuario_id')
    
    class Meta:
        db_table= 'notas'

class Item(models.Model):
    titulo= models.TextField(null=False)
    completado= models.BooleanField(default=False)
    fechaCreacion= models.DateTimeField(
        auto_now_add=True, db_column='fecha_creacion')
    
    nota=models.ForeignKey(
        to=Nota, on_delete=models.PROTECT, db_column='nota_id'
    )
    class Meta:
        db_table = 'items'


