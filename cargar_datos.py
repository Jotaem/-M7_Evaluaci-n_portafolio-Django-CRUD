"""
Script para cargar datos iniciales de ejemplo en la base de datos
Ejecutar con: python manage.py shell < cargar_datos.py
O: python manage.py shell
    >>> exec(open('cargar_datos.py').read())
"""

from biblioteca.models import Categoria, Etiqueta, Producto, DetalleProducto
from decimal import Decimal

print("=== CARGANDO DATOS INICIALES ===\n")

# Crear categorías
print("Creando categorías...")
categorias = [
    Categoria.objects.create(
        nombre="Electrónica",
        descripcion="Productos electrónicos y accesorios"
    ),
    Categoria.objects.create(
        nombre="Ropa y Accesorios",
        descripcion="Prendas de vestir y accesorios de moda"
    ),
    Categoria.objects.create(
        nombre="Hogar",
        descripcion="Artículos para el hogar y decoración"
    ),
    Categoria.objects.create(
        nombre="Deportes",
        descripcion="Equipos y accesorios deportivos"
    ),
]

# Crear etiquetas
print("Creando etiquetas...")
etiquetas = [
    Etiqueta.objects.create(
        nombre="Oferta",
        descripcion="Productos en promoción"
    ),
    Etiqueta.objects.create(
        nombre="Popular",
        descripcion="Productos más vendidos"
    ),
    Etiqueta.objects.create(
        nombre="Nuevo",
        descripcion="Productos nuevos"
    ),
    Etiqueta.objects.create(
        nombre="Premium",
        descripcion="Productos de alta calidad"
    ),
]

# Crear productos
print("Creando productos...")
productos_data = [
    {
        "nombre": "Laptop Gaming",
        "descripcion": "Laptop de alto rendimiento para gaming y trabajo profesional",
        "precio": Decimal("1299.99"),
        "codigo": "LAPT-001",
        "stock": 15,
        "disponible": True,
        "categoria": categorias[0],
        "etiquetas": [etiquetas[1], etiquetas[3]],
        "detalle": {
            "peso": Decimal("2.5"),
            "largo": Decimal("35"),
            "ancho": Decimal("25"),
            "alto": Decimal("2"),
            "material": "Aluminio",
            "color": "Negro",
            "fabricante": "TechCorp"
        }
    },
    {
        "nombre": "Auriculares Inalámbricos",
        "descripcion": "Auriculares con cancelación de ruido activa",
        "precio": Decimal("199.99"),
        "codigo": "AURI-001",
        "stock": 45,
        "disponible": True,
        "categoria": categorias[0],
        "etiquetas": [etiquetas[2], etiquetas[3]],
        "detalle": {
            "peso": Decimal("0.25"),
            "largo": Decimal("20"),
            "ancho": Decimal("18"),
            "alto": Decimal("8"),
            "material": "Plástico ABS",
            "color": "Blanco",
            "fabricante": "AudioMax"
        }
    },
    {
        "nombre": "Camiseta Premium",
        "descripcion": "Camiseta de algodón 100% de alta calidad",
        "precio": Decimal("49.99"),
        "codigo": "CAMI-001",
        "stock": 100,
        "disponible": True,
        "categoria": categorias[1],
        "etiquetas": [etiquetas[1], etiquetas[0]],
        "detalle": {
            "peso": Decimal("0.2"),
            "largo": Decimal("70"),
            "ancho": Decimal("50"),
            "alto": Decimal("1"),
            "material": "Algodón 100%",
            "color": "Azul",
            "fabricante": "FashionBrand"
        }
    },
    {
        "nombre": "Lámpara LED",
        "descripcion": "Lámpara LED inteligente con control remoto",
        "precio": Decimal("89.99"),
        "codigo": "LAMP-001",
        "stock": 30,
        "disponible": True,
        "categoria": categorias[2],
        "etiquetas": [etiquetas[2], etiquetas[0]],
        "detalle": {
            "peso": Decimal("0.5"),
            "largo": Decimal("15"),
            "ancho": Decimal("15"),
            "alto": Decimal("20"),
            "material": "Plástico + Metal",
            "color": "Plateado",
            "fabricante": "SmartHome"
        }
    },
    {
        "nombre": "Pelota de Fútbol",
        "descripcion": "Pelota de fútbol profesional de cuero genuino",
        "precio": Decimal("34.99"),
        "codigo": "PELO-001",
        "stock": 60,
        "disponible": True,
        "categoria": categorias[3],
        "etiquetas": [etiquetas[1]],
        "detalle": {
            "peso": Decimal("0.43"),
            "largo": Decimal("22"),
            "ancho": Decimal("22"),
            "alto": Decimal("22"),
            "material": "Cuero",
            "color": "Blanco y Negro",
            "fabricante": "SoccerGear"
        }
    },
    {
        "nombre": "Monitor 4K",
        "descripcion": "Monitor 4K de 27 pulgadas para diseño gráfico",
        "precio": Decimal("599.99"),
        "codigo": "MONI-001",
        "stock": 8,
        "disponible": True,
        "categoria": categorias[0],
        "etiquetas": [etiquetas[3], etiquetas[2]],
        "detalle": {
            "peso": Decimal("5.2"),
            "largo": Decimal("61"),
            "ancho": Decimal("9"),
            "alto": Decimal("42"),
            "material": "Plástico y Acero",
            "color": "Negro",
            "fabricante": "DisplayTech"
        }
    },
]

# Guardar productos y detalles
for prod_data in productos_data:
    detalle_data = prod_data.pop("detalle")
    etiquetas_list = prod_data.pop("etiquetas")
    
    producto = Producto.objects.create(**prod_data)
    
    # Añadir etiquetas
    producto.etiquetas.set(etiquetas_list)
    
    # Crear detalles del producto
    DetalleProducto.objects.create(
        producto=producto,
        **detalle_data
    )
    
    print(f"✓ Producto creado: {producto.nombre}")

print("\n=== DATOS INICIALES CARGADOS EXITOSAMENTE ===")
print(f"\nResumen:")
print(f"- Categorías: {Categoria.objects.count()}")
print(f"- Etiquetas: {Etiqueta.objects.count()}")
print(f"- Productos: {Producto.objects.count()}")
print(f"- Detalles de Productos: {DetalleProducto.objects.count()}")
