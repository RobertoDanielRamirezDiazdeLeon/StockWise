from django.db import models
from django.contrib.auth.models import User  # 👈 importa User

class Contact(models.Model):
    # Imagen del producto
    avatar = models.ImageField(
        upload_to='contact', null=True, blank=True, verbose_name="Imagen del producto"
    )

    # Datos principales
    code = models.CharField(
        max_length=30, unique=True, verbose_name="Código"
    )
    product = models.CharField(
        max_length=100, verbose_name="Nombre del producto"
    )
    category = models.CharField(
        max_length=50, verbose_name="Categoría",
        choices=[
            ("PAN", "Panadería"),
            ("BEB", "Bebidas"),
            ("LIM", "Limpieza"),
            ("OTR", "Otros"),
        ]
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Precio de venta"
    )
    stock = models.PositiveIntegerField(
        default=0, null=True, blank=True, verbose_name="Stock disponible"
    )
    supplier = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Proveedor"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Descripción"
    )

    # Fechas
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Última actualización"
    )

    # 🔹 Nuevos campos para auditoría
    created_by = models.ForeignKey(
        User, null=True, blank=True,
        related_name="contacts_created",
        on_delete=models.SET_NULL,
        verbose_name="Creado por"
    )
    updated_by = models.ForeignKey(
        User, null=True, blank=True,
        related_name="contacts_updated",
        on_delete=models.SET_NULL,
        verbose_name="Actualizado por"
    )

    def __str__(self):
        return f"{self.code} - {self.product}"
