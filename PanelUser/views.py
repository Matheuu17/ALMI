from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import logout
from .forms import ContactoForm, ActividadForm
from .models import Contacto, Actividad, ArchivoContacto
import json
# Listas de opciones de catálogo
CARRERAS_LIST = [
    '--------------',
    'Administración',
    'Administración Hotelera',
    'Administración y Emprendimiento',
    'Administración y Finanzas Corporativas',
    'Administración y Marketing',
    'Administración y Negocios Internacionales',
    'Arquitectura, Urbanismo y Territorio',
    'Ciencias de la Actividad Física y del Deporte',
    'Comunicaciones',
    'Contabilidad',
    'Derecho',
    'Arte y Diseño Empresarial',
    'Educación Inicial',
    'Educación Secundaria',
    'Gastronomía y Gestión Culinaria',
    'Ingeniería Agroindustrial',
    'Ingeniería Ambiental',
    'Ingeniería Civil',
    'Ingeniería de Sistemas e Información',
    'Ingeniería de Software',
    'Ingeniería Empresarial',
    'Ingeniería Industrial',
    'Ingeniería Mecatrónica',
    'Marketing',
    'Medicina Humana',
    'Nutrición y Dietética',
    'Psicología',
    'Relaciones Internacionales',
]

RUBROS_LIST = [
    '--------------',
    'Tecnología / Software',
    'Banca y Finanzas',
    'Educación',
    'Consumo Masivo',
    'Salud',
    'Consultoría',
    'Retail',
]

AREAS_LIST = [
    '--------------',
    'Investigación e Insights',
    'Tecnología de la Información',
    'Recursos Humanos',
    'Arte Digital',
    'Media Audiovisual',
]

TIPOS_ACTIVIDAD_LIST = [
    '--------------',
    'Llamada',
    'Reunión',
    'Convocatoria',
    'Correo',
    'Presentación / Pitch',
    'Entrevista',
    'Seguimiento',
    'Otro',
]

# ================= VIEWS PRINCIPALES =================

@login_required
def home_view(request):
    """Muestra el resumen general e métricas en el Home del usuario."""
    total_contactos = Contacto.objects.filter(activo=True).count()
    total_empresas = Contacto.objects.filter(tipo_contacto='empresa', activo=True).count()
    total_miembros = Contacto.objects.filter(tipo_contacto='miembro', activo=True).count()

    actividades_activas = Actividad.objects.filter(estado='pendiente').count()
    proximas_actividades = Actividad.objects.filter(estado='pendiente').order_by('fecha_limite')[:5]

    context = {
        'total_contactos': total_contactos,
        'total_empresas': total_empresas,
        'total_miembros': total_miembros,
        'actividades_activas': actividades_activas,
        'proximas_actividades': proximas_actividades,
    }
    return render(request, 'home.html', context)


# ================= CONTACTOS =================

@login_required
def contactos_view(request):
    """Despliega la grilla de contactos activos."""
    contactos = Contacto.objects.filter(activo=True).order_by('-creado_en')
    context = {
        'contactos': contactos,
        'carreras': CARRERAS_LIST,
        'rubros': RUBROS_LIST,
        'areas': AREAS_LIST,
    }
    return render(request, 'contactos.html', context)


@login_required
def form_contactos_view(request):
    """Crea un nuevo contacto y guarda múltiples archivos si se adjuntan."""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.creado_por = request.user
            contacto.save()

            # Guardar múltiples archivos
            for f in request.FILES.getlist('archivos'):
                ArchivoContacto.objects.create(contacto=contacto, archivo=f)

            messages.success(request, 'Contacto y archivos registrados exitosamente.')
            return redirect('PanelUser:contactos')
    else:
        form = ContactoForm()

    return render(request, 'form_contactos.html', {'form': form})


@login_required
@require_POST
def editar_contacto(request, contacto_id):
    """Actualiza los datos del contacto, borra archivos marcados y acumula nuevos."""
    contacto = get_object_or_404(Contacto, id=contacto_id)

    contacto.nombre = request.POST.get('nombre')
    contacto.tipo_contacto = request.POST.get('tipo_contacto')
    contacto.carrera_rubro = request.POST.get('carrera_rubro')
    contacto.area = request.POST.get('area')
    contacto.telefono = request.POST.get('telefono')
    contacto.email = request.POST.get('email')
    contacto.save()

    # Elimina archivos
    ids_eliminar = request.POST.get('archivos_a_eliminar', '')
    if ids_eliminar:
        for arch_id in ids_eliminar.split(','):
            arch_id = arch_id.strip()
            if arch_id.isdigit():
                archivo_obj = ArchivoContacto.objects.filter(id=arch_id, contacto=contacto).first()
                if archivo_obj:
                    archivo_obj.archivo.delete(save=False) # Borra archivo del disco
                    archivo_obj.delete() # Borra de la BD

    # Acumula los archivos, no los sobrepone
    for f in request.FILES.getlist('archivos'):
        ArchivoContacto.objects.create(contacto=contacto, archivo=f)

    messages.success(request, 'Contacto actualizado correctamente.')
    return redirect('PanelUser:contactos')


