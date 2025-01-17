from dataclasses import field, fields
from faulthandler import disable
from pyexpat import model
from statistics import mode
from django import forms
from django.forms import widgets
from . import models
from django.core.validators import FileExtensionValidator



class AlertaForm(forms.ModelForm):
    class Meta:
        model = models.Alerta
        fields = ['cuerpo_mensaje']
        widgets = {
            'cuerpo_mensaje': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Cuerpo del Mensaje...', 'required': True}
            )
        }

class CasoVulneracion(forms.ModelForm):
    class Meta:
        model = models.CasoVulneracion
        fields = ['fecha_creacion']

class DiscriminacionCreateForm(forms.ModelForm):
    class Meta:
        model = models.Discriminacion
        fields = ['tipo_discrim',  'fecha_creacion', 'victima', 'agresor', 'detalle']
        widgets = {
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Relato de lo sucedido', 'required': True}
            ),
            'victima': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'agresor': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'tipo_discrim': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            )
        }

    # def __init__(self, *args, **kwargs):
    #     caso = kwargs.pop('caso', '')
    #     super(DiscriminacionCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['fecha_creaciones']=forms.DateField()

class MedidasDiscriminacion(forms.ModelForm):
    class Meta:
        model = models.MedidasDiscriminacion
        fields = ['condicionalidad', 'devolucion_casa', 'expulsion', 'suspension_clases', 'descripcion_de_medidas']
        widgets = {
            'descripcion_de_medidas': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Detalle de las medidas adoptadas', 'required': True}
            ),
        }


class MaltratoCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = ['fecha_creacion', 'tipo_maltrato', 'victima','detalle', 'funcionario_agresor']
        widgets = {
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Relato de lo sucedido', 'required': True}
            ),
            'victima': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'funcionario_agresor': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'tipo_maltrato': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            )
        }

class MaltratoAlumnoToAlumnoCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = ['fecha_creacion', 'denunciante', 'victima','detalle', 'alumno_agresor','archivo_declaracion_individual']
        widgets = {
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Relato de lo sucedido', 'required': True}
            ),
            'denunciante': forms.TextInput(
                attrs={'class': 'form-control',}
            ),
            'victima': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'alumno_agresor': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'tipo_maltrato': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'archivo_declaracion_individual': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'fecha_creacion': "Fecha de la Denuncia",
            'victima': "Identificacion del Supuesto Afectado",
            'alumno_agresor': "Identificacion del Supuesto Agresor",
            'denunciante':"Identificacion del Denunciante",
        }

class MaltratoFuncionarioToAlumnoCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = ['fecha_creacion', 'denunciante','victima','detalle', 'funcionario_agresor','archivo_declaracion_individual']
        widgets = {
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Relato de lo sucedido', 'required': True}
            ),
            'victima': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'denunciante': forms.TextInput(
                attrs={'class': 'form-control',}
            ),
            'funcionario_agresor': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'archivo_declaracion_individual': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'fecha_creacion': "Fecha de la Denuncia",
            'victima': "Identificacion del Supuesto Afectado",
            'funcionario_agresor': "Identificacion del Supuesto Agresor",
            'denunciante':"Identificacion del Denunciante",
        }

class MaltratoFuncionarioToFuncionarioCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = ['fecha_creacion','denunciante', 'funcionario_victima','detalle', 'funcionario_agresor','archivo_declaracion_individual']
        widgets = {
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Relato de lo sucedido', 'required': True}
            ),
            'denunciante': forms.TextInput(
                attrs={'class': 'form-control',}
            ),
            'funcionario_victima': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'funcionario_agresor': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'tipo_maltrato': forms.Select(
                attrs={'class': 'form-control',}
            ),
            'fecha_creacion': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'archivo_declaracion_individual': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'fecha_creacion': "Fecha de la Denuncia",
            'funcionario_victima': "Identificacion del Supuesto Afectado",
            'funcionario_agresor': "Identificacion del Supuesto Agresor",
            'denunciante':"Identificacion del Denunciante",
        }


class EstadoConnotacionSexualCreateForm(forms.ModelForm):
    class Meta:
        model = models.ConnotacionSexual
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }

class EstadoMaltratoCreateForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }


class EstadoDiscriminacionCreateForm(forms.ModelForm):
    class Meta:
        model = models.Discriminacion
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }


class MedidasMaltratoForm(forms.ModelForm):
    class Meta:
        model = models.MedidasMaltrato
        fields = ['condicionalidad', 'devolucion_casa', 'expulsion', 'suspension_clases', 'descripcion_de_medidas']
        widgets = {
            'descripcion_de_medidas': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Detalle de las medidas adoptadas', 'required': True}
            ),
        }


class AccidenteEscolarActualizarEstadoForm(forms.ModelForm):
    class Meta:
        model = models.AccidenteEscolar
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }


class AccidenteEscolarForm(forms.ModelForm):
    class Meta:
        model = models.AccidenteEscolar
        exclude =('estado','consecuencias_medicas')
        # ['matricula_accidente', 'fecha_ingreso', 'malestar_fisico', 
        #     'nombre_familiar_contacto', 'instruccion_familiar','consecuencias_medicas', 'detalle_relato',
        #     'testigo_uno', 'testigo_dos', 'archivo_declaracion_individual']
        widgets = {
            'accidentado': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'fecha_accidente': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'type': 'date'}),
            'persona_que_solicito_el_seguro': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Indicar Nombre', 'required': True}),
            'lugar_del_accidente': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Si fue dentro la Escuela, especifique donde', 'required': True}),
            'nombre_apoderado': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nombre del Apoderado', 'required': True}),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Detalle del accidente', 'required': True}),
            'medio_contacto_apoderado': forms.Select(
                attrs={'class': 'form-control', 'required': True}),
            'archivo_declaracion_individual': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            )

        }


class DificultadConstitucionConsejoForm(forms.ModelForm):
    class Meta:
        model = models.DificultadConstitucionConsejo
        fields = ['tipo_consejos', 'funcionario_afectado', 'fecha', 'detalle']
        widgets = {
            'tipo_consejos': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'funcionario_afectado': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'detalle': forms.Textarea(
                attrs={'class': 'form-control'}
            ),

        }
    
    def __init__(self, *args, **kwargs):
        super(DificultadConstitucionConsejoForm, self).__init__(*args, **kwargs)
        self.fields['funcionario_afectado'].empty_label = "Seleccione funcionario"




class VulneracionDerechosFuncionariosForm(forms.ModelForm):
    class Meta:
        model = models.VulneracionDerechosFuncionarios
        fields = ['tipo_vulneracion', 'denunciante','funcionario_afectado', 'fecha', 'detalle','archivo_declaracion_individual']
        widgets = {
            'tipo_vulneracion': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'funcionario_afectado': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'detalle': forms.Textarea(
                attrs={'class': 'form-control'}
            ),
            'archivo_declaracion_individual': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
            'denunciante': forms.TextInput(attrs={'class':'form-control'})
        }
        labels = {
            'fecha': "Fecha de la Denuncia",
            'funcionario_afectado': "Identificacion del Supuesto Afectado",
            'tipo_vulneracion': "Tipo Vulneración",
            'denunciante':"Identificacion del Denunciante",
        }


class EstadoVulneracionFuncionariosUpdateForm(forms.ModelForm):
    class Meta:
        model = models.VulneracionDerechosFuncionarios
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }


class EstadoDificultadConsejoUpdateForm(forms.ModelForm):
    class Meta:
        model = models.DificultadConstitucionConsejo
        fields = ['estado']
        widgets = {
            'estado': forms.Select(
                attrs={'class': 'form-control',}
            )
        }

class EstablecimientoUsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Establecimiento
        fields = (
            'nombre',
            'telefono',
            'direccion',
            'logo',
            'reglamento_interno',
            'nombramiento_encargado_convivencia',
            'plan_gestion_convivencia',
        )
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'reglamento_interno': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nombramiento_encargado_convivencia': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
            'plan_gestion_convivencia': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'nombramiento_encargado_convivencia': 'Nombramiento Encargado de Convivencia Escolar',
            'plan_gestion_convivencia': 'Plan de Gestión de Convivencia Escolar',
            'reglamento_interno': 'Reglamento Interno',
        }

