from django.urls import path
from . import views

app_name = 'biblioteca'

urlpatterns = [
    # Página de inicio
    path('', views.index, name='index'),

    # Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # Perfil de Usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Libros (CRUD)
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/crear/', views.crear_libro, name='crear_libro'),
    path('libros/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('libros/<int:pk>/editar/', views.editar_libro, name='editar_libro'),
    path('libros/<int:pk>/eliminar/', views.eliminar_libro, name='eliminar_libro'),

    # Categorías (CRUD)
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/eliminar/', views.eliminar_categoria, name='eliminar_categoria'),

    # Etiquetas (CRUD)
    path('etiquetas/', views.lista_etiquetas, name='lista_etiquetas'),
    path('etiquetas/crear/', views.crear_etiqueta, name='crear_etiqueta'),
    path('etiquetas/<int:pk>/editar/', views.editar_etiqueta, name='editar_etiqueta'),
    path('etiquetas/<int:pk>/eliminar/', views.eliminar_etiqueta, name='eliminar_etiqueta'),

    # Préstamos
    path('prestamos/solicitar/<int:libro_id>/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('prestamos/mis-prestamos/', views.mis_prestamos, name='mis_prestamos'),
    path('prestamos/devolver/<int:prestamo_id>/', views.confirmar_devolucion, name='confirmar_devolucion'),
    
    # Página 'Acerca de'
    path('acerca-de/', views.acerca_de, name='acerca_de'),
]
