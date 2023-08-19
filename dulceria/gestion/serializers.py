from rest_framework import serializers
from .models import CategoriModel

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriModel
        # si utilizas todos los atributos del modelo entonces se usa la sigueiente forma
        fields = '__all__'
        # se puede utilizar el atributo exclude para excluir algun atributo, pero sin usar el atrib field
        # exclude = ['id']