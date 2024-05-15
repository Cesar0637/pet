from django.db import models
from django.contrib.auth.models import User
from usuarios.validadores import  imagen_validador
# Create your models here.
GENERO = [
    ('1', 'Masculino'),
    ('2', 'Femenino'),
    ('3', 'Otro'),
]

class DatosPersonales(models.Model):
    user = models.OneToOneField(User, verbose_name="Usuario", related_name='datos', on_delete=models.CASCADE)
    nombre = models.CharField("Nombres del encargado",max_length=300, null=True,blank=True)
    apellidos = models.CharField("Apellidos del encargado",max_length=300, null=True,blank=True)
    genero = models.CharField('Género del encargado', max_length=1, choices=GENERO,default=1,null=True,blank=True)
    imag_perfil = models.ImageField('', upload_to='imagenes_usuarios/',validators=[imagen_validador],null=True,blank=True)

class Location(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre Sucursal')
    address = models.CharField(max_length=250, verbose_name='Dirección')
    lat = models.FloatField(verbose_name='Latitud')
    lng = models.FloatField(verbose_name='Longitud')

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['name']

    def _str_(self):
        return self.name 