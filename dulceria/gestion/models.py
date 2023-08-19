from django.db import models
from uuid import uuid4

# Create your models here.

class CategoriModel(models.Model):

    opcionesNivelAzucar = (
        ['MA', 'MUY_ALTO'],
        ['ALTO', 'ALTO'],
        ['MEDIO', 'MEDIO'],
        ['BAJO', 'BAJO'],
        ['MUY_BAJO', 'MUY_BAJO'],
        ['CERO', 'CERO']
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.TextField(null=False)
    nivelAzucar = models.TextField(db_column='nivel_azucar', null=False, choices=opcionesNivelAzucar)

    class Meta:
        db_table = 'categorias'

class GolosinaModel(models.Model):
    tipoProcedencia = (
        ['NACIONAL', 'NACIONAL'],
        ['IMPORTADO', 'IMPORTADO']
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nombre = models.TextField(null=False)
    fechaVencimiento = models.DateField(editable=False, null=False, db_column='fecha_vencimiento')
    precio = models.FloatField(null=False)
    procedencia = models.TextField(choices=tipoProcedencia, default='NACIONAL')

    categoria = models.ForeignKey(to=CategoriModel, db_column='categoria_id', on_delete=models.PROTECT, 
                                  related_name='golosinas')
    
    class Meta:
        db_table = 'golosinas'
        unique_together = [['nombre', 'fechaVencimiento']]