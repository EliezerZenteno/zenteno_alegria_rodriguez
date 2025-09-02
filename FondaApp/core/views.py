from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def historia(request):
    return render(request, 'core/historia.html')

def sobre_nosotros(request):
    return render(request, 'core/sobre_nosotros.html')

def promociones(request):
    return render(request, 'core/promociones.html')
