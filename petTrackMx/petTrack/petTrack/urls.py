from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importa las vistas de la aplicación 'usuarios'
from usuarios import views

# Definición de las URL principales del proyecto
urlpatterns = [
    # Ruta para el panel de administración de Django
    path('admin/', admin.site.urls),

    # Ruta principal que incluye las URLs de la aplicación 'usuarios'
    path('', include('usuarios.urls'), name='bienvenida'),

    # Ruta para la aplicación 'mascota'
    path('Mascotas/', include('mascota.urls')),
]

# Añade rutas para servir archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
