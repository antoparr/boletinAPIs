from rest_framework import serializers
from .models import Patinete, Alquiler


class PatineteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patinete
        fields = ['id', 'numero', 'tipo', 'precio_desbloqueo', 'precio_minuto']


class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
        fields = ['id', 'usuario', 'patinete', 'fecha_desbloqueo', 'fecha_entrega', 'coste_final']