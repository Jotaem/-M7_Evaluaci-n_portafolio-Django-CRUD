from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, F, Value, DecimalField
from django.db.models.functions import Coalesce
from django.views.decorators.http import require_http_methods

from .models import Producto, Categoria, Etiqueta, DetalleProducto
from .forms import (
    BusquedaProductoForm, ProductoForm, DetalleProductoForm,
    CategoriaForm, EtiquetaForm
)


# ============================================================================
# VISTAS DE PÁGINA DE INICIO
# ============================================================================

def index(request):
    """Vista principal con estadísticas del sistema"""
    productos_recientes = Producto.objects.select_related('categoria').order_by('-fecha_creacion')[:6]
    
    context = {
        'productos_recientes': productos_recientes,
        'total_productos': Producto.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_etiquetas': Etiqueta.objects.count(),
        'productos_disponibles': Producto.objects.filter(disponible=True, stock__gt=0).count(),
    }
    return render(request, 'biblioteca/index.html', context)


# ============================================================================
# VISTAS DE PRODUCTOS
# ============================================================================

def lista_productos(request):
    """Vista para listar productos con búsqueda y filtrado avanzado"""
    queryset = Producto.objects.select_related('categoria').prefetch_related('etiquetas')
    
    # Aplicar filtros
    nombre = request.GET.get('nombre', '').strip()
    categoria_id = request.GET.get('categoria', '')
    etiqueta_id = request.GET.get('etiqueta', '')
    precio_minimo = request.GET.get('precio_minimo', '')
    precio_maximo = request.GET.get('precio_maximo', '')
    disponible = request.GET.get('disponible', '')
    
    # Filtro por nombre
    if nombre:
        queryset = queryset.filter(
            Q(nombre__icontains=nombre) | Q(descripcion__icontains=nombre) | Q(codigo__icontains=nombre)
        )
    
    # Filtro por categoría
    if categoria_id:
        queryset = queryset.filter(categoria_id=categoria_id)
    
    # Filtro por etiqueta (Relación Muchos a Muchos)
    if etiqueta_id:
        queryset = queryset.filter(etiquetas__id=etiqueta_id).distinct()
    
    # Filtro por rango de precios (Consulta avanzada con ORM)
    if precio_minimo:
        queryset = queryset.filter(precio__gte=precio_minimo)
    if precio_maximo:
        queryset = queryset.filter(precio__lte=precio_maximo)
    
    # Filtro por disponibilidad
    if disponible:
        queryset = queryset.filter(disponible=True, stock__gt=0)
    
    # Ordenamiento
    ordenar_por = request.GET.get('ordenar', '-fecha_creacion')
    queryset = queryset.order_by(ordenar_por)
    
    # Contar productos únicos
    total_resultados = queryset.distinct().count()
    
    # Paginación
    from django.core.paginator import Paginator
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    form = BusquedaProductoForm(request.GET)
    
    context = {
        'productos': productos,
        'form': form,
        'total_resultados': total_resultados,
        'ordenar_por': ordenar_por,
    }
    return render(request, 'biblioteca/lista_libros.html', context)


def detalle_producto(request, id):
    """Vista para mostrar detalles de un producto con relaciones"""
    producto = get_object_or_404(
        Producto.objects.select_related('categoria').prefetch_related('etiquetas'),
        id=id
    )
    
    # Obtener detalles del producto (Relación Uno a Uno)
    detalle = getattr(producto, 'detalle', None)
    
    # Productos relacionados (misma categoría)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(id=producto.id).select_related('categoria')[:4]
    
    context = {
        'producto': producto,
        'detalle': detalle,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'biblioteca/detalle_libro.html', context)


