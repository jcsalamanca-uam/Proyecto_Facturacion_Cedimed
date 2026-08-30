from decimal import Decimal

from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    nif = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.nif})"


class ProductoServicio(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("21.00"))
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Factura(models.Model):
    ESTADO_BORRADOR = "borrador"
    ESTADO_ENVIADA = "enviada"
    ESTADO_PAGADA = "pagada"
    ESTADO_VENCIDA = "vencida"
    ESTADOS = [
        (ESTADO_BORRADOR, "Borrador"),
        (ESTADO_ENVIADA, "Enviada"),
        (ESTADO_PAGADA, "Pagada"),
        (ESTADO_VENCIDA, "Vencida"),
    ]

    numero = models.CharField(max_length=30, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="facturas")
    fecha = models.DateField(default=timezone.now)
    vence = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_BORRADOR)
    observaciones = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "-id"]

    @property
    def subtotal(self):
        return sum((linea.cantidad * linea.precio_unitario) for linea in self.lineas.all())

    @property
    def iva_total(self):
        return sum((linea.importe_iva) for linea in self.lineas.all())

    @property
    def total(self):
        return self.subtotal + self.iva_total

    def __str__(self):
        return f"Factura {self.numero} - {self.cliente.nombre}"


class LineaFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="lineas")
    producto = models.ForeignKey(ProductoServicio, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=255, blank=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("21.00"))

    class Meta:
        ordering = ["id"]

    @property
    def importe_base(self):
        return self.cantidad * self.precio_unitario

    @property
    def importe_iva(self):
        return (self.importe_base * self.iva) / Decimal("100")

    @property
    def total_linea(self):
        return self.importe_base + self.importe_iva

    def __str__(self):
        return f"{self.factura.numero} - {self.producto.nombre}"
