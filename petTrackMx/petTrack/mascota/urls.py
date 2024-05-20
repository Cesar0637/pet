from django.urls import path, include
from mascota import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # URL para agregar una nueva mascota
    path('Agregar/', views.registrar_mascota, name='nueva_convocatoria'),
    
    # URL para ver la lista de mascotas (requiere autenticación)
    path('Lista_mascotas/', login_required(views.ListaConvocatoria.as_view()), name='mascotas_lista'),
    
    # URL para eliminar una mascota
    path('eliminar_mascota/<int:id>', views.eliminar_mascota, name='eliminar_mascota'),
    
    # URL para editar una mascota
    path('editar_mascota/<int:id>', views.editar_mascota, name='editar_mascota'),
]
