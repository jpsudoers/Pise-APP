from multiprocessing import context
from pyexpat import model
from unittest import loader
from urllib.request import Request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, View
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from . import models, forms
import os
import pandas as pd
import numpy as np
import datetime as dt
from .forms import ConnotacionSexualForm
from django.contrib import messages

# Create your views here.
class UserLoginView(LoginView):
    pass


def logout_view(request):
    logout(request)
    return render(request, 'login.html')


@login_required
def home_view(request):
    # Inicializar variables
    mensaje = None
    form = None
    correos_lista = []
    
    # Obtener el establecimiento del usuario
    establecimiento_actual = request.user.establecimiento
    print(f"\nEstablecimiento actual: ID={establecimiento_actual.id}, RBD={establecimiento_actual.rbd}")
    
    # Debug de casos de connotación sexual
    print("\nDEBUG - Casos de connotación sexual:")
    todos_casos = models.ConnotacionSexual.objects.all()
    print(f"Total de casos: {todos_casos.count()}")
    
    casos_nol = models.ConnotacionSexual.objects.filter(estado='nol')
    print(f"Casos no leídos: {casos_nol.count()}")
    
    for caso in casos_nol:
        print(f"\nCaso ID: {caso.id}")
        print(f"Estado: {caso.estado}")
        print(f"Víctima ID: {caso.victima_id}")
        try:
            print(f"Víctima establecimiento: {caso.victima.establecimiento.rbd}")
            print(f"¿Coincide?: {caso.victima.establecimiento == establecimiento_actual}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Corregir las matrículas usando el ID correcto
    print("\nCorrigiendo matrículas con ID correcto...")
    try:
        # Obtener el establecimiento correcto por ID
        establecimiento_correcto = models.Establecimiento.objects.get(id=2)  # ID correcto
        
        # Actualizar todas las matrículas que tienen RBD como ID
        matriculas_a_corregir = models.Matricula.objects.filter(establecimiento_id=26005)
        print(f"Matrículas a corregir: {matriculas_a_corregir.count()}")
        
        # Actualizar usando el ID correcto
        matriculas_a_corregir.update(establecimiento_id=establecimiento_correcto.id)
        print(f"Matrículas actualizadas al establecimiento ID={establecimiento_correcto.id}")
        
        # Verificar la actualización
        for m in matriculas_a_corregir:
            m.refresh_from_db()  # Recargar los datos de la base de datos
            print(f"Matrícula {m.id} actualizada - Establecimiento ID: {m.establecimiento_id}")
    except Exception as e:
        print(f"Error al corregir matrículas: {str(e)}")
    
    # Ahora obtener los casos usando el ID correcto
    casos = {
        'connotacion_sexual': models.ConnotacionSexual.objects.filter(
            estado='nol',
            victima__establecimiento_id=establecimiento_actual.id  # Usar ID en lugar de objeto
        ).count(),
        'maltrato': models.Maltrato.objects.filter(
            estado='nol',
            victima__establecimiento_id=establecimiento_actual.id
        ).count(),
        'accidente_escolar': models.AccidenteEscolar.objects.filter(
            estado='nol',
            accidentado__establecimiento_id=establecimiento_actual.id
        ).count(),
        'vulneracion_derechos': models.VulneracionDerechosFuncionarios.objects.filter(
            estado='nol',
            funcionario_afectado__establecimiento_id=establecimiento_actual.id
        ).count(),
        'dificultad_consejo': models.DificultadConstitucionConsejo.objects.filter(
            estado='nol',
            funcionario_afectado__establecimiento_id=establecimiento_actual.id
        ).count()
    }
    
    # Debug de conteos
    print("\nDEBUG - Conteo de casos:")
    for tipo, cantidad in casos.items():
        print(f"- {tipo}: {cantidad}")
    
    # Debug final
    print("\nVerificación final:")
    casos_nol = models.ConnotacionSexual.objects.filter(estado='nol')
    for caso in casos_nol:
        print(f"\nCaso {caso.id}:")
        print(f"- Víctima: {caso.victima_id}")
        print(f"- Establecimiento: {caso.victima.establecimiento_id}")
        print(f"- ¿Coincide?: {caso.victima.establecimiento_id == establecimiento_actual.id}")
    
    context = {
        'mensaje': mensaje,
        'form': form,
        'correos': correos_lista,
        'casos': casos,
    }
    
    return render(request, 'index.html', context)


def descarga_archivo_accidente_escolar(request):
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f'BASE DIR URL == {BASE_DIR}')
    filename = 'dec.pdf'
    filepath = BASE_DIR + '/media/dec/' + filename
    path = open(filepath, 'r')
    import mimetypes

    mime_type, _ = mimetypes.guess_type("/media/dec/dec.pdf")
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment;"
    return response

#region Matricula
class MatriculaEstablecimientoListView(LoginRequiredMixin,ListView):
    model = models.Matricula
    context_object_name = 'casos_list'
    template_name = 'matriculas/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(
                establecimiento = self.request.user.establecimiento
            ).filter(esta_activo = True)
        
        return qs

