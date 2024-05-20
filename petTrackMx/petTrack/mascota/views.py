from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mascota
from .forms import MascotaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def registrar_mascota(request):
    """
    Permite a un usuario registrar una nueva mascota.
    Si el formulario es válido, guarda la mascota en la base de datos
    y envía un correo electrónico de confirmación al usuario.
    """
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.user = request.user  # Asigna el usuario actual
            mascota.save()
            mascota.enviar_correo_registro()  # Envía el correo de registro
            return redirect('mascotas_lista')  # Redirige a la lista de mascotas
    else:
        form = MascotaForm()
    return render(request, 'registrar_mascota.html', {'form': form})

class ListaConvocatoria(LoginRequiredMixin, ListView):
    """
    Lista todas las mascotas registradas en el sistema.
    Si el usuario es miembro del grupo 'Administrador', muestra todas las mascotas.
    De lo contrario, solo muestra las mascotas del usuario actual.
    """
    model = Mascota

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Administrador').exists():
            # Si el usuario pertenece al grupo 'Administrador', mostrar todas las mascotas
            return queryset
        else:
            # Si el usuario no pertenece al grupo 'Administrador', mostrar solo las mascotas del usuario actual
            return queryset.filter(user=self.request.user)

@login_required
def eliminar_mascota(request, id):
    """
    Elimina una mascota existente del sistema.
    """
    mascota = get_object_or_404(Mascota, id=id)
    mascota.enviar_correo_de_eliminacion()  # Envía el correo de eliminación
    mascota.delete()
    return redirect('mascotas_lista')

@login_required
def editar_mascota(request, id):
    """
    Permite a un usuario editar los detalles de una mascota existente.
    """
    # Obtener la mascota a editar
    mascota = get_object_or_404(Mascota, id=id)
    
    if request.method == 'POST':
        # Llenar el formulario con los datos de la mascota actualizados
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('mascotas_lista')
    else:
        # Llenar el formulario con los datos de la mascota actual
        form = MascotaForm(instance=mascota)
    
    return render(request, 'editar_mascota.html', {'form': form, 'mascota': mascota})
