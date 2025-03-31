from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Carga productos iniciales en la base de datos'

    def handle(self, *args, **kwargs):
        # Crear categorías
        categories = [
            "Medicamentos Veterinarios",
            "Cuidado Mascotas",
            "Avicultura",
            "Ganadería",
            "Porcicultura"
        ]
        category_objects = {}
        for cat_name in categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            category_objects[cat_name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría "{cat_name}" creada.'))

        # Lista de productos
        products = [
            ("Antibiótico Canino", "Medicamentos Veterinarios", 50.00, "Tratamiento para infecciones caninas", 100, "product1.jpg"),
            ("Shampoo Antipulgas", "Cuidado Mascotas", 15.00, "Protección contra pulgas", 200, "product2.jpg"),
            ("Suplemento Avícola", "Avicultura", 30.00, "Mejora la salud de aves", 150, "product3.jpg"),
            ("Vacuna Ganadera", "Ganadería", 75.00, "Prevención de enfermedades", 80, "product4.jpg"),
            ("Alimento Porcino", "Porcicultura", 25.00, "Nutrición balanceada", 120, "product5.jpg"),
            ("Desparasitante Felino", "Cuidado Mascotas", 20.00, "Elimina parásitos", 180, "product6.jpg"),
            ("Vitamina Avícola", "Avicultura", 40.00, "Fortalece el sistema inmunológico", 90, "product7.jpg"),
            ("Antibiótico Bovino", "Ganadería", 90.00, "Tratamiento para ganado", 70, "product8.jpg"),
            ("Suplemento Porcino", "Porcicultura", 35.00, "Crecimiento saludable", 110, "product9.jpg"),
            ("Cepillo para Mascotas", "Cuidado Mascotas", 10.00, "Mantiene el pelaje limpio", 250, "product10.jpg"),
            ("Desinfectante Avícola", "Avicultura", 45.00, "Higiene en granjas", 60, "product11.jpg"),
            ("Sueroterapia Ganadera", "Ganadería", 60.00, "Hidratación y recuperación", 85, "product12.jpg"),
            ("Pienso Porcino", "Porcicultura", 28.00, "Alimento completo", 130, "product13.jpg"),
            ("Collar Antipulgas", "Cuidado Mascotas", 18.00, "Protección continua", 220, "product14.jpg"),
            ("Vacuna Avícola", "Avicultura", 55.00, "Prevención de enfermedades", 75, "product15.jpg"),
            ("Mineral Ganadero", "Ganadería", 70.00, "Suplemento mineral", 95, "product16.jpg"),
            ("Antibiótico Porcino", "Porcicultura", 40.00, "Tratamiento efectivo", 100, "product17.jpg"),
            ("Juguete para Mascotas", "Cuidado Mascotas", 12.00, "Entretenimiento seguro", 300, "product18.jpg"),
            ("Desparasitante Avícola", "Avicultura", 25.00, "Control de parásitos", 140, "product19.jpg"),
            ("Fertilizante Ganadero", "Ganadería", 80.00, "Mejora el pasto", 50, "product20.jpg"),
            ("Antiséptico Canino", "Medicamentos Veterinarios", 35.00, "Desinfección de heridas", 120, "product21.jpg"),
            ("Cama para Mascotas", "Cuidado Mascotas", 40.00, "Cama cómoda para perros", 90, "product22.jpg"),
            ("Probiótico Avícola", "Avicultura", 50.00, "Mejora la digestión", 80, "product23.jpg"),
            ("Antiparasitario Bovino", "Ganadería", 65.00, "Control de parásitos externos", 70, "product24.jpg"),
            ("Engorde Porcino", "Porcicultura", 45.00, "Suplemento para engorde", 100, "product25.jpg"),
            ("Correa para Mascotas", "Cuidado Mascotas", 15.00, "Correa resistente", 200, "product26.jpg"),
            ("Antiviral Avícola", "Avicultura", 60.00, "Protección contra virus", 60, "product27.jpg"),
            ("Electrolitos Ganaderos", "Ganadería", 55.00, "Hidratación rápida", 85, "product28.jpg"),
            ("Vacuna Porcina", "Porcicultura", 70.00, "Prevención de enfermedades", 90, "product29.jpg"),
            ("Analgésico Canino", "Medicamentos Veterinarios", 45.00, "Alivio del dolor", 110, "product30.jpg"),
        ]

        # Añadir productos
        for name, category_name, price, description, stock, image_name in products:
            if not Product.objects.filter(name=name).exists():
                product = Product(
                    name=name,
                    category=category_objects[category_name],
                    price=price,
                    description=description,
                    stock=stock
                )
                image_path = os.path.join('static/images', image_name)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        product.image.save(image_name, File(f), save=True)
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Producto "{name}" creado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Producto "{name}" ya existe.'))