class FuncionarioEstablecimientoUpdateForm(forms.ModelForm):
    class Meta:
        model = models.FuncionarioEstablecimiento
        exclude = ['rut','dv','nombre','nombre','apellido_paterno','apellido_materno','establecimiento']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio', 'required': True}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'required': True}),
            'fecha_nacimiento': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'type': 'date'}),
        }
class FuncionarioEstablecimientoCreateForm(forms.ModelForm):
    class Meta:
        model = models.FuncionarioEstablecimiento
        fields = ['rut','dv','nombre','apellido_paterno','apellido_materno','direccion','cargo','fecha_nacimiento']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control',}),
            'dv': forms.TextInput(attrs={'class': 'col col-md-1',}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres', 'required': True,}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno', 'required': True}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio', 'required': True}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo', 'required': True}),
            'fecha_nacimiento': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'type': 'date'}),
        }

class MatriculaEstablecimientoCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.establecimiento:
            self.fields['establecimiento'].initial = user.establecimiento
            self.fields['establecimiento'].widget = forms.HiddenInput()
            self.fields['establecimiento'].queryset = models.Establecimiento.objects.filter(id=user.establecimiento.id)

    class Meta:
        model = models.Matricula
        exclude = ['año','establecimiento','fecha_retiro','esta_activo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control',}),
            'dv': forms.TextInput(attrs={'class': 'col col-md-1 form-control',}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres', 'required': True,}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno', 'required': True}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno', 'required': True}),
            'domicilio_actual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio', 'required': True}),
            'Comuna_residencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna', 'required': True}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'required': False}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'required': False}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'required': False}),
            'fecha_nacimiento': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'type': 'date'}),
            'codigo_etnia': forms.NumberInput(attrs={'class':'col col-md-1 form-control','type':'number'}),
            #matricula
            'nombre_apoderado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Apoderado', 'required': True,}),
            'nivel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion Grado', 'required': True,}),
            'letra': forms.TextInput(attrs={'class': 'col col-md-1 form-control', 'required': True}),
            'fecha_incorporacion': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'type': 'date'}),
            'establecimiento': forms.HiddenInput()
        }
class MatriculaEstablecimientoEditForm(forms.ModelForm):
    class Meta:
        model = models.Matricula
        exclude = ['año','establecimiento','rut','dv','nombres','apellido_paterno','apellido_materno','codigo_etnia','fecha_nacimiento','fecha_incorporacion','fecha_retiro']
        widgets = {
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'nombre_apoderado': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre Apoderado', 'required': True}),
            'domicilio_actual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio', 'required': True}),
            'Comuna_residencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna', 'required': True}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono', 'required': False}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular', 'required': False}),
            #matricula
            'nivel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion Grado', 'required': True,}),
            'letra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Letra Curso', 'required': True})
        }

class ConnotacionSexualForm(forms.ModelForm):
    class Meta:
        model = models.ConnotacionSexual
        fields = [
            'fecha_creacion',
            'denunciante',
            'detalle',
            'victima',
            'archivo_declaracion_individual'
        ]
        widgets = {
            'fecha_creacion': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'denunciante': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 100%;'}
            ),
            'detalle': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'style': 'width: 100%;'}
            ),
            'victima': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'archivo_declaracion_individual': forms.FileInput(
                attrs={'class': 'form-control'}
            ),
        }

class ProtocoloInstitucionalForm(forms.ModelForm):
    class Meta:
        model = models.ProtocoloInstitucional
        fields = ['version', 'archivo']
        widgets = {
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1.0'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }

class MaltratoAdultoAdultoForm(forms.ModelForm):
    class Meta:
        model = models.Maltrato
        fields = [
            'fecha_creacion',
            'denunciante',
            'detalle',
            'funcionario_victima',
            'archivo_declaracion_individual'
        ]
        
    def __init__(self, *args, **kwargs):
        establecimiento = kwargs.pop('establecimiento', None)
        super().__init__(*args, **kwargs)
        if establecimiento:
            self.fields['funcionario_victima'].queryset = models.FuncionarioEstablecimiento.objects.filter(
                establecimiento=establecimiento
            )