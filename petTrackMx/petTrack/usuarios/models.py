from django.db import models
from django.contrib.auth.models import User
from usuarios.validadores import imagen_validador

# Opciones para el campo de género
GENERO = [
    ('1', 'Masculino'),
    ('2', 'Femenino'),
    ('3', 'Otro'),
]

class DatosPersonales(models.Model):
    """
    Modelo para almacenar los datos personales del usuario.

    Atributos:
        user (OneToOneField): Relación uno a uno con el modelo de usuario de Django.
        nombre (CharField): Nombre del usuario.
        apellidos (CharField): Apellidos del usuario.
        genero (CharField): Género del usuario, con opciones predefinidas.
        imag_perfil (ImageField): Imagen de perfil del usuario.
    """
    user = models.OneToOneField(User, verbose_name="Usuario", related_name='datos', on_delete=models.CASCADE)
    nombre = models.CharField("Nombres", max_length=300, null=True, blank=True)
    apellidos = models.CharField("Apellidos", max_length=300, null=True, blank=True)
    genero = models.CharField('Género', max_length=1, choices=GENERO, default=1, null=True, blank=True)
    imag_perfil = models.ImageField('', upload_to='imagenes_usuarios/', validators=[imagen_validador], null=True, blank=True)

class Location(models.Model):
    """
    Modelo para almacenar las ubicaciones.

    Atributos:
        lat (FloatField): Latitud de la ubicación.
        lng (FloatField): Longitud de la ubicación.
    """
    lat = models.FloatField(verbose_name='Latitud')
    lng = models.FloatField(verbose_name='Longitud')

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['id']

    def __str__(self):
        """
        Retorna una representación legible del objeto Location.
        """
        return f"Latitud: {self.lat}, Longitud: {self.lng}"
