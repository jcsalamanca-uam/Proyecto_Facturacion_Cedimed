from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("clientes/", views.clientes_list, name="clientes_list"),
    path("clientes/nuevo/", views.cliente_form, name="cliente_new"),
    path("clientes/<int:pk>/editar/", views.cliente_form, name="cliente_edit"),
    path("clientes/<int:pk>/eliminar/", views.cliente_delete, name="cliente_delete"),
    path("productos/", views.productos_list, name="productos_list"),
    path("productos/nuevo/", views.producto_form, name="producto_new"),
    path("productos/<int:pk>/editar/", views.producto_form, name="producto_edit"),
    path("productos/<int:pk>/eliminar/", views.producto_delete, name="producto_delete"),
    path("facturas/", views.facturas_list, name="facturas_list"),
    path("facturas/exportar/", views.export_facturas_csv, name="export_facturas_csv"),
    path("facturas/nueva/", views.factura_new, name="factura_new"),
    path("facturas/<int:pk>/", views.factura_detail, name="factura_detail"),
    path("facturas/<int:pk>/editar/", views.factura_edit, name="factura_edit"),
    path("facturas/<int:pk>/eliminar/", views.factura_delete, name="factura_delete"),
    path("vaciar-base-datos/", views.clear_database, name="clear_database"),
]
