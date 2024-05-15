from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from .models import DatosPersonales, Location
from .forms import FormDatosPersonales, UserForm
from .token import token_activacion
from django.contrib.auth.views import PasswordResetView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import folium 
from folium.plugins import FastMarkerCluster

class BienvenidaView(TemplateView):
    template_name = 'bienvenida.html'

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.txt'
    success_url = reverse_lazy('password_reset_done')

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # Elimina líneas en blanco de la cadena

        # Obtén los datos necesarios para el enlace de restablecimiento
        protocol = self.request.scheme  # 'http' o 'https'
        domain = self.request.META['HTTP_HOST']  # Dominio del sitio
        uid = urlsafe_base64_encode(force_bytes(context['user'].pk)).decode()
        token = context['token']

        context.update({
            'protocol': protocol,
            'domain': domain,
            'uid': uid,
            'token': token,
            'timeout': 24,  # Ajusta esto según tu configuración
        })

        # Renderiza la plantilla de correo electrónico en texto plano
        message = render_to_string(email_template_name, context)

        # Envía el correo electrónico
        email = EmailMessage(subject, message, from_email, [to_email])
        email.send()

class LoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    # form_class = LoginForm

class RegistrarView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')
    success_message = "Entre a su correo '%(email)s' para validar su cuenta"
   
    def form_valid(self, form):
        # Validación de correo electrónico único
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(self.request, 'Este correo electrónico ya está en uso.')
            return self.form_invalid(form)
       
        user = form.save(commit=False)
        user.is_active = False
        user.save()
       
        sitio = get_current_site(self.request)
       
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = token_activacion.make_token(user)
        mensaje = render_to_string(
            'confirmar_cuenta.html',
            {
                'user': user,
                'sitio': sitio,
                'uid': uid,
                'token': token
            }
        )
       
        asunto = 'Activar cuenta'
        para = user.email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[para],
        )
        email.content_subtype = 'html'
        email.send()
       
        return super().form_valid(form)


class ActivarCuentaView(TemplateView):
    def get(self, request, *args, **kwargs):
        
        try:
            uid = urlsafe_base64_decode(kwargs['uidb64'])
            token = kwargs['token']
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        if user is not None and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            
            messages.success(request, 'Cuenta activada, ingresar datos')
        else:
            messages.error(request, 'Token inválido, contacta al administrador')
            
        return redirect('login')
    
class ListaUsuariosView(LoginRequiredMixin,ListView):
    model = User
    template_name = 'lista_usuarios.html'

    def get_context_data(self, **kwargs):
        context = super(ListaUsuariosView,self).get_context_data(**kwargs)
        context['grupos'] = Group.objects.all()
        return context
    
@login_required
def eliminar_usuario(request, id):
    User.objects.get(id=id).delete()
    return redirect('lista')

@login_required
def asignar_grupos(request):
    id_usuario = request.POST.get('usuario', None)
    
    usuario = User.objects.get(id=id_usuario)
    
    usuario.groups.clear()
    for item in request.POST:
        if request.POST[item] == 'on':
            grupo = Group.objects.get(id=int(item))
            usuario.groups.add(grupo)
    messages.success(request, 'Se agregó el usuario a los grupos')
            
    return redirect('lista')    


class CrearPerfilView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model=DatosPersonales
    form_class = FormDatosPersonales
    success_url = reverse_lazy('bienvenida')
    success_message = "Datos guardados de manera exitosa"

    def form_valid(self, form):
        datos_personales = form.save(commit=False)
        datos_personales.user = self.request.user
        datos_personales.save()
        
        return super().form_valid(form)

class EditarPerfilView(LoginRequiredMixin,UpdateView):
    model=DatosPersonales
    form_class = FormDatosPersonales
    extra_context = {'accion':'Editar'}
    success_url = reverse_lazy('bienvenida')
    success_message = "Datos guardados de manera exitosa"

    def dispatch(self,request,*args,**kwargs):
        self.object=self.get_object()
        return super().dispatch(request,*args,**kwargs)

    def get_object(self,queryset=None):
        return self.request.user.datos
    
def homepage(request):
    # Recupero todas las sucursales
    locations = Location.objects.all()
    # Defino el mapa
    initialMap = folium.Map(location=[22.768345351549794, -102.59867657968344], zoom_start=11)

    # Creamos el Clustering de los marcadores
    latitudes = [location.lat for location in locations]
    longitudes = [location.lng for location in locations]
    popups = [location.name for location in locations]

    FastMarkerCluster(data=list(zip(latitudes, longitudes, popups))).add_to(initialMap)

    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup='Mascota ' + location.name).add_to(initialMap)

    # Usamos _repr_html_() en lugar de repr_html_()
    context = {'map': initialMap._repr_html_()}
    return render(request, 'home.html', context)
