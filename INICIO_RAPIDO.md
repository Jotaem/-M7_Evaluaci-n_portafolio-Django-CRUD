# GUÍA RÁPIDA DE INICIO

## Inicio Rápido (5 minutos)

### 1️⃣ Clonar y entrar al directorio
```bash
cd "c:\src\Talento Digital\modulo_6\proyecto_django\M7_Evaluación del módulo"
```

### 2️⃣ Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar migraciones
```bash
python manage.py migrate
```

### 5️⃣ Crear superusuario
```bash
python manage.py createsuperuser
```

### 6️⃣ Cargar datos de ejemplo (opcional)
```bash
python manage.py shell
>>> exec(open('cargar_datos.py').read())
>>> exit()
```

### 7️⃣ Ejecutar servidor
```bash
python manage.py runserver
```

### ✅ ¡Listo!
- Sitio: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## 📋 Lista de Verificación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Servidor corriendo

---

## 🎯 Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio con dashboard |
| `/productos/` | Listado de productos |
| `/productos/crear/` | Crear nuevo producto |
| `/productos/<id>/` | Ver detalles del producto |
| `/productos/<id>/editar/` | Editar producto |
| `/productos/<id>/eliminar/` | Eliminar producto |
| `/categorias/` | Gestionar categorías |
| `/etiquetas/` | Gestionar etiquetas |
| `/admin/` | Panel administrativo |

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Error: "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### Error: "Database connection failed"
- Verificar que PostgreSQL esté corriendo (si lo usas)
- O cambiar a SQLite en settings.py

### Error de migraciones
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

---

## 📚 Documentación

- **README.md**: Documentación completa
- **IMPLEMENTACION.md**: Detalles técnicos
- **requirements.txt**: Dependencias del proyecto

---

## 💡 Consejos

- Los datos iniciales incluyen 6 productos de ejemplo
- Prueba los filtros en la página de productos
- Explora el panel admin para gestión avanzada
- Los estilos están optimizados para móviles

---

¡Disfruta del proyecto! 🚀
