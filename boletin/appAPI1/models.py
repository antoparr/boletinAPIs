from django.db import models


# Create your models here.

class Marca(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Marcas"


class Vehiculo(models.Model):
    TIPO_CHOICES = (
        ('COCHE', 'Coche'),
        ('CICLO', 'Ciclomotor'),
        ('MOTO', 'Motocicleta'),
    )

    COLOR_CHOICES = (
        ('ROJO', 'Rojo'),
        ('AZUL', 'Azul'),
        ('VERDE', 'Verde'),
        ('NEGRO', 'Negro'),
        ('GRIS', 'Gris'),
        ('BLANCO', 'Blanco'),
        ('OTRO', 'Otro'),
        # Agrega más colores según sea necesario
    )

    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    chasis = models.CharField(max_length=50, unique=True)
    marca = models.ForeignKey(Marca, models.PROTECT)
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    fecha_fabricacion = models.DateField()
    fecha_matriculacion = models.DateField()
    fecha_baja = models.DateField(null=True, blank=True)
    suspendido = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo_vehiculo} - {self.modelo} - {self.matricula}"

    class Meta:
        verbose_name_plural = "Vehiculos"


