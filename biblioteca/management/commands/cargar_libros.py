import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from biblioteca.models import Autor, Categoria, Libro


class Command(BaseCommand):
    help = 'Carga libros desde el archivo CSV de la Biblioteca IBG'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            nargs='?',
            type=str,
            default='Biblioteca IBG - Biblioteca.csv',
            help='Ruta del archivo CSV a cargar (por defecto: Biblioteca IBG - Biblioteca.csv)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        # Construir la ruta del archivo
        if not os.path.isabs(csv_file):
            csv_file = os.path.join(settings.BASE_DIR, csv_file)

        # Verificar que el archivo existe
        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'El archivo "{csv_file}" no existe.')
            )
            return

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                libros_creados = 0
                libros_actualizados = 0
                errores = 0

                for row in reader:
                    try:
                        # Obtener o crear categoría
                        categoria_nombre = row.get('TIPO', '').strip()
                        if categoria_nombre:
                            categoria, _ = Categoria.objects.get_or_create(
                                nombre=categoria_nombre
                            )
                        else:
                            categoria = None

                        # Obtener o crear autor
                        autor_nombre = row.get('AUTOR', '').strip()
                        if not autor_nombre:
                            self.stdout.write(
                                self.style.WARNING(f'Skipping libro sin autor: {row.get("TÍTULO")}')
                            )
                            errores += 1
                            continue

                        autor, _ = Autor.objects.get_or_create(
                            nombre=autor_nombre
                        )

                        # Obtener datos del libro
                        titulo = row.get('TÍTULO', '').strip()
                        codigo = row.get('CÓDIGO', '').strip()
                        isbn = row.get('CÓDIGO', '').strip() if '97' in row.get('CÓDIGO', '') else ''
                        stock = int(row.get('STOCK', '1') or '1')

                        if not titulo or not codigo:
                            self.stdout.write(
                                self.style.WARNING(f'Skipping libro sin título o código: {titulo}')
                            )
                            errores += 1
                            continue

                        # Crear o actualizar libro
                        libro, created = Libro.objects.update_or_create(
                            codigo=codigo,
                            defaults={
                                'titulo': titulo,
                                'autor': autor,
                                'categoria': categoria,
                                'isbn': isbn,
                                'stock': stock,
                                'disponible': stock > 0,
                            }
                        )

                        if created:
                            libros_creados += 1
                        else:
                            libros_actualizados += 1

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error procesando fila: {str(e)}')
                        )
                        errores += 1
                        continue

            # Resumen
            self.stdout.write(self.style.SUCCESS('✓ Carga completada'))
            self.stdout.write(f'  Libros creados: {libros_creados}')
            self.stdout.write(f'  Libros actualizados: {libros_actualizados}')
            if errores > 0:
                self.stdout.write(self.style.WARNING(f'  Errores: {errores}'))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al leer el archivo: {str(e)}')
            )
