# Proyecto de Facturación Cedimed

Sistema de facturación y gestión comercial desarrollado con Django.

## Requisitos

- Python 3.11+
- pip

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# o .venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

## Funcionalidades

- Gestión de clientes
- Gestión de productos y servicios
- Creación de facturas con líneas de detalle
- Cálculo automático de subtotal, IVA e importe total
- Dashboard resumen
- Estado de facturas: borrador, enviada, pagada, vencida

## Acceso

La aplicación queda disponible en:

- http://127.0.0.1:8000/

## Datos de ejemplo

Se pueden cargar datos demo con el comando:

```bash
python manage.py seed_demo_data
```
