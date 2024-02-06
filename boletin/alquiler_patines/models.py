from django.db import models
from django.contrib.auth.models import User
from rest_framework import permissions

class Patinete(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)
    precio_desbloqueo = models.DecimalField(max_digits=5, decimal_places=2)
    precio_minuto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.numero

class Alquiler(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    patinete = models.ForeignKey(Patinete, on_delete=models.CASCADE)
    fecha_desbloqueo = models.DateTimeField()
    fecha_entrega = models.DateTimeField()
    coste_final = models.DecimalField(max_digits=8, decimal_places=2)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debito = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite a los usuarios ver sus propios alquileres, pero solo permite a los administradores realizar otras operaciones
        if request.user and request.user.is_authenticated:
            return obj.usuario == request.user or request.user.is_staff
        return False
