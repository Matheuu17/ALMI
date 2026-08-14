from django import forms
from Base.models import Usuario

# Agregamos la opción por defecto vacía
CHOICES_ROL = [('', '-- Seleccione un Rol --')] + Usuario.ROLES_PANEL

class CrearUsuarioForm(forms.ModelForm):
    """
    Formulario para el registro de nuevos usuarios en el panel administrativo.
    Utiliza el DNI como contraseña temporal inicial y fuerza el cambio de clave en el primer inicio.
    """
    rol = forms.ChoiceField(
        choices=CHOICES_ROL,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='ROL EN EL SISTEMA',
        error_messages={
            'required': 'Debe seleccionar un rol obligatoriamente.',
            'invalid_choice': 'Seleccione una opción de rol válida.'
        }
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'dni', 'email', 'telefono', 'cargo', 'rol']
        labels = {
            'nombre': 'NOMBRE',
            'apellidos': 'APELLIDOS',
            'dni': 'DNI',
            'email': 'EMAIL',
            'telefono': 'TELÉFONO',
            'cargo': 'CARGO',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pérez'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8 dígitos', 'maxlength': '8'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@th.club'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9 dígitos', 'maxlength': '9'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Directora de RH'}),
        }

    def save(self, commit=True):
        dni = self.cleaned_data['dni']

        # Se crea el usuario en una sola consulta de base de datos pasando todas las propiedades iniciales
        user = Usuario.objects.create_user(
            email=self.cleaned_data['email'],
            password=dni,  # DNI como contraseña inicial temporal
            nombre=self.cleaned_data['nombre'],
            apellidos=self.cleaned_data['apellidos'],
            dni=dni,
            telefono=self.cleaned_data.get('telefono', ''),
            cargo=self.cleaned_data.get('cargo', ''),
            rol=self.cleaned_data['rol'],
            debe_cambiar_password=True  # Forzamos el flag en la misma creación
        )

        return user


class EditarUsuarioForm(forms.ModelForm):
    """
    Formulario para la edición de usuarios existentes desde el panel administrativo.
    Permite modificar datos personales, cargo, rol y activar/desactivar la cuenta.
    """

    rol = forms.ChoiceField(
        choices=CHOICES_ROL,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='ROL EN EL SISTEMA',
        error_messages={
            'required': 'Debe seleccionar un rol obligatoriamente.',
            'invalid_choice': 'Seleccione una opción de rol válida.'
        }
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'dni', 'email', 'telefono', 'cargo', 'rol', 'is_active']
        labels = {
            'nombre': 'NOMBRE',
            'apellidos': 'APELLIDOS',
            'dni': 'DNI',
            'email': 'EMAIL',
            'telefono': 'TELÉFONO',
            'cargo': 'CARGO',
            'rol': 'ROL EN SISTEMA',
            'is_active': 'USUARIO ACTIVO',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '9'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }