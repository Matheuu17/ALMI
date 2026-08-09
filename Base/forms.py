from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    """
    Formulario de inicio de sesión basado en correo electrónico.
    Autentica al usuario y verifica que la cuenta se encuentre activa.
    """
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'auth-input',
            'placeholder': 'correo@th.club',
            'autofocus': True,
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'auth-input',
            'placeholder': '*************',
            'autocomplete': 'current-password',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Correo o contraseña incorrectos.')
            elif not self.user.is_active:
                raise forms.ValidationError('Esta cuenta está desactivada.')
        return cleaned_data

    def get_user(self):
        return self.user


class CambioPasswordInicialForm(PasswordChangeForm):
    """
    Formulario para el cambio de contraseña.
    Inyecta clases CSS, personaliza etiquetas/placeholders y valida que
    la nueva contraseña sea distinta a la actual.
    """
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].label = 'Contraseña actual'
        self.fields['new_password1'].label = 'Nueva contraseña'
        self.fields['new_password2'].label = 'Confirmar nueva contraseña'

        for campo, field in self.fields.items():
            field.widget.attrs['class'] = 'auth-input'
            field.widget.attrs['placeholder'] = '*************'
            field.widget.attrs['autocomplete'] = (
                'current-password' if campo == 'old_password' else 'new-password'
            )

    def clean_new_password1(self):
        nueva_password = self.cleaned_data.get('new_password1')
        if self.user.check_password(nueva_password):
            raise forms.ValidationError(
                'La nueva contraseña debe ser diferente de la contraseña actual.'
            )
        return nueva_password