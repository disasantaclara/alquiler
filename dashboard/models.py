from django.db import models

# Create your models here.

class Arrendatario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.nombre

class Local(models.Model):
    nombre = models.CharField(max_length=50)
    arrendatario = models.ForeignKey(Arrendatario, on_delete=models.SET_NULL, null=True, blank=True)
    es_departamento = models.BooleanField(default=False)
    es_parqueadero = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    garantia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rentado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    arrendatario = models.ForeignKey(Arrendatario, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    es_abono = models.BooleanField(default=False)
    tipo_pago = models.CharField(max_length=20, choices=[('efectivo', 'Efectivo'), ('transferencia', 'Transferencia')])
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    fecha_proximo_pago = models.DateField()

    def __str__(self):
        return f"{self.arrendatario} - {self.local} - {self.fecha_pago}"
