from django.db import models

# Create your models here.


class Client(models.Model):
    sucursal = models.CharField(max_length=5)
    cartera = models.CharField(max_length=6)
    clientes = models.CharField(max_length=150)
    fecha_alta = models.CharField(max_length=10, default='')
    saldo = models.FloatField()

    def __str__(self):
        return self.clientes
