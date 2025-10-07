from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posteo
from .forms import PosteoForm


def lista_noticias(request):
    """Vista para mostrar todas las noticias activas"""
    posteos = Posteo.objects.filter(activo=True)
    return render(request, 'noticias/lista.html', {'posteos': posteos})


def detalle_noticia(request, pk):
    """Vista para mostrar el detalle de una noticia"""
    posteo = get_object_or_404(Posteo, pk=pk, activo=True)
    return render(request, 'noticias/detalle.html', {'posteo': posteo})


@login_required
def crear_noticia(request):
    """Vista para crear una nueva noticia"""
    if request.method == 'POST':
        form = PosteoForm(request.POST)
        if form.is_valid():
            posteo = form.save(commit=False)
            posteo.autor = request.user
            posteo.save()
            messages.success(request, 'Noticia creada exitosamente.')
            return redirect('noticias:detalle', pk=posteo.pk)
    else:
        form = PosteoForm()
    return render(request, 'noticias/crear.html', {'form': form})


@login_required
def editar_noticia(request, pk):
    """Vista para editar una noticia existente"""
    posteo = get_object_or_404(Posteo, pk=pk)
    
    # Solo el autor puede editar su posteo
    if posteo.autor != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para editar esta noticia.')
        return redirect('noticias:detalle', pk=posteo.pk)
    
    if request.method == 'POST':
        form = PosteoForm(request.POST, instance=posteo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Noticia actualizada exitosamente.')
            return redirect('noticias:detalle', pk=posteo.pk)
    else:
        form = PosteoForm(instance=posteo)
    return render(request, 'noticias/editar.html', {'form': form, 'posteo': posteo})


@login_required
def eliminar_noticia(request, pk):
    """Vista para eliminar (desactivar) una noticia"""
    posteo = get_object_or_404(Posteo, pk=pk)
    
    # Solo el autor o staff pueden eliminar
    if posteo.autor != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar esta noticia.')
        return redirect('noticias:detalle', pk=posteo.pk)
    
    if request.method == 'POST':
        posteo.activo = False
        posteo.save()
        messages.success(request, 'Noticia eliminada exitosamente.')
        return redirect('noticias:lista')
    
    return render(request, 'noticias/eliminar.html', {'posteo': posteo})
