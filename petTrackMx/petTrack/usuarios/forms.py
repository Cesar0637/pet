from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DatosPersonales

class UserForm(forms.ModelForm):
    """
    Formulario para el registro de usuarios, incluye confirmación de contraseña.
    """
    repassword = forms.CharField(widget=forms.PasswordInput(), label="Repetir contraseña")
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'repassword')

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        """
        Sobrescribe el método save para manejar el almacenamiento del usuario con la contraseña encriptada.
        """
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def clean_password(self):
        """
        Valida que las contraseñas coincidan.
        """
        if self.cleaned_data['password'] != self.cleaned_data['repassword']:
            raise ValidationError('Las contraseñas son diferentes; favor de verificar')
        return self.cleaned_data['password']

    def clean_username(self):
        """
        Valida que el nombre de usuario sea único.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

class FormDatosPersonales(forms.ModelForm):
    """
    Formulario para los datos personales del usuario.
    """
    class Meta:
        model = DatosPersonales
        exclude = ['user']  # Campos excluidos de la generación automática de campos del formulario
        fields = '__all__'  # Puedes usar '__all__' para incluir todos los campos, excepto los excluidos
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'imag_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }