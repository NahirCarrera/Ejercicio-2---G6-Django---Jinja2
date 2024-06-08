from .forms import ProductoForm
from .models import Producto
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from django.contrib import messages
import csv

productos = []


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
            messages.error(request, "Por favor, suba un archivo CSV válido.")
            return redirect('/') 

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]  # Eliminamos la cabecera para no procesarla

        productos_importados = 0
        errores = []

        for line in lines:
            if line:
                fields = line.split(",")
                if len(fields) < 4:
                    errores.append(f"Faltan datos en la línea: {line[:50]}... (esperados 4, encontrados {len(fields)})")
                    continue

                try:
                    nombre = fields[0].strip()
                    precio = Decimal(fields[1].strip())
                    cantidad = int(fields[2].strip())
                    descripcion = fields[3].strip()

                    Producto.objects.create(nombre=nombre, precio=precio, cantidad=cantidad, descripcion=descripcion)
                    productos_importados += 1
                except (ValueError, InvalidOperation) as e:
                    errores.append(f"Error en la línea: {line[:50]}... {str(e)}")

        if errores:
            error_message = "Algunos productos no pudieron ser importados debido a errores.\n" + "\n".join(errores)
            messages.error(request, error_message)
        else:
            success_message = f"Productos importados correctamente: {productos_importados}"
            messages.success(request, success_message)

        return redirect('/') 

    return render(request, 'importar_csv.html')

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})