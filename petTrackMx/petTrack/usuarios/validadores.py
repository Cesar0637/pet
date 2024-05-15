from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator, RegexValidator

imagen_validador = FileExtensionValidator(
    allowed_extensions=['png','jpg'],
    message="Sólo se permiten imágenes PNG"
)