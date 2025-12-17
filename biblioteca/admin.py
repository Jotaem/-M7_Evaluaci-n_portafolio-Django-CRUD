from django.contrib import admin
from .models import Categoria, Etiqueta, Producto, DetalleProducto


class DetalleProductoInline(admin.StackedInline):
    """Admin inline para detalles de productos (Relación Uno a Uno)"""
    model = DetalleProducto
    extra = 0
    fieldsets = (
        ('Dimensiones', {
            'fields': ('largo', 'ancho', 'alto', 'peso')
        }),
        ('Características', {
            'fields': ('material', 'color', 'fabricante')
        }),
    )


class CategoriaAdmin(admin.ModelAdmin):
    """Administrador personalizado para Categorías"""
    list_display = ('nombre', 'get_cantidad_productos', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    fieldsets = (
        ('Categoría', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_cantidad_productos(self, obj):
        """Mostrar cantidad de productos en la categoría"""
        return obj.get_productos_count()
    get_cantidad_productos.short_description = 'Productos'


class EtiquetaAdmin(admin.ModelAdmin):
    """Administrador personalizado para Etiquetas"""
    list_display = ('nombre', 'get_cantidad_productos', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)
    readonly_fields = ('fecha_creacion',)

    fieldsets = (
        ('Etiqueta', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )

    def get_cantidad_productos(self, obj):
        """Mostrar cantidad de productos con esta etiqueta"""
        return obj.get_productos_count()
    get_cantidad_productos.short_description = 'Productos'


class ProductoAdmin(admin.ModelAdmin):
    """Administrador personalizado para Productos"""
    list_display = ('nombre', 'codigo', 'categoria', 'precio', 'stock', 'disponible', 'fecha_creacion')
    search_fields = ('nombre', 'codigo', 'descripcion')
    list_filter = ('categoria', 'disponible', 'fecha_creacion', 'etiquetas')
    filter_horizontal = ('etiquetas',)  # Interfaz mejorada para relaciones M2M
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'get_detalles')
    list_per_page = 25
    
    inlines = [DetalleProductoInline]  # Editar detalles desde la página de producto

    fieldsets = (
        ('Información del Producto', {
            'fields': ('nombre', 'descripcion', 'codigo', 'categoria')
        }),
        ('Precios e Inventario', {
            'fields': ('precio', 'stock', 'disponible')
        }),
        ('Clasificación', {
            'fields': ('etiquetas',)
        }),
        ('Detalles', {
            'fields': ('get_detalles',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_detalles(self, obj):
        """Mostrar enlace a los detalles del producto"""
        try:
            detalle = obj.detalle
            return f"Peso: {detalle.peso}kg, Dimensiones: {detalle.largo}x{detalle.ancho}x{detalle.alto}cm"
        except DetalleProducto.DoesNotExist:
            return "Sin detalles registrados"
    get_detalles.short_description = 'Detalles del Producto'

    def get_queryset(self, request):
        """Optimizar consultas"""
        queryset = super().get_queryset(request)
        return queryset.select_related('categoria').prefetch_related('etiquetas')


class DetalleProductoAdmin(admin.ModelAdmin):
    """Administrador personalizado para Detalles de Productos"""
    list_display = ('producto', 'peso', 'get_dimensiones', 'material', 'color', 'fabricante')
    search_fields = ('producto__nombre', 'material', 'color', 'fabricante')
    list_filter = ('material', 'color', 'fecha_creacion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    list_per_page = 25

    fieldsets = (
        ('Producto', {
            'fields': ('producto',)
        }),
        ('Dimensiones', {
            'fields': ('largo', 'ancho', 'alto', 'peso')
        }),
        ('Características', {
            'fields': ('material', 'color', 'fabricante')
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def get_dimensiones(self, obj):
        """Mostrar dimensiones de forma legible"""
        return f"{obj.largo}x{obj.ancho}x{obj.alto} cm"
    get_dimensiones.short_description = 'Dimensiones (L x A x A)'

    def get_queryset(self, request):
        """Optimizar consultas"""
        queryset = super().get_queryset(request)
        return queryset.select_related('producto')


# Registrar modelos en el admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Etiqueta, EtiquetaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(DetalleProducto, DetalleProductoAdmin)

# Personalizar el sitio admin
admin.site.site_header = "Sistema de Gestión de Productos"
admin.site.site_title = "Panel Administrativo"
admin.site.index_title = "Bienvenido al Panel de Administración"

