from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def sobre_nosotros(request):
    return render(request, 'core/sobrenosotros.html')

def promociones(request):
    return render(request, 'core/promociones.html')

def recetas(request):
    return render(request, 'core/recetas.html')

def error_404(request, exception):
    """Vista personalizada para error 404"""
    return render(request, '404.html', status=404)
