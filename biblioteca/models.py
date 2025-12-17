from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Modelo para categorías de productos - Relación Uno a Muchos"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

    def get_productos_count(self):
        """Retorna la cantidad de productos en esta categoría"""
        return self.productos.count()


class Etiqueta(models.Model):
    """Modelo para etiquetas de productos - Relación Muchos a Muchos"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def __str__(self):
        return self.nombre

    def get_productos_count(self):
        """Retorna la cantidad de productos con esta etiqueta"""
        return self.productos.count()


class Producto(models.Model):
    """Modelo principal para productos - Relación Muchos a Uno con Categoría"""
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    codigo = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    disponible = models.BooleanField(default=True)
    
    # Relación Muchos a Uno: Un producto pertenece a una categoría
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        related_name='productos'
    )
    
    # Relación Muchos a Muchos: Un producto puede tener varias etiquetas
    etiquetas = models.ManyToManyField(
        Etiqueta,
        blank=True,
        related_name='productos'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria']),
            models.Index(fields=['precio']),
        ]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    @property
    def puede_venderse(self):
        """Verifica si hay stock disponible"""
        return self.stock > 0 and self.disponible


class DetalleProducto(models.Model):
    """Modelo para detalles adicionales de productos - Relación Uno a Uno"""
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='detalle'
    )
    
    # Detalles específicos del producto
    peso = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Peso en kilogramos"
    )
    largo = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Largo en centímetros"
    )
    ancho = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Ancho en centímetros"
    )
    alto = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Alto en centímetros"
    )
    material = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    fabricante = models.CharField(max_length=200, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Detalle de Producto'
        verbose_name_plural = 'Detalles de Productos'

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"
