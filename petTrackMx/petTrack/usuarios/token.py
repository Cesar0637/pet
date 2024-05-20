from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class Token(PasswordResetTokenGenerator):
    """
    Clase personalizada para generar tokens de activación de cuenta.
    """
    
    def _make_hash_value(self, user, timestamp):
        """
        Genera un valor hash basado en la información del usuario y un timestamp.
        
        Parámetros:
        user (User): El usuario para el cual se genera el token.
        timestamp (int): El timestamp utilizado para la generación del token.
        
        Retorna:
        str: El valor hash generado.
        """
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)

# Instancia de la clase Token para usar en la activación de cuenta
token_activacion = Token()