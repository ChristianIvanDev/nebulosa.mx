from django.db import models

class Boleto(models.Model):
    # Datos del comprador (guardados en el boleto)
    comprador_nombre = models.CharField(max_length=150, verbose_name="Nombre del Comprador")
    comprador_email = models.EmailField(verbose_name="Correo del Comprador")
    comprador_tel = models.CharField(max_length=30, blank=True, verbose_name="Teléfono")
    tipo_venta = "Stripe"
    
    # STRIPE USAR
    
    ESTADOS = (
        ("vendido", "Vendido"),
        ("usado", "Usado / Check-in")
    )

    # Vendedor (tu usuario); el comprador NO es usuario del sistema
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True, related_name="boletos_vendidos"
    )

    
    # Info del “tipo” de boleto sin modelo extra (simple y directo)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        base = f"{self.codigo} — {self.comprador_nombre}"
        if self.categoria:
            base += f" — {self.categoria}"
        return base

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:16].upper()
        super().save(*args, **kwargs)

    def marcar_usado(self):
        if self.estado == "vendido":
            self.estado = "usado"
            self.save(update_fields=["estado"])
            return True
        return False

    def es_valido(self):
        return self.estado == "vendido"