from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'apellidos', 'dni', 'rol', 'debe_cambiar_password', 'is_active')
    search_fields = ('email', 'nombre', 'apellidos', 'dni')
    list_filter = ('rol', 'debe_cambiar_password', 'is_active')
    ordering = ('email',)

    def save_model(self, request, obj, form, change):
        if not change:  # Creación de nuevo usuario
            # Asigna el DNI como contraseña si no fue encriptada previa
            if obj.dni and (not obj.password or not obj.password.startswith('pbkdf2_sha256$')):
                obj.set_password(obj.dni)

            # Asegura la bandera activa para primer inicio
            obj.debe_cambiar_password = True

        super().save_model(request, obj, form, change)