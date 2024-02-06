from rest_framework import serializers
from .models import Marca, Vehiculo

class MarcaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Marca
        fields = ['nombre']

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['tipo_vehiculo', 'chasis', 'marca', 'modelo', 'matricula', 'color', 'fecha_fabricacion', 'fecha_matriculacion', 'fecha_baja', 'suspendido']