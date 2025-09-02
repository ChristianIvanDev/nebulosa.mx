from django.db import models

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

# Create your models here.
class Usuario(AbstractUser):
    AbstractUser.username = models.CharField(max_length=150, verbose_name='Nombre Usuario')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_admin = models.BooleanField(default=False, verbose_name='Administrador')
    is_ventas = models.BooleanField(default=False, verbose_name='Ventas')
    # Campos para manejo de eliminación

    def puede_vender_boletos(self):
        """
        Retorna True si el usuario tiene permisos para vender boletos.
        """
        return self.is_ventas or self.is_admin

    def vender_boleto(self, evento, comprador, cantidad=1):
        """
        Lógica para vender boletos a un comprador para un evento.
        """
        if not self.puede_vender_boletos():
            raise PermissionError("No tienes permisos para vender boletos.")
        # Aquí deberías importar el modelo Boleto y registrar la venta
        from nebulosa.boletos.models import Boleto
        boletos = []
        for _ in range(cantidad):
            boleto = Boleto.objects.create(
                evento=evento,
                vendedor=self,
                comprador=comprador
            )
            boletos.append(boleto)
        return boletos

    def boletos_vendidos(self):
        """
        Retorna todos los boletos vendidos por este usuario.
        """
        from nebulosa.boletos.models import Boleto
        return Boleto.objects.filter(vendedor=self)

    def total_boletos_vendidos(self):
        """
        Retorna el número total de boletos vendidos por este usuario.
        """
        return self.boletos_vendidos().count()

