from django.shortcuts import render
from .models import Producto
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

from django.shortcuts import render
from .models import Producto
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def exportar_csv(request):
    # Crea la respuesta HTTP con el tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Precio', 'Cantidad'])  # Cabeceras

    productos = Producto.objects.all().values_list('nombre', 'precio', 'cantidad')
    for producto in productos:
        writer.writerow(producto)

    return response

def importar_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            return HttpResponse('<script>alert("Por favor, suba un archivo CSV."); window.location.href = "/";</script>')

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]  # Eliminamos la cabecera para no procesarla

        errores = []
        productos_importados = 0
        for line in lines:
            if line:  # Asegurarse de no procesar líneas vacías
                fields = line.split(",")
                try:
                    nombre = fields[0].strip()
                    precio = Decimal(fields[1].strip())
                    cantidad = int(fields[2].strip())

                    Producto.objects.create(nombre=nombre, precio=precio, cantidad=cantidad)
                    productos_importados += 1
                except (ValueError, InvalidOperation) as e:
                    errores.append(f"Error en la línea '{line}': {str(e)}")

        mensaje = f"Productos importados correctamente: {productos_importados}"
        if errores:
            mensaje += f" | Errores encontrados: <br>{'<br>'.join(errores)}"

        mensaje += '<script>alert("'+ mensaje +'"); window.location.href = "/";</script>'
        return HttpResponse(mensaje)

    return render(request, 'importar_csv.html')
from django.shortcuts import render
from .models import Producto
import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

productos = []

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def exportar_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Precio', 'Cantidad', 'Descripción'])  # Añadir descripción a la cabecera

    productos = Producto.objects.all().values_list('nombre', 'precio', 'cantidad', 'descripcion')
    for producto in productos:
        writer.writerow(producto)

    return response

def importar_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            return HttpResponse('<script>alert("Por favor, suba un archivo CSV."); window.location.href = "/";</script>')

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]  # Eliminamos la cabecera para no procesarla

        errores = []
        productos_importados = 0
        for line in lines:
            if line:  # Asegurarse de no procesar líneas vacías
                fields = line.split(",")
                # Verificar que cada línea tiene suficientes campos
                if len(fields) < 4:
                    errores.append(f"Faltan datos en la línea '{line}'. Esperados 4, encontrados {len(fields)}.")
                    continue
                
                try:
                    nombre = fields[0].strip()
                    precio = Decimal(fields[1].strip())
                    cantidad = int(fields[2].strip())
                    descripcion = fields[3].strip()

                    Producto.objects.create(nombre=nombre, precio=precio, cantidad=cantidad, descripcion=descripcion)
                    productos_importados += 1
                except (ValueError, InvalidOperation) as e:
                    errores.append(f"Error en la línea '{line}': {str(e)}")

        mensaje = f"Productos importados correctamente: {productos_importados}"
        if errores:
            mensaje += f" | Errores encontrados: <br>{'<br>'.join(errores)}"

            mensaje += '<script>alert("'+ mensaje +'"); window.location.href = "/";</script>'
        return HttpResponse(mensaje)

    return render(request, 'importar_csv.html')
