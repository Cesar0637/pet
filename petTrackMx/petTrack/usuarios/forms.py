from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DatosPersonales


class UserForm(forms.ModelForm):
    repassword = forms.CharField()
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'repassword')
   
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
   
    def clean_password(self, *args, **kwargs):
        if self.data['password'] != self.data['repassword']:
            raise forms.ValidationError('Las contraseñas son diferentes; favor de verificar')
       
        return self.data['password']
   
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username
    
class FormDatosPersonales(forms.ModelForm):
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