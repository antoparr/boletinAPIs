from rest_framework import serializers

from .models import Usuario, Alquiler, Patinete


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class PatineteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patinete
        fields = '__all__'


class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
        fields = '__all__'