class MatriculaEstablecimientoDetailView(LoginRequiredMixin, DetailView):
    model = models.Matricula
    context_object_name = 'matricula'
    template_name = 'matriculas/detail_case.html'

class MatriculaEstablecimientoUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Matricula
    template_name = 'matriculas/update_case.html'
    form_class = forms.MatriculaEstablecimientoEditForm
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(MatriculaEstablecimientoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        instance = self.get_object()
        return reverse('matricula_detail',kwargs={'pk': instance.pk })

def CargarNominaMatriculas(request):
    fs = FileSystemStorage()
    repetido = []
    try:
        if request.method == 'POST' and request.FILES['importData']:
            myfile = request.FILES['importData']        
            filename = fs.save(myfile.name, myfile)
            excel_file = os.path.join(settings.MEDIA_ROOT,filename) 
            read_file = pd.read_excel (excel_file)
            dtframe = pd.DataFrame(read_file)
            dtframe.fillna('',inplace=True)
            dtframe['Telefono'] = dtframe['Telefono'].astype(str).replace(r'\.0', '', regex=True)
            dtframe['Celular'] = dtframe['Celular'].astype(str).replace(r'\.0', '', regex=True)
            dbframe = dtframe
            for dbframe in dbframe.itertuples():
                if str(request.user.establecimiento.rbd) == str(dbframe.RBD):
                    establecimiento = request.user.establecimiento

                    if dbframe._21 >= dbframe._22:
                        activo=1
                    else:
                        activo=0
                    try:
                        obj = models.Matricula.objects.get(rut=dbframe.Run)
                        repetido.append(obj)
                    except models.Matricula.DoesNotExist:
                        obj = models.Matricula(rut=dbframe.Run,dv=dbframe._8, nombres=dbframe.Nombres, apellido_paterno=dbframe._11,  apellido_materno=dbframe._12,
                                                domicilio_actual=dbframe.Dirección, Comuna_residencia=dbframe._14, email=dbframe.Email, telefono=dbframe.Telefono, celular=dbframe.Celular,
                                                fecha_nacimiento=dbframe._19, codigo_etnia=dbframe._20, nivel=dbframe._5, letra=dbframe._6, año=dbframe.Año,fecha_incorporacion=dbframe._21,
                                                fecha_retiro=dbframe._22, esta_activo=activo, establecimiento=establecimiento, genero=dbframe.Genero)
                        obj.save() 
                else:
                     mensaje = '%s no corresponde a esta institucion, verifique su RBD'%filename  
            os.remove(excel_file)
            if len(repetido) > 0 :
                mensaje = 'Se ha cargado exitosamente %s ignorando %d registros al ya existir'%(filename,len(repetido))
            else:
                mensaje = 'Se ha cargado exitosamente %s'%filename
            return render(request, 'matriculas/create_case.html', {'alumnos':repetido,'mensaje': mensaje})       
                   
    except Exception as identifier:            
        mensaje = identifier
    return render(request, 'matriculas/create_case.html')    

class MatriculaEstablecimientoCreateView(LoginRequiredMixin, CreateView):
    model = models.Matricula
    template_name = 'matriculas/create_unique.html'
    context_object_name = 'caso'

    def get(self, request, *args, **kwargs):
        context = {'form': forms.MatriculaEstablecimientoCreateForm()}
        return render(request, 'matriculas/create_unique.html', context)

    def post(self, request, *args, **kwargs):
        form = forms.MatriculaEstablecimientoCreateForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.esta_activo = True
            alumno.establecimiento = self.request.user.establecimiento
            alumno.save()
        return HttpResponseRedirect(reverse_lazy('matricula_detail', args=[alumno.id]))
#endregion


class DiscriminacionListView(LoginRequiredMixin,ListView):
    model = models.Discriminacion
    context_object_name = 'casos_list'
    template_name = 'discriminacion/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.Discriminacion.objects.all()
        else:
            qs = models.Discriminacion.objects.filter(
                victima__establecimiento = self.request.user.establecimiento
            )
        
        return qs



class CasoCreateView(CreateView):
    model = models.CasoVulneracion
    fields = ['fecha_creacion']
    template_name = 'caso/create.html'
    context_object_name = 'caso'

    def get(self, request, *args, **kwargs):
        context = {'form': forms.CasoVulneracion()}
        return render(request, 'caso/create.html', context)


    def get_success_url(self) -> str:
        return reverse('discriminacion_add', kwargs={'pk': self.object.id})



class DiscriminacionDetailView(LoginRequiredMixin, DetailView):
    model = models.Discriminacion
    context_object_name = 'caso'
    template_name = 'discriminacion/detail_case.html'



class DiscriminacionCreateView(LoginRequiredMixin, CreateView):
    model = models.Discriminacion
    fields = ['tipo_discrim','detalle','victima', 'agresor', 'fecha_creacion']
    template_name = 'discriminacion/create_case.html'
    context_object_name = 'caso'
    

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs


    def get(self, request, *args, **kwargs):
        form = forms.DiscriminacionCreateForm()
        form.fields['agresor'].queryset = self.get_matriculas()
        form.fields['victima'].queryset = self.get_matriculas()
        context = {'form' : form, 'caso': forms.CasoVulneracion()}
        return render(request, 'discriminacion/create_case.html', context)

    
    # def post(self, request, *args, **kwargs):
    #     otro_campo = request.POST.get('otro')
    #     print(otro_campo)
    #     print("QUI SE SUPONE QUE PUEDO HACER ALGO")

    #     return super(DiscriminacionCreateView, self).post(self)

    def get_success_url(self) -> str:
        return reverse('discriminacion_detail', kwargs={'pk': self.object.pk})

     
    # def form_valid(self, form):
    #     form.instance.caso = models.CasoVulneracion.objects.get(pk=self.kwargs['pk'])
    #     print(form.fields)

    #     return super(DiscriminacionCreateView, self).form_valid(form)



class CasoUpdateView(UpdateView):
    model = models.CasoVulneracion
    template_name = 'caso/update.html'
    fields = ['estado']

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('discriminacion_detail',kwargs={'pk': instance.discriminacion_set.all().first().pk })
        # super().get_success_url()
    



def medidas_discriminacion_view(request, pk):
    """
        CREAR MEDIDAS
    """
    caso = models.Discriminacion.objects.get(pk=pk)
    form = forms.MedidasDiscriminacion(initial={'caso': caso})

    if request.method == 'POST':
        form = forms.MedidasDiscriminacion(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.caso = caso
            obj.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('discriminacion_detail', kwargs={'pk': pk}))
    
    if request.method == 'GET':
        if caso.medidasdiscriminacion_set.all():
            medidas = caso.medidasdiscriminacion_set.all().first()
            form = forms.MedidasDiscriminacion(instance=medidas)

    return render(request, 'discriminacion/medidas/discriminacion_medidas.html', {'form': form, 'caso': caso})


def actualizar_medidas_discriminacion(request, pk):
    """
        EDICION DE MEDIDAS DISCRIMINACION
        el @param: pk viene del path el cual es el ID del caso Discriminacion.
        Se obtiene el primer elemento de medidas_discriminacion del caso seleccionado.

        se inicializa el formulario con ese caso.
        
        
    """
    caso = models.Discriminacion.objects.get(pk=pk)
    
    objeto_medidas = caso.medidasdiscriminacion_set.all().first()


    form = forms.MedidasDiscriminacion(initial={'caso': caso})

    if request.method == 'POST':
        form = forms.MedidasDiscriminacion(request.POST or None, instance=objeto_medidas)
        print(form)
    
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('discriminacion_detail', kwargs={'pk': pk}))
    
    if request.method == 'GET':
        if caso.medidasdiscriminacion_set.all():
            medidas = caso.medidasdiscriminacion_set.all().first()
            form = forms.MedidasDiscriminacion(instance=medidas)

    return render(request, 'discriminacion/medidas/discriminacion_medidas.html', {'form': form, 'caso': caso})


