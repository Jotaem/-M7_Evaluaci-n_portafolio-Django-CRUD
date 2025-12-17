# Sistema de Gestión de Productos - Django

Este es un proyecto Django completo que implementa un sistema de gestión de productos con todas las características requeridas en la evaluación del módulo.

## Características Implementadas

### 1. **Modelos con Relaciones**
- **Categoría** (One-to-Many): Una categoría puede tener muchos productos
- **Producto** (Many-to-One): Un producto pertenece a una sola categoría
- **Etiqueta** (Many-to-Many): Los productos pueden tener múltiples etiquetas
- **DetalleProducto** (One-to-One): Cada producto tiene detalles únicos (dimensiones, peso, etc.)

### 2. **Operaciones CRUD Completas**
- ✅ Crear productos, categorías y etiquetas
- ✅ Listar productos con paginación
- ✅ Ver detalles de productos
- ✅ Editar productos, categorías y etiquetas
- ✅ Eliminar productos, categorías y etiquetas

### 3. **Filtrado y Búsqueda Avanzada**
- Búsqueda por nombre, código y descripción
- Filtrado por categoría y etiquetas
- Filtrado por rango de precios
- Filtrado por disponibilidad
- Búsqueda con ORM de Django (Q, F, annotate)

### 4. **Base de Datos**
- Configurado para **PostgreSQL**
- SQLite disponible como alternativa
- Migraciones implementadas
- Índices en campos frecuentemente consultados

### 5. **Panel Administrativo**
- Interfaz Django Admin personalizada
- Inlines para editar detalles de productos
- Búsqueda y filtrado en el admin
- Visualización de relaciones

### 6. **Interfaz de Usuario**
- Diseño responsivo con **Bootstrap 5**
- Temas visuales modernos
- Animaciones y transiciones suaves
- Iconos con **Font Awesome**
- Formularios intuitivos

### 7. **Seguridad**
- Protección CSRF en todos los formularios
- Middleware de seguridad configurado
- Validación de datos en formularios
- Control de acceso

## Requisitos Previos

```bash
- Python 3.8+
- pip (gestor de paquetes de Python)
- PostgreSQL (opcional, SQLite por defecto)
- Git
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd proyecto_django
```

### 2. Crear un entorno virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

#### Opción A: Usar PostgreSQL (Recomendado)
```bash
# Crear la base de datos en PostgreSQL
psql -U postgres
CREATE DATABASE gestion_productos;
\q
```

Luego editar `biblioteca_config/settings.py` y asegurarse de que PostgreSQL está configurado:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_productos',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Opción B: Usar SQLite (Por defecto)
SQLite ya está configurado en `settings.py`. Solo necesitas ejecutar las migraciones.

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario (Administrador)
```bash
python manage.py createsuperuser
```

Ingresar los datos solicitados:
- Usuario
- Email
- Contraseña

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

El servidor se iniciará en: `http://127.0.0.1:8000/`

## Uso de la Aplicación

### Acceder al Sitio Web
- **URL Principal**: http://localhost:8000/
- Navegación por productos, categorías y etiquetas
- Crear, editar y eliminar productos

### Acceder al Panel Administrativo
- **URL Admin**: http://localhost:8000/admin/
- Credenciales: Usuario y contraseña del superusuario creado
- Gestión completa de modelos
- Edición inline de detalles de productos

## Estructura del Proyecto

