# store/forms.py
from django import forms
from .models import CitaVeterinaria
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CitaVeterinariaForm(forms.ModelForm):
    class Meta:
        model = CitaVeterinaria
        fields = ['fecha_hora', 'motivo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'fecha_hora': 'Fecha y Hora de la Cita',
            'motivo': 'Motivo de la Cita',
        }
        error_messages = {
            'fecha_hora': {
                'required': 'Por favor, selecciona la fecha y hora de la cita.',
                'invalid': 'Por favor, ingresa una fecha y hora válidas.'
            },
            'motivo': {
                'required': 'Por favor, ingresa el motivo de la cita.'
            }
        }

    def clean_fecha_hora(self):
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora:
            # Asegurarse de que la fecha no sea anterior a la actual
            if fecha_hora < datetime.datetime.now(tz=fecha_hora.tzinfo):
                raise ValidationError('La fecha y hora de la cita no puede ser en el pasado.')
        return fecha_hora

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    first_name = forms.CharField(max_length=150, required=True, label="Nombre")
    telefono = forms.CharField(max_length=20, required=False, label="Teléfono")
    direccion = forms.CharField(widget=forms.Textarea, required=False, label="Dirección")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'telefono', 'direccion', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")