@login_required
@require_POST
def desactivar_contacto(request, contacto_id):
    """Aplica Soft Delete al contacto marcando su estado como inactivo."""
    contacto = get_object_or_404(Contacto, id=contacto_id)
    contacto.activo = False
    contacto.save()
    messages.success(request, 'El contacto ha sido desactivado.')
    return redirect('PanelUser:contactos')


# ================= ACTIVIDADES (TABLERO KANBAN) =================

@login_required
def actividades_view(request):
    """Organiza las actividades por columnas Kanban (Pendiente, En Proceso, Completada)."""
    actividades_pendientes = Actividad.objects.filter(estado='pendiente').order_by('fecha_limite')
    actividades_en_proceso = Actividad.objects.filter(estado='en_proceso').order_by('fecha_limite')
    actividades_completadas = Actividad.objects.filter(estado='completada').order_by('-id')[:10]

    contactos = Contacto.objects.filter(activo=True).order_by('nombre')
    contactos_data = [
        {'id': c.id, 'nombre': c.nombre or '', 'email': c.email or ''}
        for c in contactos
    ]

    columnas = [
        {'estado': 'pendiente', 'titulo': 'Pendientes', 'actividades': actividades_pendientes},
        {'estado': 'en_proceso', 'titulo': 'En Proceso', 'actividades': actividades_en_proceso},
        {'estado': 'completada', 'titulo': 'Completadas', 'actividades': actividades_completadas},
    ]

    context = {
        'columnas': columnas,
        'contactos': contactos,
        'contactos_json': json.dumps(contactos_data),
        'tipos_actividad': TIPOS_ACTIVIDAD_LIST,
    }
    return render(request, 'actividades.html', context)


@login_required
def form_actividades_view(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.creado_por = request.user
            actividad.save()
            form.save_m2m()  # Guarda los contactos asignados (ManyToManyField)

            messages.success(request, 'Actividad programada correctamente.')
            return redirect('PanelUser:actividades')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ActividadForm()

        # Obtener contactos y serializar en JSON para el buscador JS
        contactos_qs = Contacto.objects.filter(activo=True).order_by('nombre')
        contactos_data = [
            {
                'id': c.id,
                'nombre': c.nombre or '',
                'email': c.email or ''
            }
            for c in contactos_qs
        ]

        context = {
            'form': form,
            'contactos_json': json.dumps(contactos_data),
            'tipos_actividad': TIPOS_ACTIVIDAD_LIST,
        }
        return render(request, 'form_actividades.html', context)

@login_required
@require_POST
def completar_actividad(request, actividad_id):
    """Avanza la actividad de manera progresiva: Pendiente -> En Proceso -> Completada."""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    if actividad.estado == 'pendiente':
        actividad.estado = 'en_proceso'
        messages.success(request, 'Actividad movida a En Proceso.')
    elif actividad.estado == 'en_proceso':
        actividad.estado = 'completada'
        messages.success(request, 'Actividad marcada como completada.')

    actividad.save()
    return redirect('PanelUser:actividades')


@login_required
@require_POST
def editar_actividad(request, actividad_id):
    """Edita los campos de una actividad existente desde el modal de edición."""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    actividad.resumen = request.POST.get('resumen')
    actividad.tipo_actividad = request.POST.get('tipo_actividad')
    actividad.estado = request.POST.get('estado')
    actividad.fecha_limite = request.POST.get('fecha_limite')
    actividad.notas = request.POST.get('notas')
    actividad.save()

    asignados_ids = request.POST.getlist('asignado_a')
    actividad.asignado_a.set(asignados_ids)

    messages.success(request, 'Actividad actualizada correctamente.')
    return redirect('PanelUser:actividades')


@login_required
@require_POST
def eliminar_actividad(request, actividad_id):
    """Elimina permanentemente una tarjeta de actividad."""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    actividad.delete()
    messages.success(request, 'Actividad eliminada correctamente.')
    return redirect('PanelUser:actividades')


# ================= AUTENTICACIÓN =================

def logout_view(request):
    """Cierra la sesión del usuario y redirige al login."""
    logout(request)
    return redirect('Base:login')