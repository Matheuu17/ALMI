import os
from django.db import models
from Base.models import Usuario


class Contacto(models.Model):
    """
    Modelo para registrar contactos de tipo Miembro o Empresa.
    Soporta múltiples documentos adjuntos y desactivación mediante Soft Delete.
    """
    TIPO_CONTACTO = [
        ('miembro', 'Miembro'),
        ('empresa', 'Empresa'),
    ]

    # Auditoría
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='contactos'
    )

    # Datos Principales
    tipo_contacto = models.CharField(max_length=20, choices=TIPO_CONTACTO, default='miembro')
    nombre = models.CharField(max_length=150)
    carrera_rubro = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    creado_en = models.DateTimeField(auto_now_add=True)

    # Soft Delete
    activo = models.BooleanField(default=True)

    # Mantenemos el campo por retrocompatibilidad
    archivo = models.FileField(upload_to='contactos_archivos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_contacto_display()})"

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-creado_en']


class ArchivoContacto(models.Model):
    """Modelo para permitir múltiples archivos acumulados por contacto."""
    contacto = models.ForeignKey(Contacto, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='contactos_archivos/')
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def nombre_archivo(self):
        return os.path.basename(self.archivo.name) if self.archivo else ""

    def __str__(self):
        return f"{self.nombre_archivo} - {self.contacto.nombre}"

    class Meta:
        verbose_name = 'Archivo de Contacto'
        verbose_name_plural = 'Archivos de Contactos'
        ordering = ['creado_en']


class Actividad(models.Model):
    TIPO_ACTIVIDAD = [
        ('Entrevista', 'Entrevista'),
        ('Llamada', 'Llamada'),
        ('Reunión', 'Reunión'),
        ('Correo', 'Correo'),
        ('Seguimiento', 'Seguimiento'),
        ('Convocatoria', 'Convocatoria'),
        ('Presentación / Pitch', 'Presentación / Pitch'),
        ('Otro', 'Otro'),
    ]

    ESTADO_ACTIVIDAD = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    ]

    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='actividades_creadas'
    )

    asignado_a = models.ManyToManyField(
        Contacto,
        blank=True,
        related_name='actividades_asignadas'
    )

    tipo_actividad = models.CharField(max_length=50, choices=TIPO_ACTIVIDAD, default='Llamada')
    fecha_limite = models.DateField()
    resumen = models.CharField(max_length=200)
    notas = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_ACTIVIDAD, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resumen} - {self.fecha_limite}"

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['fecha_limite']