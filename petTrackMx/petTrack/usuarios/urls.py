from django.urls import path, re_path, include
from usuarios import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views

#app_name = 'usuarios'
urlpatterns = [
    # Bienbenida del sitio
    
    #path('', login_required(views.BienvenidaView.as_view()), name='bienvenida'),
    path('salir', login_required(LogoutView.as_view()), name='logout'),
    path('entrar', views.LoginView.as_view(), name='login'),
    path('registrar', views.RegistrarView.as_view(), name='registrar'),
    path('lista', login_required(views.ListaUsuariosView.as_view()), name='lista'),
    path('grupos', login_required(views.asignar_grupos), name='asignar_grupos'),
    path('activar/<slug:uidb64>/<slug:token>', views.ActivarCuentaView.as_view(), name='activar'),
    path('eliminar/<int:id>', views.eliminar_usuario, name='eliminar_usuario2'),
    path('Encargado', login_required(views.CrearPerfilView.as_view()), name='perfil'),
    path('EncargadoEditar', login_required(views.EditarPerfilView.as_view()), name='perfilEditar'),
    path('',login_required(views.homepage), name = 'bienvenida'),
    
    path('restablecer_contrasena/', CustomPasswordResetView.as_view(), name='password_reset1'),
    path('restablecer-contrasena/hecho/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('restablecer-contrasena/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('restablecer-contrasena/completado/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]