from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Modelo PerfilUsuario con Relación Uno a Uno
class PerfilUsuario(models.Model):
    """Modelo para extender el modelo de usuario predeterminado de Django."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Modelo Autor
class Autor(models.Model):
    """Modelo para los autores de los libros."""
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo Categoria con Relación Uno a Muchos
class Categoria(models.Model):
    """Modelo para categorías de libros."""
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

# Modelo Etiqueta con Relación Muchos a Muchos
class Etiqueta(models.Model):
    """Modelo para etiquetas de libros."""
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Modelo Libro
class Libro(models.Model):
    """Modelo principal para los libros de la biblioteca."""
    titulo = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor, related_name='libros')
    descripcion = models.TextField(blank=True)
    isbn = models.CharField(max_length=13, unique=True, help_text='ISBN de 13 caracteres')
    cantidad_disponible = models.PositiveIntegerField(default=0)
    
    # Relación ForeignKey: Un libro pertenece a una categoría.
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    
    # Relación ManyToManyField: Un libro puede tener varias etiquetas.
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='libros')
    
    fecha_publicacion = models.DateField(blank=True, null=True)
    editorial = models.CharField(max_length=100, blank=True, null=True)
    numero_paginas = models.PositiveIntegerField(blank=True, null=True)
    idioma = models.CharField(max_length=50, default='Español')
    
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['titulo']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.titulo

# Modelo Prestamo con Relación a Libro y Usuario
class Prestamo(models.Model):
    """Modelo para gestionar los préstamos de libros a usuarios."""
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    devuelto = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_prestamo']
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'

    def __str__(self):
        return f'{self.libro.titulo} prestado a {self.usuario.username}'

    def devolver(self):
        """Marca el libro como devuelto."""
        self.fecha_devolucion = timezone.now()
        self.devuelto = True
        self.save()
        # Incrementar el stock del libro
        self.libro.cantidad_disponible += 1
        self.libro.save()
