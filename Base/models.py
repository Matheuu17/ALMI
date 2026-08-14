from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario donde el email
    es el identificador único para el inicio de sesión.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)

        # Si no es superusuario, debe cambiar contraseña por defecto
        extra_fields.setdefault(
            'debe_cambiar_password',
            not extra_fields.get('is_superuser', False),
        )
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields['rol'] = ''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'superadmin')
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Area(models.Model):
    """
    Modelo para catalogar las áreas organizacionales de la entidad.
    """
    OPCIONES_AREA = [
        ('investigacion_insights', 'Investigación e Insights'),
        ('tecnologia_informacion', 'Tecnología de la Información'),
        ('recursos_humanos', 'Recursos Humanos'),
        ('arte_digital', 'Arte Digital'),
        ('media_audiovisual', 'Media Audiovisual'),
    ]

    nombre = models.CharField(max_length=100, choices=OPCIONES_AREA, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.get_nombre_display()

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['nombre']


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de Usuario personalizado autenticado mediante correo electrónico.
    """
    ROL = [
        ('superadmin', 'Super Administrador'),
        ('admin_crm', 'Administrador de CRM'),
        ('panel_user', 'Usuario del Panel'),
    ]

    ROLES_PANEL = [
        ('admin_crm', 'Administrador de CRM'),
        ('panel_user', 'Usuario del Panel'),
    ]

    # Información Personal y de Contacto
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9, blank=True)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField(unique=True)

    # Cargo y Rol en el Sistema
    cargo = models.CharField(
        max_length=100,
        blank=True,
        help_text='Etiqueta/Badge visible (Ej: Directora, Coordinador, Ejecutivo)'
    )
    rol = models.CharField(max_length=25, choices=ROL, blank=False, null=False )

    def clean(self):
        super().clean()
        # Si NO es superusuario y no seleccionó rol, lanzar error explícito
        if not self.is_superuser and not self.rol:
            raise ValidationError({'rol': 'El rol en el sistema es obligatorio.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # Fuerza a que ejecute las reglas de clean() antes de insertar en BD
        super().save(*args, **kwargs)

        area = models.CharField(max_length=50, choices=Area.OPCIONES_AREA, blank=True, null=True, default='')

    # Flags de Estado y Permisos
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    debe_cambiar_password = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'dni']

    objects = UsuarioManager()

    @property
    def nombre_completo(self):
        """Retorna el nombre y apellido concatenados."""
        return f'{self.nombre} {self.apellidos}'.strip()

    @property
    def es_admin_crm(self):
        """Acceso exclusivo a/panel-admin SI Y SOLO SI es tiene rol de "admin_crm"."""
        return not self.is_superuser and self.rol == 'admin_crm'

    @property
    def es_panel_user(self):
        """Otorga permisos de acceso al /panel_user."""
        return self.rol == 'panel_user'

    def badge_cargo(self):
        """Devuelve la etiqueta representativa para la interfaz."""
        if self.is_superuser:
            return 'Super Admin'
        if self.cargo:
            return self.cargo
        return self.get_rol_display() if self.rol else 'Sin Rol'

    def clean(self):
        """Validaciones de reglas de negocio antes de guardar."""
        # Si es superusuario, le forzamos la asignación del rol 'superadmin'
        if self.is_superuser:
            self.rol = 'superadmin'
        # Si NO es superusuario y no seleccionó ningún rol, exige uno
        elif not self.rol:
            raise ValidationError({'rol': 'El rol en el sistema es obligatorio.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        rol_display = 'Administrador de sistema' if self.is_superuser else (
            self.get_rol_display() if self.rol else 'No asignado'
        )
        return f'{self.nombre_completo} ({rol_display})'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'