```
proyecto_django/
├── biblioteca/
│   ├── models.py          # Modelos (Producto, Categoría, Etiqueta, DetalleProducto)
│   ├── views.py           # Vistas CRUD
│   ├── forms.py           # Formularios
│   ├── urls.py            # Rutas URL
│   ├── admin.py           # Configuración del panel admin
│   ├── migrations/        # Migraciones de base de datos
│   └── templates/
│       └── biblioteca/
│           ├── base.html  # Template base
│           ├── index.html # Página de inicio
│           ├── lista_libros.html # Listado de productos
│           ├── detalle_libro.html # Detalles del producto
│           ├── crear.html # Crear producto
│           ├── editar.html # Editar producto
│           ├── confirmar_eliminacion.html # Confirmación de eliminación
│           ├── lista_categorias.html # Listado de categorías
│           ├── crear_categoria.html # Crear categoría
│           ├── editar_categoria.html # Editar categoría
│           ├── lista_etiquetas.html # Listado de etiquetas
│           ├── crear_etiqueta.html # Crear etiqueta
│           └── editar_etiqueta.html # Editar etiqueta
├── biblioteca_config/
│   ├── settings.py       # Configuración de Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Relaciones de Base de Datos

### Relación Muchos a Uno (Producto → Categoría)
Un producto pertenece a una categoría, pero una categoría puede tener muchos productos.

```python
categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='productos')
```

### Relación Muchos a Muchos (Producto ↔ Etiqueta)
Un producto puede tener múltiples etiquetas, y una etiqueta puede estar en múltiples productos.

```python
etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='productos')
```

### Relación Uno a Uno (Producto ↔ DetalleProducto)
Cada producto tiene un único conjunto de detalles (dimensiones, peso, etc.).

```python
producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='detalle')
```

## Consultas con ORM

El proyecto implementa consultas avanzadas con el ORM de Django:

- **Filter**: Filtrado básico por campos
- **Q Objects**: Búsquedas complejas con operadores AND/OR
- **Exclude**: Excluir resultados específicos
- **Count**: Contar registros relacionados (annotate)
- **Prefetch Related**: Optimización de relaciones M2M
- **Select Related**: Optimización de relaciones FK

Ejemplo:
```python
productos = Producto.objects.filter(
    Q(nombre__icontains=nombre) | Q(descripcion__icontains=nombre)
).filter(
    precio__gte=precio_minimo,
    precio__lte=precio_maximo
).select_related('categoria').prefetch_related('etiquetas')
```

## Migraciones

Para crear nuevas migraciones después de cambios en modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Para ver el estado de las migraciones:
```bash
python manage.py showmigrations
```

## Configuración de PostgreSQL

Si deseas usar PostgreSQL, primero instala el driver:

```bash
pip install psycopg2-binary
```

Luego edita `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestion_productos',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Características de Seguridad

✅ **Protección CSRF**: Todos los formularios incluyen tokens CSRF
✅ **Middleware de Seguridad**: Configurado en `MIDDLEWARE`
✅ **Validación de Datos**: Validación en formularios y modelos
✅ **SQL Injection Prevention**: Uso de ORM previene inyecciones SQL
✅ **XSS Protection**: Escaping automático en templates

## Solución de Problemas

### Error de conexión a PostgreSQL
```bash
# Verificar que PostgreSQL está corriendo
# En Windows:
psql -U postgres

# En macOS/Linux:
sudo systemctl status postgresql
```

### Error de módulo no encontrado
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Port 8000 ya en uso
```bash
# Ejecutar en un puerto diferente
python manage.py runserver 8001
```

### Borrar la base de datos y empezar de cero
```bash
# Eliminar archivo sqlite3
rm db.sqlite3

# Ejecutar migraciones nuevamente
python manage.py migrate

# Crear nuevo superusuario
python manage.py createsuperuser
```

## Tecnologías Utilizadas

- **Backend**: Django 6.0
- **Base de Datos**: PostgreSQL / SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Iconos**: Font Awesome 6.4
- **ORM**: Django ORM
- **Validación**: Django Forms

## Próximos Pasos (Mejoras Futuras)

- [ ] Agregar imágenes a los productos
- [ ] Implementar sistema de carritos de compra
- [ ] Agregar sistema de reseñas y calificaciones
- [ ] Implementar reportes en PDF
- [ ] Agregar API REST con Django REST Framework
- [ ] Autenticación con redes sociales
- [ ] Email notifications

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Desarrollado como evaluación del Módulo 7 - Talento Digital

## Soporte

Para reportar problemas o sugerencias, por favor abre un issue en el repositorio.

---

**Nota**: Este proyecto cumple con todos los requisitos de la evaluación del módulo, incluyendo:
✅ Conexión a PostgreSQL
✅ Modelos con relaciones (1:N, M:M, 1:1)
✅ Migraciones de Django
✅ Operaciones CRUD completas
✅ Consultas avanzadas con ORM
✅ Seguridad CSRF y middleware
✅ Panel administrativo personalizado
✅ Interfaz atractiva con Bootstrap 5
