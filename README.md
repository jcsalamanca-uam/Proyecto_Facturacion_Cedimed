# Cedimed Facturación

Esta es una aplicación sencilla para gestionar clientes, productos y facturas.

## ¿Para qué sirve?

Te ayuda a:
- guardar clientes
- guardar productos o servicios
- crear facturas
- ver el total y el IVA
- exportar la información a CSV
- dejar la base de datos vacía si quieres empezar de cero

## Requisitos

Necesitas tener instalado:
- Python 3.11 o superior
- Internet para instalar paquetes

## Instalación rápida

1. Descarga el proyecto
2. Abre una ventana de PowerShell dentro de la carpeta del proyecto
3. Ejecuta estos comandos:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

4. Abre esta dirección en el navegador:

```text
http://127.0.0.1:8000/
```

## Si quieres empezar desde cero

La aplicación viene sin datos de ejemplo, lista para usar desde el principio.

Si en algún momento quieres borrar todo lo que has introducido, usa el botón:
- Vaciar base de datos

Antes de borrarlo la aplicación te pedirá confirmación para que no se borre por accidente.

## Editar o eliminar datos individuales

Desde las pantallas de **Clientes** y **Productos** puedes:
- crear registros nuevos
- editar cualquier registro existente
- eliminar un registro individual, confirmando la acción

En **Facturas** puedes editar o eliminar cada factura desde sus acciones. Al editarla también puedes cambiar o quitar sus líneas.

Para conservar la información histórica, no se permite eliminar un cliente que tenga facturas asociadas ni un producto que aparezca en una factura. En esos casos puedes editarlo o desactivarlo.

## Importante

Esta aplicación usa SQLite, que es un archivo local muy fácil de manejar. No hace falta PostgreSQL.

## ¿Qué pasa si quiero limpiar todo?

Pulsa el botón “Vaciar base de datos” desde la izquierda y confirma.

Eso borra:
- clientes
- productos
- facturas

## Si quieres volver a arrancar la app

```powershell
cd ruta\al\proyecto
.\.venv\Scripts\activate
python manage.py runserver
```

## Dificultad

Es una aplicación fácil de usar para alguien sin experiencia técnica. Solo necesita abrir el navegador y usar las pantallas.
