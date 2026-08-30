import csv

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FacturaForm, LineaFacturaFormSet
from .models import Cliente, Factura, ProductoServicio


def dashboard(request):
    clientes = Cliente.objects.filter(activo=True).count()
    productos = ProductoServicio.objects.filter(activo=True).count()
    facturas = Factura.objects.all().prefetch_related("lineas__producto")
    total_facturado = sum((factura.total for factura in facturas), 0)

    resumen = {
        "clientes": clientes,
        "productos": productos,
        "facturas_total": facturas.count(),
        "total_facturado": total_facturado,
    }

    facturas_recientes = facturas.order_by("-fecha")[:5]
    return render(
        request,
        "facturacion/dashboard.html",
        {"resumen": resumen, "facturas_recientes": facturas_recientes},
    )


def clientes_list(request):
    clientes = Cliente.objects.filter(activo=True).order_by("nombre")
    return render(request, "facturacion/clientes.html", {"clientes": clientes})


def productos_list(request):
    productos = ProductoServicio.objects.filter(activo=True).order_by("nombre")
    return render(request, "facturacion/productos.html", {"productos": productos})


def facturas_list(request):
    facturas = Factura.objects.select_related("cliente")

    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")
    cliente_id = request.GET.get("cliente", "")
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")

    if q:
        facturas = facturas.filter(numero__icontains=q) | facturas.filter(cliente__nombre__icontains=q)

    if estado:
        facturas = facturas.filter(estado=estado)

    if cliente_id:
        facturas = facturas.filter(cliente_id=cliente_id)

    if fecha_desde:
        facturas = facturas.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        facturas = facturas.filter(fecha__lte=fecha_hasta)

    facturas = facturas.order_by("-fecha", "-id")
    clientes = Cliente.objects.filter(activo=True).order_by("nombre")
    return render(
        request,
        "facturacion/facturas.html",
        {
            "facturas": facturas,
            "clientes": clientes,
            "filtro": {
                "q": q,
                "estado": estado,
                "cliente": cliente_id,
                "fecha_desde": fecha_desde,
                "fecha_hasta": fecha_hasta,
            },
        },
    )


def export_facturas_csv(request):
    facturas = Factura.objects.select_related("cliente")

    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "")
    cliente_id = request.GET.get("cliente", "")
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")

    if q:
        facturas = facturas.filter(numero__icontains=q) | facturas.filter(cliente__nombre__icontains=q)

    if estado:
        facturas = facturas.filter(estado=estado)

    if cliente_id:
        facturas = facturas.filter(cliente_id=cliente_id)

    if fecha_desde:
        facturas = facturas.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        facturas = facturas.filter(fecha__lte=fecha_hasta)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="facturas_cedimed.csv"'

    writer = csv.writer(response)
    writer.writerow(["Número", "Cliente", "Fecha", "Vence", "Estado", "Subtotal", "IVA", "Total"])

    for factura in facturas.order_by("-fecha", "-id"):
        writer.writerow(
            [
                factura.numero,
                factura.cliente.nombre,
                factura.fecha,
                factura.vence or "",
                factura.get_estado_display(),
                str(factura.subtotal),
                str(factura.iva_total),
                str(factura.total),
            ]
        )

    return response


def factura_detail(request, pk):
    factura = Factura.objects.select_related("cliente").prefetch_related("lineas__producto").get(pk=pk)
    return render(request, "facturacion/factura_detail.html", {"factura": factura})


def factura_new(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        formset = LineaFacturaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            factura = form.save()
            formset.instance = factura
            formset.save()
            messages.success(request, "Factura creada correctamente.")
            return redirect("factura_detail", pk=factura.pk)
    else:
        form = FacturaForm()
        formset = LineaFacturaFormSet()
    return render(
        request,
        "facturacion/factura_form.html",
        {"form": form, "formset": formset, "titulo": "Nueva factura"},
    )


def factura_edit(request, pk):
    factura = Factura.objects.get(pk=pk)
    if request.method == "POST":
        form = FacturaForm(request.POST, instance=factura)
        formset = LineaFacturaFormSet(request.POST, instance=factura)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Factura actualizada correctamente.")
            return redirect("factura_detail", pk=factura.pk)
    else:
        form = FacturaForm(instance=factura)
        formset = LineaFacturaFormSet(instance=factura)
    return render(
        request,
        "facturacion/factura_form.html",
        {"form": form, "formset": formset, "titulo": "Editar factura"},
    )


def factura_delete(request, pk):
    factura = Factura.objects.get(pk=pk)
    factura.delete()
    messages.success(request, "Factura eliminada.")
    return redirect(reverse("facturas_list"))


def clear_database(request):
    if request.method == "POST":
        Factura.objects.all().delete()
        LineaFactura.objects.all().delete()
        Cliente.objects.all().delete()
        ProductoServicio.objects.all().delete()
        messages.warning(request, "La base de datos ha sido vaciada.")
    return redirect(reverse("dashboard"))
