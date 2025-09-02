from django.db import models

class Boleto_efectivo(models.Model):
    # Datos del comprador (guardados en el boleto)
    comprador_nombre = models.CharField(max_length=150, verbose_name="Nombre del Comprador")
    comprador_email = models.EmailField(verbose_name="Correo del Comprador")
    comprador_tel = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    tipo_venta = "Efectivo"
    creado_en = models.DateTimeField(auto_now_add=True)