class CasoMaltratoCreateView(LoginRequiredMixin, CreateView):
    model = models.CasoVulneracion
    fields = ['fecha_creacion']
    template_name = 'caso/create.html'
    context_object_name = 'caso'

    def get(self, request, *args, **kwargs):
        context = {'form': forms.CasoVulneracion()}
        return render(request, 'caso/create.html', context)

    def get_success_url(self) -> str:
        return reverse('maltrato_add', kwargs={'pk': self.object.id})



class MaltratoCreateView(LoginRequiredMixin, CreateView):
    model = models.Maltrato
    fields = ['tipo_maltrato', 'detalle','victima', 'fecha_creacion', 'funcionario_agresor']
    template_name = 'maltrato/create_case.html'
    context_object_name = 'maltrato'

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs


    def get(self, request, *args, **kwargs):
        form = forms.MaltratoCreateForm()
        form.fields['victima'].queryset = self.get_matriculas()
        context = {'form': form}
        return render(request, 'maltrato/create_case.html', context)


    def form_valid(self, form):
        form.instance.estado = 'nol'
        # Asegurarnos que el tipo sea válido
        if not form.instance.tipo_maltrato:
            form.instance.tipo_maltrato = 'apoderado'
        print(f"DEBUG - tipo_maltrato antes de guardar: {form.instance.tipo_maltrato}")
        print(f"DEBUG - funcionario_victima antes de guardar: {form.instance.funcionario_victima}")
        response = super().form_valid(form)
        messages.success(self.request, 'Caso de maltrato creado exitosamente')
        return response



class MaltratoDetailView(LoginRequiredMixin, DetailView):
    model = models.Maltrato
    context_object_name = 'caso'
    template_name = 'maltrato/detail_case.html'


class MaltratoListView(LoginRequiredMixin, ListView):
    model = models.Maltrato
    context_object_name = 'casos_list'
    template_name = 'maltrato/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.Maltrato.objects.all()
        else:
            qs = models.Maltrato.objects.filter(
                models.Q(victima__establecimiento=self.request.user.establecimiento) |
                models.Q(funcionario_victima__establecimiento=self.request.user.establecimiento)
            )
        return qs

# CONNOTACION SEXUAL
'''
class ConnotacionSexualCreateView(LoginRequiredMixin, CreateView):
    model = models.ConnotacionSexual
    fields = ['tipo_connotacion_sexual', 'detalle', 'victima']
    template_name = 'connotacion/create_case.html'
    context_object_name = 'caso'

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        """
        Método GET, se configura queryset para el campo victima
        """
        form = forms.ConnotacionSexualCreateForm()
        form.fields['victima'].queryset = self.get_matriculas()
        context = {'form' : form, 'caso': forms.CasoVulneracion()}
        return render(request, 'connotacion/create_case.html', context)

     
    def form_valid(self, form):
        form.instance.caso = models.CasoVulneracion.objects.get(pk=self.kwargs['pk'])

        return super(ConnotacionSexualCreateView, self).form_valid(form)
'''
    
class ConnotacionSexualDetailView(LoginRequiredMixin, DetailView):
    model = models.ConnotacionSexual
    context_object_name = 'caso'
    template_name = 'connotacion/detail_case.html'


class ConnotacionSexualListView(LoginRequiredMixin, ListView):
    model = models.ConnotacionSexual
    context_object_name = 'casos_list'
    template_name = 'connotacion/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.ConnotacionSexual.objects.all()
        else:
            qs = models.ConnotacionSexual.objects.filter(
                victima__establecimiento=self.request.user.establecimiento
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar información de casos no leídos
        context['casos_no_leidos'] = {
            caso.id: True for caso in context['casos_list'] 
            if caso.estado == 'nol'
        }
        return context

    
'''
class CasoConnotacionCreateView(LoginRequiredMixin, CreateView):
    
    model = models.CasoVulneracion
    fields = ['fecha_creacion']
    template_name = 'caso/create.html'
    context_object_name = 'caso'

    def get(self, request, *args, **kwargs):
        context = {'form': forms.CasoVulneracion()}
        return render(request, 'caso/create.html', context)

    def get_success_url(self) -> str:
        return reverse('connotacion_add', kwargs={'pk': self.object.id})
'''
    
class FullConnotacionSexualCreateView(LoginRequiredMixin, CreateView):
    model = models.ConnotacionSexual
    fields = ['tipo_connotacion_sexual', 'detalle', 'victima', 'fecha_creacion']
    template_name = 'connotacion/create_case.html'
    context_object_name = 'caso'

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.ConnotacionSexualForm()
        form.fields['victima'].queryset = self.get_matriculas()
        context = {'form': form}
        return render(request, 'connotacion/create_case.html', context)

    def post(self, request, *args, **kwargs):
        form = forms.ConnotacionSexualForm(request.POST, request.FILES)
        if form.is_valid():
            caso = form.save()
            return HttpResponseRedirect(reverse('connotacion_detail', args=[caso.id]))
        return render(request, 'connotacion/create_case.html', {'form': form})


"""
ACTUALIZACION DE ESTADO PARA CASOS
"""
class ConnotacionSexualUpdateView(UpdateView):
    model = models.ConnotacionSexual
    template_name = 'connotacion/update_case.html'
    # fields = ['estado']
    form_class = forms.EstadoConnotacionSexualCreateForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ConnotacionSexualUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('connotacion_detail',kwargs={'pk': instance.pk })
        # super().get_success_url()


class MaltratoUpdateView(UpdateView):
    model = models.Maltrato
    template_name = 'maltrato/update_case.html'
    # fields = ['estado']
    form_class = forms.EstadoMaltratoCreateForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(MaltratoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('maltrato_detail',kwargs={'pk': instance.pk })
        # super().get_success_url()


class DiscriminacionUpdateView(UpdateView):
    model = models.Discriminacion
    template_name = 'discriminacion/update_case.html'
    form_class = forms.EstadoDiscriminacionCreateForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DiscriminacionUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('discriminacion_detail',kwargs={'pk': instance.pk })
        # super().get_success_url()


def medidas_maltrato_view(request, pk):
    caso = models.Maltrato.objects.get(pk=pk)
    form = forms.MedidasMaltratoForm(initial={'caso': caso})

    if request.method == 'POST':
        form = forms.MedidasMaltratoForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.caso = caso
            obj.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('maltrato_detail', kwargs={'pk': pk}))

    return render(request, 'maltrato/medidas/maltrato_medidas.html', {'form': form, 'caso': caso})


class MedidasMaltratoCreate(CreateView):
    model = models.MedidasMaltrato
    template_name = 'maltrato/medidas/create_medidas.html'
    form_class = forms.MedidasMaltratoForm

    def get(self, request, *args, **kwargs):
        print(self.kwargs['pk'])
        form = forms.MedidasMaltratoForm()
        context = {'form' : form}
        return render(request, 'discriminacion/create_case.html', context)

    def get_success_url(self) -> str:
        instance = self.get_object()
        print("este seria LA ID DEL CASO MALTRATO",instance.caso.pk)
        return HttpResponseRedirect(reverse('maltrato_detail', kwargs={'pk': self.kwargs['pk']}))
    
    def form_valid(self, form):
        form.instance.caso = models.Maltrato.objects.get(pk=self.kwargs['pk'])
        print(form.fields)
        return super(MedidasMaltratoCreate, self).form_valid(form)
    

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        print(self.kwargs['pk'])
        return reverse('maltrato_detail', kwargs={'pk': self.kwargs['pk']})


class MedidasMaltratoView(UpdateView):
    model = models.MedidasMaltrato
    template_name = 'maltrato/medidas/maltrato_medidas.html'
    form_class = forms.MedidasMaltratoForm

    def get_success_url(self) -> str:
        # print(self.request.)
        instance = self.get_object()
        return reverse('maltrato_detail', kwargs={'pk': instance.caso.pk})


"""
    ListView para Accidente, Falta y Derivacion
"""
class AccidenteEscolarListView(LoginRequiredMixin,ListView):
    model = models.AccidenteEscolar
    context_object_name = 'casos_list'
    template_name = 'accidente/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.AccidenteEscolar.objects.all()
        else:
            qs = models.AccidenteEscolar.objects.filter(
                accidentado__establecimiento = self.request.user.establecimiento
            )
        
        return qs


class AccidenteEscolarEstadoUpdateView(UpdateView):
    model = models.AccidenteEscolar
    template_name = 'accidente/update_status.html'
    form_class = forms.AccidenteEscolarActualizarEstadoForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AccidenteEscolarEstadoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('detail_accidente',kwargs={'pk': instance.pk })
        # super().get_success_url()


class FaltaConvivenciaListView(ListView):
    model = models.FaltaConvivencia
    context_object_name = 'casos_list'
    template_name = 'faltas/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.FaltaConvivencia.objects.all()
        else:
            qs = models.FaltaConvivencia.objects.filter(
                accidentado__establecimiento = self.request.user.establecimiento
            )
        
        return qs


"""
    CreateView para Accidente, Falta y Derivacion
"""

class AccidenteEscolarCreateView(LoginRequiredMixin, CreateView):
    model = models.AccidenteEscolar
    template_name = 'accidente/create_case.html'
    context_object_name = 'caso'
    form_class = forms.AccidenteEscolarForm

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.AccidenteEscolarForm()
        form.fields['accidentado'].queryset = self.get_matriculas()
        context = {'form' : form, }
        return render(request, 'accidente/create_case.html', context)


class AccidenteEscolarUpdateView(LoginRequiredMixin, UpdateView):
    model = models.AccidenteEscolar
    template_name = 'accidente/update_case.html'
    context_object_name = 'caso'
    form_class = forms.AccidenteEscolarForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AccidenteEscolarUpdateView, self).get(request, *args, **kwargs)
    
    
    def get_success_url(self) -> str:
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('detail_accidente',kwargs={'pk': instance.pk })

    
class AccidenteEscolarDetailView(LoginRequiredMixin, DetailView):
    model = models.AccidenteEscolar
    context_object_name = 'caso'
    template_name = 'accidente/detail_case.html'



def medidas_maltrato_view(request, pk):
    """
        CREAR MEDIDAS
    """
    caso = models.Maltrato.objects.get(pk=pk)
    form = forms.MedidasMaltratoForm(initial={'caso': caso})

    if request.method == 'POST':
        form = forms.MedidasMaltratoForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.caso = caso
            obj.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('maltrato_detail', kwargs={'pk': pk}))
    
        # if caso.medidasmaltrato:
        #     print("Este es la entidad")
            # print("Hay caso...")
            # medidas = caso.medidasmaltrato_set.all().first()
            # form = forms.MedidasMaltratoForm(instance=medidas)
            # print(medidas)

    return render(request, 'maltrato/medidas/maltrato_medidas.html', {'form': form, 'caso': caso})



def actualizar_medidas_maltratos(request, pk):

    caso = models.Maltrato.objects.get(pk=pk)
    
    objeto_medidas = caso.medidasmaltrato

    form = forms.MedidasMaltratoForm(initial={'caso': caso})

    if request.method == 'POST':
        form = forms.MedidasMaltratoForm(request.POST or None, instance=objeto_medidas)
        print(form)
    
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('maltrato_detail', kwargs={'pk': pk}))
    
    if request.method == 'GET':
        if caso.medidasmaltrato:
            medidas = caso.medidasmaltrato
            form = forms.MedidasMaltratoForm(instance=medidas)

    return render(request, 'maltrato/medidas/maltrato_medidas.html', {'form': form, 'caso': caso})



class ReportesView(TemplateView):
    """
    Vista genérica basa en clase (Base-class function) para datos generales de cada caso,
    como cantidad de casos y filtros para obtener ciertos casos:
    Fecha, Estado, Tipo de Caso
    """

    template_name= 'reportes/report.html'

    def get_context_data(self, **kwargs):
        # fecha = None
        # estado = None
        # tipo = None

        context = super().get_context_data(**kwargs)

        # if self.request.GET.get('fecha') :
        #     fecha = self.request.GET.get('fecha')
        #     context["fecha"] = fecha
        
        # if self.request.GET.get('estado') :
        #     estado = self.request.GET.get('estado')
        #     context["estado"] = estado

        # if self.request.GET.get('tipo') :
        #     tipo = self.request.GET.get('tipo')
        #     context["tipo"] = tipo

        if self.request.user.is_admin:
            #context['casos_discriminaciones'] = models.Discriminacion.objects.all()
            context['casos_connotacion'] = models.ConnotacionSexual.objects.all()
            context['casos_maltrato'] = models.Maltrato.objects.all()
            context['casos_accidentes'] = models.AccidenteEscolar.objects.all()
            context['casos_vulneracion'] = models.VulneracionDerechosFuncionarios.objects.all()
            context['casos_dificultad'] = models.DificultadConstitucionConsejo.objects.all()
            
        else:
            #context['casos_discriminaciones'] = models.Discriminacion.objects.filter(victima__establecimiento = self.request.user.establecimiento)
            context['casos_connotacion'] = models.ConnotacionSexual.objects.filter(victima__establecimiento = self.request.user.establecimiento)
            context['casos_maltrato'] = models.Maltrato.objects.filter(victima__establecimiento = self.request.user.establecimiento)
            context['casos_accidentes'] = models.AccidenteEscolar.objects.filter(accidentado__establecimiento = self.request.user.establecimiento)
            context['casos_vulneracion'] = models.VulneracionDerechosFuncionarios.objects.filter(funcionario_afectado__establecimiento = self.request.user.establecimiento)
            context['casos_dificultad'] = models.DificultadConstitucionConsejo.objects.filter(funcionario_afectado__establecimiento = self.request.user.establecimiento)

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('tipo'):
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


def report_vulneracion(request, pk):
    from .reports.maltrato_report import ReporteMaltrato
    #Crea objeto ReporteMaltrato con el caso obtenido
    report_vulneracion = ReporteMaltrato(models.Maltrato.objects.get(pk=pk), request)
    #obtiene un HttpResponse con el PDF listo para retornar.
    documento = report_vulneracion.create_pdf()
    #Retorna el Response
    return documento


def report_discriminacion(request, pk):
    from .reports.discriminacion_report import ReporteDiscriminacion
    #Crea objeto ReporteMaltrato con el caso obtenido
    report_vulneracion = ReporteDiscriminacion(models.Discriminacion.objects.get(pk=pk), request)
    #obtiene un HttpResponse con el PDF listo para retornar.
    documento = report_vulneracion.create_pdf()
    #Retorna el Response
    return documento


def report_connotacionsexual(request, pk):
    from .reports.connotacion_report import ReporteConnotacionSexual
    #Crea objeto ReporteMaltrato con el caso obtenido
    report_vulneracion = ReporteConnotacionSexual(models.ConnotacionSexual.objects.get(pk=pk), request)
    #obtiene un HttpResponse con el PDF listo para retornar.
    documento = report_vulneracion.create_pdf()
    #Retorna el Response
    return documento


def report_vulneracion_derechos_funcionario(request, pk):
    from .reports.vulneracion_derechos_funcionario_report import ReportVulneracionDerechosFuncionarios
    #Crea objeto ReporteMaltrato con el caso obtenido
    report_vulneracion = ReportVulneracionDerechosFuncionarios(
        models.VulneracionDerechosFuncionarios.objects.get(pk=pk), 
        request)
    #obtiene un HttpResponse con el PDF listo para retornar.
    documento = report_vulneracion.create_pdf()
    #Retorna el Response
    return documento


def report_dificultad_consejo_escolar(request, pk):
    from .reports.dificultad_constitucion_consejo import ReportDificultadConstitucionConsejo
    #Crea objeto ReporteMaltrato con el caso obtenido
    report_vulneracion = ReportDificultadConstitucionConsejo(
        models.DificultadConstitucionConsejo.objects.get(pk=pk), 
        request)
    #obtiene un HttpResponse con el PDF listo para retornar.
    documento = report_vulneracion.create_pdf()
    #Retorna el Response
    return documento

"""
Nuevas Vistas Create/Detail/List/Update
    para: DificultadConstitucionConsejo
"""
class DificultadConstitucionCreateView(CreateView):
    model = models.DificultadConstitucionConsejo
    fields = ['tipo_consejos', 'funcionario_afectado', 'fecha', 'detalle']
    template_name = 'dificultad_constitucion/create_case.html'
    context_object_name = 'caso'

    def get_funcionarios(self):
        if self.request.user.is_admin:
            qs = models.FuncionarioEstablecimiento.objects.all()
        else:
            qs = models.FuncionarioEstablecimiento.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.DificultadConstitucionConsejoForm()
        form.fields['funcionario_afectado'].queryset = self.get_funcionarios()
        context = {'form' : form,}
        return render(request, 'dificultad_constitucion/create_case.html', context)



class DificultadConstitucionDetailView(DetailView):
    model = models.DificultadConstitucionConsejo
    context_object_name = 'caso'
    template_name= 'dificultad_constitucion/detail_case.html'


class DificultadConstitucionListView(LoginRequiredMixin,ListView):
    model = models.DificultadConstitucionConsejo
    context_object_name = 'casos_list'
    template_name = 'dificultad_constitucion/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.DificultadConstitucionConsejo.objects.all()
        else:
            qs = models.DificultadConstitucionConsejo.objects.filter(
                funcionario_afectado__establecimiento = self.request.user.establecimiento
            )
        
        return qs


    

"""
Nuevas Vistas Create/Detail/List/Update
    para: VulneracionDerechosFuncionarios
"""

class VulneracionDerechosFuncionariosCreateView(CreateView):
    model = models.VulneracionDerechosFuncionarios
    fields = ['tipo_vulneracion', 'funcionario_afectado', 'fecha', 'detalle']
    template_name = 'vulneracionderechos_funcionarios/create_case.html'
    context_object_name = 'caso'

    def get_funcionarios(self):
        if self.request.user.is_admin:
            qs = models.FuncionarioEstablecimiento.objects.all()
        else:
            qs = models.FuncionarioEstablecimiento.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.VulneracionDerechosFuncionariosForm()
        form.fields['funcionario_afectado'].queryset = self.get_funcionarios()
        context = {'form' : form,}
        return render(request, 'vulneracionderechos_funcionarios/create_case.html', context)


class VulneracionDerechosFuncionariosDetailView(DetailView):
    model = models.VulneracionDerechosFuncionarios
    context_object_name = 'caso'
    template_name= 'vulneracionderechos_funcionarios/detail_case.html'



class VulneracionDerechosFuncionariosListView(LoginRequiredMixin,ListView):
    model = models.VulneracionDerechosFuncionarios
    context_object_name = 'casos_list'
    template_name = 'vulneracionderechos_funcionarios/list_case.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.VulneracionDerechosFuncionarios.objects.all()
        else:
            qs = models.VulneracionDerechosFuncionarios.objects.filter(
                funcionario_afectado__establecimiento = self.request.user.establecimiento
            )
        
        return qs


