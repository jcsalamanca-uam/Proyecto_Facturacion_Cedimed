from decimal import Decimal

from django.core.management.base import BaseCommand

from facturacion.models import Cliente, Factura, LineaFactura, ProductoServicio


class Command(BaseCommand):
    help = "Crea datos de ejemplo para la aplicación de facturación"

    def handle(self, *args, **options):
        Factura.objects.all().delete()
        Cliente.objects.all().delete()
        ProductoServicio.objects.all().delete()

        clientes = [
            Cliente.objects.create(
                nombre="Hospital General",
                nif="B12345678",
                email="facturas@hospitalgeneral.com",
                telefono="912345678",
                direccion="Calle Real 12, Madrid",
            ),
            Cliente.objects.create(
                nombre="Clínica San Vicente",
                nif="B87654321",
                email="admin@clinicasanvicente.es",
                telefono="913456789",
                direccion="Avenida Mayor 45, Barcelona",
            ),
            Cliente.objects.create(
                nombre="Centro Médico Norte",
                nif="B11223344",
                email="compras@centromediconorte.es",
                telefono="914567890",
                direccion="Plaza de la Paz 8, Valencia",
            ),
        ]

        productos = [
            ProductoServicio.objects.create(
                codigo="CONS-001",
                nombre="Consulta médica general",
                descripcion="Consulta con médico general",
                precio=Decimal("120.00"),
                iva=Decimal("21.00"),
            ),
            ProductoServicio.objects.create(
                codigo="ANAL-010",
                nombre="Análisis de sangre",
                descripcion="Estudio analítico básico",
                precio=Decimal("65.00"),
                iva=Decimal("21.00"),
            ),
            ProductoServicio.objects.create(
                codigo="RAIO-025",
                nombre="Radiografía torácica",
                descripcion="Servicio de radiología",
                precio=Decimal("180.00"),
                iva=Decimal("21.00"),
            ),
            ProductoServicio.objects.create(
                codigo="FISI-100",
                nombre="Sesión fisioterapia",
                descripcion="Sesión de rehabilitación",
                precio=Decimal("90.00"),
                iva=Decimal("21.00"),
            ),
        ]

        factura1 = Factura.objects.create(
            numero="F-2026-001",
            cliente=clientes[0],
            estado="enviada",
            observaciones="Factura mensual de servicios.",
        )
        LineaFactura.objects.create(
            factura=factura1,
            producto=productos[0],
            descripcion=productos[0].nombre,
            cantidad=2,
            precio_unitario=productos[0].precio,
            iva=productos[0].iva,
        )
        LineaFactura.objects.create(
            factura=factura1,
            producto=productos[2],
            descripcion=productos[2].nombre,
            cantidad=1,
            precio_unitario=productos[2].precio,
            iva=productos[2].iva,
        )

        factura2 = Factura.objects.create(
            numero="F-2026-002",
            cliente=clientes[1],
            estado="pagada",
            observaciones="Pagada por transferencia bancaria.",
        )
        LineaFactura.objects.create(
            factura=factura2,
            producto=productos[1],
            descripcion=productos[1].nombre,
            cantidad=3,
            precio_unitario=productos[1].precio,
            iva=productos[1].iva,
        )
        LineaFactura.objects.create(
            factura=factura2,
            producto=productos[3],
            descripcion=productos[3].nombre,
            cantidad=2,
            precio_unitario=productos[3].precio,
            iva=productos[3].iva,
        )

        self.stdout.write(self.style.SUCCESS("Datos demo creados correctamente."))
