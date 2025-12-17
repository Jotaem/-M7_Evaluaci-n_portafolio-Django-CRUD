from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Libro, Autor, Categoria, Etiqueta, PerfilUsuario

# ============================================================================
# FORMULARIOS DE AUTENTICACIÓN Y USUARIO
# ============================================================================

class RegistroUsuarioForm(UserCreationForm):
    """Formulario de registro de usuarios, extendido para incluir email."""
    email = forms.EmailField(required=True, help_text='Requerido. Ingrese un email válido.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class LoginForm(AuthenticationForm):
    """Formulario de login con estilos de Bootstrap."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre de usuario'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})

class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para editar el perfil de usuario."""
    class Meta:
        model = PerfilUsuario
        fields = ['direccion', 'telefono', 'fecha_nacimiento']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ============================================================================
# FORMULARIOS DE BÚSQUEDA
# ============================================================================

class BusquedaLibroForm(forms.Form):
    """Formulario para búsqueda y filtrado de libros."""
    q = forms.CharField(
        max_length=200, required=False, label='Buscar',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título, autor o ISBN...'})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(), required=False, empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    disponible = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Solo disponibles'
    )

# ============================================================================
# FORMULARIOS DE MODELOS (CRUD)
# ============================================================================

class LibroForm(forms.ModelForm):
    """Formulario para crear y editar Libros."""
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Libro
        fields = [
            'titulo', 'autores', 'descripcion', 'isbn', 'cantidad_disponible', 
            'categoria', 'etiquetas', 'fecha_publicacion', 'editorial', 
            'numero_paginas', 'idioma'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'etiquetas': forms.CheckboxSelectMultiple,
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_paginas': forms.NumberInput(attrs={'class': 'form-control'}),
            'idioma': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AutorForm(forms.ModelForm):
    """Formulario para crear y editar Autores."""
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar Categorías."""
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class EtiquetaForm(forms.ModelForm):
    """Formulario para crear y editar Etiquetas."""
    class Meta:
        model = Etiqueta
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }
