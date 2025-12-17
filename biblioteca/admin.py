from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Autor, Categoria, Etiqueta, Libro, Prestamo, PerfilUsuario

# ============================================================================
# INLINES
# ============================================================================

class PerfilUsuarioInline(admin.StackedInline):
    """Inline para editar el perfil de usuario desde la página del usuario."""
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'user'

# ============================================================================
# ADMINS PERSONALIZADOS
# ============================================================================

class UserAdmin(BaseUserAdmin):
    """Extiende el admin de User para incluir el perfil."""
    inlines = (PerfilUsuarioInline,)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    """Admin para el modelo Autor."""
    list_display = ('nombre', 'fecha_nacimiento')
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin para el modelo Categoria."""
    list_display = ('nombre', 'id')
    search_fields = ('nombre',)

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    """Admin para el modelo Etiqueta."""
    list_display = ('nombre', 'id')
    search_fields = ('nombre',)

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    """Admin para el modelo Libro."""
    list_display = ('titulo', 'display_autores', 'categoria', 'cantidad_disponible', 'isbn')
    list_filter = ('categoria', 'etiquetas', 'autores')
    search_fields = ('titulo', 'isbn', 'autores__nombre')
    filter_horizontal = ('autores', 'etiquetas')
    readonly_fields = ('fecha_agregado', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'autores', 'descripcion', 'isbn')
        }),
        ('Clasificación', {
            'fields': ('categoria', 'etiquetas')
        }),
        ('Detalles Editoriales', {
            'fields': ('editorial', 'fecha_publicacion', 'numero_paginas', 'idioma')
        }),
        ('Inventario', {
            'fields': ('cantidad_disponible',)
        }),
        ('Auditoría', {
            'fields': ('fecha_agregado', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Autores')
    def display_autores(self, obj):
        """Muestra los autores en el list_display."""
        return ", ".join([autor.nombre for autor in obj.autores.all()])

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    """Admin para el modelo Prestamo."""
    list_display = ('libro', 'usuario', 'fecha_prestamo', 'devuelto', 'fecha_devolucion')
    list_filter = ('devuelto', 'fecha_prestamo')
    search_fields = ('libro__titulo', 'usuario__username')
    readonly_fields = ('fecha_prestamo', 'fecha_devolucion')
    actions = ['marcar_como_devuelto']

    @admin.action(description='Marcar seleccionados como devueltos')
    def marcar_como_devuelto(self, request, queryset):
        """Acción para devolver múltiples préstamos."""
        for prestamo in queryset.filter(devuelto=False):
            prestamo.devolver()
        self.message_user(request, f"{queryset.filter(devuelto=True).count()} préstamos marcados como devueltos.")

# ============================================================================
# REGISTRO
# ============================================================================

# Des-registrar el UserAdmin base y registrar el nuestro
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Personalizar el sitio admin
admin.site.site_header = "Administración de la Biblioteca"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Panel de Administración"
