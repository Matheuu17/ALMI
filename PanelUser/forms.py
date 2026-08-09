from django import forms
from .models import Actividad, Contacto


class ContactoForm(forms.ModelForm):
    """
    Formulario para la creación de nuevos contactos (Miembros o Empresas).
    Soporta la carga opcional de archivos adjuntos (CVs, propuestas, contratos).
    """
    class Meta:
        model = Contacto
        fields = ['tipo_contacto', 'nombre', 'carrera_rubro', 'area', 'telefono', 'email', 'archivo']
        labels = {
            'tipo_contacto': 'Tipo de Contacto',
            'nombre': 'Nombre / Razon Social',
            'carrera_rubro': 'Carrera o Rubro',
            'area': 'Área de Interés',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'archivo': 'Archivo Adjunto (CV, PDF, Contrato)',
        }
        widgets = {
            'tipo_contacto': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Elena Kovar', 'required': 'required'}),
            'carrera_rubro': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+51 999 999 999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com', 'required': 'required'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ActividadForm(forms.ModelForm):
    """
    Formulario para programar nuevas actividades en el tablero Kanban.
    Permite asignar múltiples contactos activos de manera simultánea.
    """
    class Meta:
        model = Actividad
        fields = ['tipo_actividad', 'fecha_limite', 'resumen', 'asignado_a', 'notas']
        labels = {
            'tipo_actividad': 'Tipo de Actividad',
            'fecha_limite': 'Fecha Límite',
            'resumen': 'Resumen / Asunto',
            'asignado_a': 'Asignado a (Selección Múltiple)',
            'notas': 'Notas Adicionales',
        }
        widgets = {
            'tipo_actividad': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Coordinar entrevista con Nova Tech', 'required': 'required'}),
            'asignado_a': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'height: 100px;'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detalles, contexto o próximos pasos...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar contactos que no hayan sido desactivados (Soft Delete)
        self.fields['asignado_a'].queryset = Contacto.objects.filter(activo=True).order_by('nombre')
        # Formatear la opción para mostrar el tipo (Empresa/Miembro) al lado del nombre
        self.fields['asignado_a'].label_from_instance = lambda obj: (
            f"{obj.nombre} ({'Empresa' if obj.tipo_contacto == 'empresa' else 'Miembro'})"
        )
        self.fields['asignado_a'].required = False