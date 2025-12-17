from django import forms
from .models import Producto, Categoria, Etiqueta, DetalleProducto


class BusquedaProductoForm(forms.Form):
    """Formulario para búsqueda y filtrado de productos"""
    nombre = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    etiqueta = forms.ModelChoiceField(
        queryset=Etiqueta.objects.all(),
        required=False,
        empty_label="Todas las etiquetas",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    precio_minimo = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'step': '0.01'
        })
    )
    precio_maximo = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'step': '0.01'
        })
    )
    disponible = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Solo productos disponibles'
    )


class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'codigo', 'stock', 'disponible', 'categoria', 'etiquetas']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'etiquetas': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'codigo': 'Código',
            'stock': 'Stock',
            'disponible': 'Disponible',
            'categoria': 'Categoría',
            'etiquetas': 'Etiquetas'
        }


class DetalleProductoForm(forms.ModelForm):
    """Formulario para crear y editar detalles de productos"""
    class Meta:
        model = DetalleProducto
        fields = ['peso', 'largo', 'ancho', 'alto', 'material', 'color', 'fabricante']
        widgets = {
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso en kg',
                'step': '0.01'
            }),
            'largo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Largo en cm',
                'step': '0.01'
            }),
            'ancho': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ancho en cm',
                'step': '0.01'
            }),
            'alto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alto en cm',
                'step': '0.01'
            }),
            'material': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Material'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'fabricante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fabricante'
            }),
        }
        labels = {
            'peso': 'Peso (kg)',
            'largo': 'Largo (cm)',
            'ancho': 'Ancho (cm)',
            'alto': 'Alto (cm)',
            'material': 'Material',
            'color': 'Color',
            'fabricante': 'Fabricante'
        }


class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías"""
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }


class EtiquetaForm(forms.ModelForm):
    """Formulario para crear y editar etiquetas"""
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la etiqueta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción'
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }
