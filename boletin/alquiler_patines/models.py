# gestion_alquiler/models.py
from django.db import models
from django.contrib.auth.models import User


class Patinete(models.Model):
    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
    precio_desbloqueo = models.DecimalField(max_digits=5, decimal_places=2)
    precio_minuto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.numero} - {self.tipo}"


class Alquiler(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    patinete = models.ForeignKey(Patinete, on_delete=models.CASCADE)
    fecha_desbloqueo = models.DateTimeField()
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    coste_final = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.patinete}"


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    debito = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}"