def crear_producto(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        detalle_form = DetalleProductoForm(request.POST)
        
        if form.is_valid() and detalle_form.is_valid():
            producto = form.save()
            
            # Guardar detalles del producto (Relación Uno a Uno)
            detalle = detalle_form.save(commit=False)
            detalle.producto = producto
            detalle.save()
            
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('biblioteca:detalle_producto', id=producto.id)
    else:
        form = ProductoForm()
        detalle_form = DetalleProductoForm()
    
    context = {
        'form': form,
        'detalle_form': detalle_form,
        'titulo': 'Crear Producto'
    }
    return render(request, 'biblioteca/crear.html', context)


def editar_producto(request, id):
    """Vista para editar un producto existente"""
    producto = get_object_or_404(Producto, id=id)
    
    # Obtener o crear detalles
    try:
        detalle = producto.detalle
    except DetalleProducto.DoesNotExist:
        detalle = None
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        detalle_form = DetalleProductoForm(request.POST, instance=detalle) if detalle else DetalleProductoForm(request.POST)
        
        if form.is_valid() and detalle_form.is_valid():
            producto = form.save()
            
            detalle = detalle_form.save(commit=False)
            detalle.producto = producto
            detalle.save()
            
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('biblioteca:detalle_producto', id=producto.id)
    else:
        form = ProductoForm(instance=producto)
        detalle_form = DetalleProductoForm(instance=detalle) if detalle else DetalleProductoForm()
    
    context = {
        'form': form,
        'detalle_form': detalle_form,
        'producto': producto,
        'titulo': f'Editar {producto.nombre}'
    }
    return render(request, 'biblioteca/editar.html', context)


def eliminar_producto(request, id):
    """Vista para eliminar un producto"""
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect('biblioteca:lista_productos')
    
    context = {'producto': producto, 'tipo': 'producto'}
    return render(request, 'biblioteca/confirmar_eliminacion.html', context)


# ============================================================================
# VISTAS DE CATEGORÍAS
# ============================================================================

def lista_categorias(request):
    """Vista para listar todas las categorías"""
    # Consulta avanzada con anotaciones (contar productos por categoría)
    categorias = Categoria.objects.annotate(
        cantidad_productos=Count('productos')
    ).order_by('nombre')
    
    context = {
        'categorias': categorias,
        'total_categorias': categorias.count()
    }
    return render(request, 'biblioteca/lista_categorias.html', context)


def crear_categoria(request):
    """Vista para crear una nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('biblioteca:lista_categorias')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Categoría'
    }
    return render(request, 'biblioteca/crear_categoria.html', context)


def editar_categoria(request, id):
    """Vista para editar una categoría"""
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente.')
            return redirect('biblioteca:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': f'Editar {categoria.nombre}'
    }
    return render(request, 'biblioteca/editar_categoria.html', context)


def eliminar_categoria(request, id):
    """Vista para eliminar una categoría"""
    categoria = get_object_or_404(Categoria, id=id)
    
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada exitosamente.')
        return redirect('biblioteca:lista_categorias')
    
    # Contar productos en esta categoría
    cantidad_productos = categoria.productos.count()
    
    context = {
        'categoria': categoria,
        'tipo': 'categoría',
        'cantidad_productos': cantidad_productos
    }
    return render(request, 'biblioteca/confirmar_eliminacion.html', context)


# ============================================================================
# VISTAS DE ETIQUETAS
# ============================================================================

def lista_etiquetas(request):
    """Vista para listar todas las etiquetas"""
    # Consulta avanzada con anotaciones (contar productos por etiqueta)
    etiquetas = Etiqueta.objects.annotate(
        cantidad_productos=Count('productos')
    ).order_by('nombre')
    
    context = {
        'etiquetas': etiquetas,
        'total_etiquetas': etiquetas.count()
    }
    return render(request, 'biblioteca/lista_etiquetas.html', context)


def crear_etiqueta(request):
    """Vista para crear una nueva etiqueta"""
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            etiqueta = form.save()
            messages.success(request, f'Etiqueta "{etiqueta.nombre}" creada exitosamente.')
            return redirect('biblioteca:lista_etiquetas')
    else:
        form = EtiquetaForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Etiqueta'
    }
    return render(request, 'biblioteca/crear_etiqueta.html', context)


def editar_etiqueta(request, id):
    """Vista para editar una etiqueta"""
    etiqueta = get_object_or_404(Etiqueta, id=id)
    
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            etiqueta = form.save()
            messages.success(request, f'Etiqueta "{etiqueta.nombre}" actualizada exitosamente.')
            return redirect('biblioteca:lista_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    
    context = {
        'form': form,
        'etiqueta': etiqueta,
        'titulo': f'Editar {etiqueta.nombre}'
    }
    return render(request, 'biblioteca/editar_etiqueta.html', context)


def eliminar_etiqueta(request, id):
    """Vista para eliminar una etiqueta"""
    etiqueta = get_object_or_404(Etiqueta, id=id)
    
    if request.method == 'POST':
        nombre = etiqueta.nombre
        etiqueta.delete()
        messages.success(request, f'Etiqueta "{nombre}" eliminada exitosamente.')
        return redirect('biblioteca:lista_etiquetas')
    
    # Contar productos con esta etiqueta
    cantidad_productos = etiqueta.productos.count()
    
    context = {
        'etiqueta': etiqueta,
        'tipo': 'etiqueta',
        'cantidad_productos': cantidad_productos
    }
    return render(request, 'biblioteca/confirmar_eliminacion.html', context)