class VulneracionFuncionariosEstadoUpdateView(UpdateView):
    model = models.VulneracionDerechosFuncionarios
    template_name = 'vulneracionderechos_funcionarios/update_status.html'
    # fields = ['estado']
    form_class = forms.EstadoVulneracionFuncionariosUpdateForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(VulneracionFuncionariosEstadoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('detail_vulneracion_funcionario',kwargs={'pk': instance.pk })
        # super().get_success_url()


class DificultadConsejoEstadoUpdateView(UpdateView):
    model = models.DificultadConstitucionConsejo
    template_name = 'dificultad_constitucion/update_status.html'
    # fields = ['estado']
    form_class = forms.EstadoDificultadConsejoUpdateForm
    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(DificultadConsejoEstadoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        
        instance = self.get_object()
        # print(instance.discriminacion_set.all().first().pk)
        return reverse('detail_dificultad',kwargs={'pk': instance.pk })
        # super().get_success_url()
    

class MaltratoAlumnoToAlumnoCreateView(CreateView):
    model = models.Maltrato
    fields = ['victima', 'fecha_creacion', 'detalle', 'alumno_agresor']
    template_name = 'maltrato/create_case_alumno_alumno.html'
    context_object_name = 'caso'

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.MaltratoAlumnoToAlumnoCreateForm()
        form.fields['victima'].queryset = self.get_matriculas()
        form.fields['alumno_agresor'].queryset = self.get_matriculas()
        context = {'form' : form,}
        return render(request, 'maltrato/create_case_alumno_alumno.html', context)


class MaltratoFuncionarioToAlumnoCreateView(CreateView):
    model = models.Maltrato
    fields = ['victima', 'fecha_creacion', 'detalle', 'funcionario_agresor']
    template_name = 'maltrato/create_case_adulto_menor.html'
    context_object_name = 'caso'

    def get_matriculas(self):
        if self.request.user.is_admin:
            qs = models.Matricula.objects.all()
        else:
            qs = models.Matricula.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs
    
    def get_funcionarios(self):
        if self.request.user.is_admin:
            qs = models.FuncionarioEstablecimiento.objects.all()
        else:
            qs = models.FuncionarioEstablecimiento.objects.filter(establecimiento = self.request.user.establecimiento)
        return qs

    def get(self, request, *args, **kwargs):
        form = forms.MaltratoFuncionarioToAlumnoCreateForm()
        form.fields['victima'].queryset = self.get_matriculas()
        form.fields['funcionario_agresor'].queryset = self.get_funcionarios()
        context = {'form' : form,}
        return render(request, 'maltrato/create_case_adulto_menor.html', context)
    
    def post(self, request, *args, **kwargs):
        form = forms.MaltratoFuncionarioToAlumnoCreateForm(request.POST)
        if form.is_valid():
            caso_maltrato_funcionario_to_alumno = form.save(commit=False)
            caso_maltrato_funcionario_to_alumno.tipo_maltrato = 'adulto'
            print(str(caso_maltrato_funcionario_to_alumno.tipo_maltrato))
            caso_maltrato_funcionario_to_alumno.save()
        return HttpResponseRedirect(reverse_lazy('maltrato_detail', args=[caso_maltrato_funcionario_to_alumno.id]))

class MaltratoAdultoToAdultoCreateView(LoginRequiredMixin, CreateView):
    model = models.Maltrato
    form_class = forms.MaltratoAdultoAdultoForm
    template_name = 'maltrato/form.html'
    success_url = reverse_lazy('maltrato_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['establecimiento'] = self.request.user.establecimiento
        return kwargs

    def form_valid(self, form):
        # No llamar a save() aquí, dejar que CreateView lo maneje
        form.instance.estado = 'nol'
        form.instance.tipo_maltrato = 'apoderado'  # Este es el valor de la clave, no el display
        print(f"DEBUG - tipo_maltrato antes de guardar: {form.instance.tipo_maltrato}")
        print(f"DEBUG - funcionario_victima antes de guardar: {form.instance.funcionario_victima}")
        response = super().form_valid(form)  # Esto guardará el objeto
        messages.success(self.request, 'Caso de maltrato creado exitosamente')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Caso de Maltrato entre Adultos'
        return context


"""
    FUNCIONARIOS MODELS
"""
#region Funcionario
class FuncionarioEstablecimientoListView(ListView):
    model = models.FuncionarioEstablecimiento
    context_object_name = 'list'
    template_name = 'funcionarios/list.html'

    def get_queryset(self):
        if self.request.user.is_admin:
            qs = models.FuncionarioEstablecimiento.objects.all()
        else:
            qs = models.FuncionarioEstablecimiento.objects.filter(
                establecimiento = self.request.user.establecimiento
            )        
        return qs
    pass

class FuncionarioEstablecimientoDetailView(DetailView):
    model = models.FuncionarioEstablecimiento
    context_object_name = 'funcionario'
    template_name= 'funcionarios/detail.html'
    pass

class FuncionarioEstablecimientoUpdateView(UpdateView):
    model = models.FuncionarioEstablecimiento
    template_name = 'funcionarios/updates.html'
    form_class = forms.FuncionarioEstablecimientoUpdateForm
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FuncionarioEstablecimientoUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        instance = self.get_object()
        return reverse('funcionario_detail',kwargs={'pk': instance.pk })

class FuncionarioEstablecimientoCreateView(CreateView):
    model = models.FuncionarioEstablecimiento
    template_name = 'funcionarios/create.html'
    context_object_name = 'funcionario'

    def get(self, request, *args, **kwargs):
        context = {'form': forms.FuncionarioEstablecimientoCreateForm}
        return render(request, 'funcionarios/create.html', context)

    def post(self, request, *args, **kwargs):
        try:
            form = forms.FuncionarioEstablecimientoCreateForm(request.POST)
            if form.is_valid():
                funcionario = form.save(commit=False)
                funcionario.establecimiento = self.request.user.establecimiento
                funcionario.save()
            return HttpResponseRedirect(reverse_lazy('funcionario_detail', args=[funcionario.id]))
        except Exception as e:
            mensaje = 'Ya existe un registro con este RUN'
            context = {'form': forms.FuncionarioEstablecimientoCreateForm, 'mensaje': mensaje}
            return render(request, self.template_name, context)
#endregion

#region Establecimiento
class EstablecimientoUsuarioDetailView(LoginRequiredMixin,DetailView):
    model = models.Establecimiento
    context_object_name = 'detail'
    template_name = 'ajustes/detail.html'    
    pass

class EstablecimientoUsuarioUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Establecimiento
    template_name = 'ajustes/updates.html'
    form_class = forms.EstablecimientoUsuarioUpdateForm
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(EstablecimientoUsuarioUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        instance = self.get_object()
        return reverse('detail',kwargs={'pk': instance.pk })
#endregion

class ProtocoloUploadView(LoginRequiredMixin, CreateView):
    model = models.ProtocoloInstitucional
    form_class = forms.ProtocoloInstitucionalForm
    template_name = 'protocolos/upload.html'
    
    def form_valid(self, form):
        form.instance.establecimiento = self.request.user.establecimiento
        form.instance.tipo = self.kwargs['tipo']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('protocolo_list', kwargs={'tipo': self.kwargs['tipo']})

class ProtocoloListView(LoginRequiredMixin, ListView):
    model = models.ProtocoloInstitucional
    template_name = 'protocolos/list.html'
    context_object_name = 'protocolos'
    
    def get_queryset(self):
        return models.ProtocoloInstitucional.objects.filter(
            establecimiento=self.request.user.establecimiento,
            tipo=self.kwargs['tipo']
        ).order_by('-fecha_subida')

def crear_connotacion_sexual(request):
    if request.method == 'POST':
        form = ConnotacionSexualForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # ... resto de tu lógica
    else:
        form = ConnotacionSexualForm()
    
    context = {
        'form': form,
        # ... resto de tu contexto
    }
    return render(request, 'tu_template.html', context)

def matricula_create_view(request):
    if request.method == 'POST':
        form = forms.MatriculaEstablecimientoCreateForm(request.POST, user=request.user)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.establecimiento = request.user.establecimiento
            matricula.año = datetime.now().year
            matricula.esta_activo = True
            matricula.save()
            messages.success(request, 'Matrícula creada exitosamente')
            return redirect('matricula_list')
    else:
        form = forms.MatriculaEstablecimientoCreateForm(user=request.user)
    
    context = {
        'form': form,
        'titulo': 'Crear Matrícula'
    }
    return render(request, 'matricula/form.html', context)