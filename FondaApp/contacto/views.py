from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactoForm


def contacto(request):
    """Vista para mostrar y procesar el formulario de contacto"""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                '¡Gracias por contactarnos! Tu mensaje ha sido enviado exitosamente. '
                'Te responderemos lo antes posible.'
            )
            return redirect('contacto:contacto')
    else:
        form = ContactoForm()
    
    context = {
        'form': form,
        'titulo': 'Contáctanos',
    }
    return render(request, 'contacto/contacto.html', context)
