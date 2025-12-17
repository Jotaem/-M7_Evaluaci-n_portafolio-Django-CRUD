from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Libro, Autor, Categoria, Etiqueta, Prestamo, PerfilUsuario
from .forms import (
    RegistroUsuarioForm, LoginForm, LibroForm, CategoriaForm, 
    EtiquetaForm, BusquedaLibroForm, PerfilUsuarioForm
)

# ============================================================================
# VISTAS PÚBLICAS
# ============================================================================

def index(request):
    """Vista principal con estadísticas y libros recientes."""
    libros_recientes = Libro.objects.select_related('categoria').prefetch_related('autores').order_by('-fecha_agregado')[:6]
    context = {
        'libros_recientes': libros_recientes,
        'total_libros': Libro.objects.count(),
        'total_autores': Autor.objects.count(),
        'total_categorias': Categoria.objects.count(),
    }
    return render(request, 'biblioteca/index.html', context)

def acerca_de(request):
    """Vista para la página 'Acerca de'."""
    return render(request, 'biblioteca/acerca_de.html')

# ============================================================================
# VISTAS DE AUTENTICACIÓN
# ============================================================================

def registro_usuario(request):
    """Vista para el registro de nuevos usuarios."""
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(user=user) # Crea un perfil vacío
            login(request, user)
            messages.success(request, '¡Te has registrado exitosamente!')
            return redirect('biblioteca:index')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'biblioteca/registro.html', {'form': form})

def login_usuario(request):
    """Vista para el inicio de sesión de usuarios."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('biblioteca:index')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'biblioteca/login.html', {'form': form})

@login_required
def logout_usuario(request):
    """Vista para cerrar la sesión del usuario."""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('biblioteca:index')

# ============================================================================
# VISTAS DE USUARIO Y PRÉSTAMOS
# ============================================================================

@login_required
def perfil_usuario(request):
    """Vista para ver y editar el perfil del usuario."""
    perfil, created = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('biblioteca:perfil_usuario')
    else:
        form = PerfilUsuarioForm(instance=perfil)
    return render(request, 'biblioteca/perfil_usuario.html', {'form': form})

@login_required
def mis_prestamos(request):
    """Vista para que el usuario vea sus préstamos."""
    prestamos = Prestamo.objects.filter(usuario=request.user).select_related('libro').order_by('-fecha_prestamo')
    return render(request, 'biblioteca/mis_prestamos.html', {'prestamos': prestamos})

@login_required
def solicitar_prestamo(request, libro_id):
    """Procesa la solicitud de un préstamo para un libro."""
    libro = get_object_or_404(Libro, id=libro_id)
    if libro.cantidad_disponible > 0:
        # Verificar si el usuario ya tiene un préstamo activo de este libro
        if not Prestamo.objects.filter(libro=libro, usuario=request.user, devuelto=False).exists():
            Prestamo.objects.create(libro=libro, usuario=request.user)
            libro.cantidad_disponible -= 1
            libro.save()
            messages.success(request, f'Has solicitado el libro "{libro.titulo}".')
        else:
            messages.warning(request, 'Ya tienes un préstamo activo para este libro.')
    else:
        messages.error(request, 'Este libro no está disponible actualmente.')
    return redirect('biblioteca:detalle_libro', pk=libro.id)

@login_required
def confirmar_devolucion(request, prestamo_id):
    """Confirma y procesa la devolución de un libro."""
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, usuario=request.user)
    if request.method == 'POST':
        prestamo.devolver()
        messages.success(request, f'Has devuelto el libro "{prestamo.libro.titulo}".')
        return redirect('biblioteca:mis_prestamos')
    return render(request, 'biblioteca/confirmar_devolucion.html', {'prestamo': prestamo})

# ============================================================================
# VISTAS CRUD DE LIBROS
# ============================================================================

def lista_libros(request):
    """Vista para listar, buscar y filtrar libros."""
    queryset = Libro.objects.select_related('categoria').prefetch_related('autores', 'etiquetas').all()
    form = BusquedaLibroForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        categoria_id = form.cleaned_data.get('categoria')
        disponible = form.cleaned_data.get('disponible')

        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) | Q(autores__nombre__icontains=q) | Q(isbn__icontains=q)
            ).distinct()
        if categoria_id:
            queryset = queryset.filter(categoria=categoria_id)
        if disponible:
            queryset = queryset.filter(cantidad_disponible__gt=0)
    
    paginator = Paginator(queryset.order_by('titulo'), 12)
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)
    
    return render(request, 'biblioteca/lista_libros.html', {'libros': libros, 'form': form})

def detalle_libro(request, pk):
    """Vista para mostrar los detalles de un libro."""
    libro = get_object_or_404(Libro.objects.prefetch_related('autores', 'etiquetas'), pk=pk)
    return render(request, 'biblioteca/detalle_libro.html', {'libro': libro})

@login_required
def crear_libro(request):
    """Vista para añadir un nuevo libro."""
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f'Libro "{libro.titulo}" creado exitosamente.')
            return redirect('biblioteca:detalle_libro', pk=libro.pk)
    else:
        form = LibroForm()
    return render(request, 'biblioteca/crear.html', {'form': form, 'titulo': 'Añadir Nuevo Libro'})

@login_required
def editar_libro(request, pk):
    """Vista para editar un libro existente."""
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, f'Libro "{libro.titulo}" actualizado.')
            return redirect('biblioteca:detalle_libro', pk=libro.pk)
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/editar.html', {'form': form, 'libro': libro, 'titulo': f'Editar {libro.titulo}'})

@login_required
def eliminar_libro(request, pk):
    """Vista para eliminar un libro."""
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        nombre = libro.titulo
        libro.delete()
        messages.success(request, f'Libro "{nombre}" eliminado.')
        return redirect('biblioteca:lista_libros')
    return render(request, 'biblioteca/confirmar_eliminacion.html', {'objeto': libro, 'tipo': 'Libro'})

# ============================================================================
# VISTAS CRUD DE CATEGORÍAS Y ETIQUETAS (Protegidas)
# ============================================================================

@login_required
def lista_categorias(request):
    categorias = Categoria.objects.annotate(num_libros=Count('libros')).order_by('nombre')
    return render(request, 'biblioteca/lista_categorias.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('biblioteca:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'biblioteca/crear_categoria.html', {'form': form, 'titulo': 'Crear Categoría'})

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('biblioteca:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'biblioteca/editar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('biblioteca:lista_categorias')
    return render(request, 'biblioteca/confirmar_eliminacion.html', {'objeto': categoria, 'tipo': 'Categoría'})

@login_required
def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.annotate(num_libros=Count('libros')).order_by('nombre')
    return render(request, 'biblioteca/lista_etiquetas.html', {'etiquetas': etiquetas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada exitosamente.')
            return redirect('biblioteca:lista_etiquetas')
    else:
        form = EtiquetaForm()
    return render(request, 'biblioteca/crear_etiqueta.html', {'form': form, 'titulo': 'Crear Etiqueta'})

@login_required
def editar_etiqueta(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada.')
            return redirect('biblioteca:lista_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'biblioteca/editar_etiqueta.html', {'form': form, 'etiqueta': etiqueta})

@login_required
def eliminar_etiqueta(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        etiqueta.delete()
        messages.success(request, 'Etiqueta eliminada.')
        return redirect('biblioteca:lista_etiquetas')
    return render(request, 'biblioteca/confirmar_eliminacion.html', {'objeto': etiqueta, 'tipo': 'Etiqueta'})
