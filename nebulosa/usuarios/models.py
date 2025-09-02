# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # NO modifiques AbstractUser.username globalmente.
    # En su lugar, redefine el campo en tu subclass.
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Nombre de usuario'
    )

    # AbstractUser YA trae is_staff, is_superuser, is_active.
    # No vuelvas a declararlos. Agrega solo los tuyos:
    is_admin = models.BooleanField(default=False, verbose_name='Administrador')
    is_ventas = models.BooleanField(default=False, verbose_name='Ventas')

    def puede_vender_boletos(self):
        return self.is_ventas or self.is_admin or self.is_staff or self.is_superuser

    def vender_boleto(self, evento, comprador, cantidad=1):
        if not self.puede_vender_boletos():
            raise PermissionError("No tienes permisos para vender boletos.")
        # Import correcto del app (no uses 'nebulosa.boletos...')
        from boletos.models import Boleto
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
        from boletos.models import Boleto
        return Boleto.objects.filter(vendedor=self)

    def total_boletos_vendidos(self):
        return self.boletos_vendidos().count()
