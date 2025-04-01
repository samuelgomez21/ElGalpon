# store/models.py
from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'clientes'

class Empleado(models.Model):
    CARGO_CHOICES = [
        ('veterinario', 'Veterinario'),
        ('asistente', 'Asistente'),
        ('cajero', 'Cajero'),
        ('administrador', 'Administrador'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    horario_entrada = models.TimeField(default='07:00:00')
    horario_salida = models.TimeField(default='18:00:00')

    def __str__(self):
        return f"{self.nombre} ({self.get_cargo_display()})"

    class Meta:
        db_table = 'empleados'

class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('comida', 'Comida'),
        ('cuidado_animal', 'Cuidado Animal'),
    ]

    ESPECIE_CHOICES = [
        ('pollos', 'Pollos'),
        ('gallinas', 'Gallinas'),
        ('cerdos', 'Cerdos'),
        ('vacas', 'Vacas'),
        ('caballos', 'Caballos'),
        ('terneros', 'Terneros'),
        ('perros', 'Perros'),
        ('gatos', 'Gatos'),
        ('otros', 'Otros'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'productos'

class CitaVeterinaria(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Cita para {self.cliente.nombre} el {self.fecha_hora}"

    class Meta:
        db_table = 'citas_veterinarias'

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha}"

    class Meta:
        db_table = 'ventas'

class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de venta #{self.venta.id} - {self.producto.nombre}"

    class Meta:
        db_table = 'detalles_venta'