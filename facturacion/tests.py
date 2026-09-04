from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Factura, LineaFactura, ProductoServicio


class FacturacionTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test",
            nif="B12345678",
            email="cliente@test.com",
        )
        self.producto = ProductoServicio.objects.create(
            codigo="PROD-001",
            nombre="Servicio prueba",
            precio=Decimal("100.00"),
            iva=Decimal("21.00"),
        )
        self.factura = Factura.objects.create(
            numero="F-2026-100",
            cliente=self.cliente,
            estado="enviada",
        )
        LineaFactura.objects.create(
            factura=self.factura,
            producto=self.producto,
            descripcion="Servicio prueba",
            cantidad=2,
            precio_unitario=Decimal("100.00"),
            iva=Decimal("21.00"),
        )

    def test_factura_total_calculation(self):
        self.assertEqual(self.factura.subtotal, Decimal("200.00"))
        self.assertEqual(self.factura.iva_total, Decimal("42.00"))
        self.assertEqual(self.factura.total, Decimal("242.00"))

    def test_dashboard_total_facturado_uses_amounts_not_row_count(self):
        factura2 = Factura.objects.create(
            numero="F-2026-101",
            cliente=self.cliente,
            estado="pagada",
        )
        LineaFactura.objects.create(
            factura=factura2,
            producto=self.producto,
            descripcion="Servicio prueba 2",
            cantidad=1,
            precio_unitario=Decimal("50.00"),
            iva=Decimal("21.00"),
        )

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["resumen"]["total_facturado"], Decimal("242.00") + Decimal("60.50"))

    def test_facturas_filter_by_number_and_client(self):
        response = self.client.get(reverse("facturas_list"), {"q": "Cliente Test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.factura, response.context["facturas"])

        response2 = self.client.get(reverse("facturas_list"), {"q": "F-2026-100"})
        self.assertIn(self.factura, response2.context["facturas"])

    def test_cliente_can_be_edited_individually(self):
        response = self.client.post(
            reverse("cliente_edit", args=[self.cliente.pk]),
            {"nombre": "Cliente Actualizado", "nif": self.cliente.nif, "email": "nuevo@test.com", "telefono": "123", "direccion": "Calle 1", "activo": "on"},
        )
        self.assertRedirects(response, reverse("clientes_list"))
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nombre, "Cliente Actualizado")

    def test_product_delete_is_blocked_when_used_by_invoice(self):
        response = self.client.post(reverse("producto_delete", args=[self.producto.pk]))
        self.assertRedirects(response, reverse("productos_list"))
        self.assertTrue(ProductoServicio.objects.filter(pk=self.producto.pk).exists())

    def test_invoice_can_be_deleted_individually(self):
        response = self.client.post(reverse("factura_delete", args=[self.factura.pk]))
        self.assertRedirects(response, reverse("facturas_list"))
        self.assertFalse(Factura.objects.filter(pk=self.factura.pk).exists())
