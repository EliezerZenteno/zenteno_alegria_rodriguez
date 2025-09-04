from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def sobre_nosotros(request):
    return render(request, 'core/sobrenosotros.html')

def promociones(request):
    return render(request, 'core/promociones.html')

def recetas(request):
    return render(request, 'core/recetas.html')
