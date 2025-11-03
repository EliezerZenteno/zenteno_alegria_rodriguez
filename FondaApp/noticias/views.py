from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posteo, Categoria, Comentario
from django.core.paginator import Paginator
from .forms import PosteoForm, ComentarioForm
from django.db.models import Q


def lista_noticias(request):
    """Vista para mostrar todas las noticias activas con filtros"""
    posteos_list = Posteo.objects.filter(activo=True)
    
    # Filtro 1: Por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        posteos_list = posteos_list.filter(categoria_id=categoria_id)
    
    # Filtro 2: Por autor
    autor_id = request.GET.get('autor')
    if autor_id:
        posteos_list = posteos_list.filter(autor_id=autor_id)
    
    # Filtro 3: Por búsqueda de texto
    busqueda = request.GET.get('buscar')
    if busqueda:
        posteos_list = posteos_list.filter(
            Q(titulo__icontains=busqueda) | Q(contenido__icontains=busqueda)
        )
    
    # Filtro 4: Solo destacados
    destacado = request.GET.get('destacado')
    if destacado == '1':
        posteos_list = posteos_list.filter(destacado=True)
    
    # Ordenamiento
    orden = request.GET.get('orden', '-created')
    posteos_list = posteos_list.order_by(orden)
    
    # Paginación
    paginator = Paginator(posteos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.filter(activo=True)
    
    # Obtener autores únicos
    from django.contrib.auth.models import User
    autores = User.objects.filter(posteos__activo=True).distinct()
    
    context = {
        'posteos': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'categorias': categorias,
        'autores': autores,
        'categoria_seleccionada': categoria_id,
        'autor_seleccionado': autor_id,
        'busqueda': busqueda or '',
        'destacado': destacado,
        'orden': orden,
    }
    return render(request, 'noticias/lista.html', context)


def detalle_noticia(request, pk):
    """Vista para mostrar el detalle de una noticia"""
    posteo = get_object_or_404(Posteo, pk=pk, activo=True)
    
    # Incrementar contador de visitas
    posteo.visitas += 1
    posteo.save(update_fields=['visitas'])
    
    # Obtener comentarios activos
    comentarios = posteo.comentarios.filter(activo=True).select_related('autor')
    
    # Crear instancia del formulario
    comentario_form = ComentarioForm()
    
    context = {
        'posteo': posteo,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
    }
    return render(request, 'noticias/detalle.html', context)


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


@login_required
def crear_comentario(request, pk):
    """Vista para crear un comentario en un posteo"""
    posteo = get_object_or_404(Posteo, pk=pk, activo=True)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.posteo = posteo
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
    
    return redirect('noticias:detalle', pk=pk)
