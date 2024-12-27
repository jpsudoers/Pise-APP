from django.shortcuts import render
from pise.models import ConnotacionSexual

def index(request):
    # Contar casos de connotación sexual no leídos
    casos_no_leidos = ConnotacionSexual.objects.filter(
        estado='nol'  # Este es el valor definido en el modelo para "No leído"
    ).count()
    
    # Agregar más prints para debug
    print("DEBUG:")
    print(f"Casos no leídos: {casos_no_leidos}")
    print(f"Tipo de casos_no_leidos: {type(casos_no_leidos)}")
    
    # Verificar si hay casos en general
    total_casos = ConnotacionSexual.objects.all().count()
    print(f"Total de casos: {total_casos}")
    
    context = {
        'casos_no_leidos': casos_no_leidos,
    }
    
    return render(request, 'index.html', context)
