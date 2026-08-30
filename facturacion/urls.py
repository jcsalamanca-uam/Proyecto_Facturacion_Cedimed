from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clientes/", views.clientes_list, name="clientes_list"),
    path("productos/", views.productos_list, name="productos_list"),
    path("facturas/", views.facturas_list, name="facturas_list"),
    path("facturas/exportar/", views.export_facturas_csv, name="export_facturas_csv"),
    path("facturas/nueva/", views.factura_new, name="factura_new"),
    path("facturas/<int:pk>/", views.factura_detail, name="factura_detail"),
    path("facturas/<int:pk>/editar/", views.factura_edit, name="factura_edit"),
    path("facturas/<int:pk>/eliminar/", views.factura_delete, name="factura_delete"),
]
