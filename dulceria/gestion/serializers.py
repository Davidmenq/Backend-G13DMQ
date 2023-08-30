from rest_framework import serializers
from .models import CategoriModel, GolosinaModel

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriModel
        # si utilizas todos los atributos del modelo entonces se usa la sigueiente forma
        fields = '__all__'
        # se puede utilizar el atributo exclude para excluir algun atributo, pero sin usar el atrib field
        # exclude = ['id']

class GolosinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GolosinaModel
        fields = '__all__'

class GolosinaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GolosinaModel
        fields = '__all__'
        # depth sirve para indicar cuantos niveles queremos recorrer
        depth = 1

class CategoriaResponseSerializer(serializers.ModelSerializer):
    golosinass = GolosinaSerializer(many=True, source='golosinas')#se agrego source para que acepte un nombre de variable diferente al related_name
    class Meta:
        model = CategoriModel
        fields = '__all__'
