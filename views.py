from django.shortcuts import render
from .models import Caso

def index(request):
    # Primero veamos todos los casos
    todos_casos = Caso.objects.all()
    print("Total de casos:", todos_casos.count())
    
    # Veamos los tipos de caso que existen
    tipos_casos = Caso.objects.values_list('tipo_caso', flat=True).distinct()
    print("Tipos de casos disponibles:", list(tipos_casos))
    
    # Veamos los estados disponibles
    estados = Caso.objects.values_list('estado', flat=True).distinct()
    print("Estados disponibles:", list(estados))
    
    # Intentemos el filtro original
    casos_no_leidos = Caso.objects.filter(
        tipo_caso='CONNOTACION_SEXUAL',
        estado='NO_LEIDO'
    ).count()
    print(f"Casos no leídos: {casos_no_leidos}")

    context = {
        'casos_no_leidos': casos_no_leidos,
    }
    
    return render(request, 'index.html', context) 