from django.contrib import admin

from .models import Cliente, Factura, LineaFactura, ProductoServicio


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre", "nif", "email", "activo"]
    search_fields = ["nombre", "nif"]


@admin.register(ProductoServicio)
class ProductoServicioAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre", "precio", "iva", "activo"]
    search_fields = ["codigo", "nombre"]


class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ["numero", "cliente", "fecha", "estado", "total"]
    inlines = [LineaFacturaInline]
    list_filter = ["estado", "fecha"]
    search_fields = ["numero", "cliente__nombre"]
