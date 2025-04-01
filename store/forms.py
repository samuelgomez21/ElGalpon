# store/forms.py
from django import forms
from .models import CitaVeterinaria, Cliente
from django.core.exceptions import ValidationError
import datetime

class CitaVeterinariaForm(forms.ModelForm):
    cliente_nombre = forms.CharField(
        max_length=255,
        label="Nombre del Cliente",
        error_messages={
            'required': 'Por favor, ingresa el nombre del cliente.',
            'max_length': 'El nombre del cliente no puede exceder los 255 caracteres.'
        }
    )
    cliente_telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono del Cliente",
        error_messages={
            'max_length': 'El teléfono no puede exceder los 20 caracteres.'
        }
    )
    cliente_email = forms.EmailField(
        required=False,
        label="Correo Electrónico del Cliente",
        error_messages={
            'invalid': 'Por favor, ingresa un correo electrónico válido.'
        }
    )
    cliente_direccion = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label="Dirección del Cliente",
        error_messages={
            'max_length': 'La dirección no puede exceder los 255 caracteres.'
        }
    )

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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('cliente_email')
        nombre = cleaned_data.get('cliente_nombre')

        if email:
            # Verificar si ya existe un cliente con este email
            existing_client = Cliente.objects.filter(email=email).exclude(nombre=nombre).first()
            if existing_client:
                raise ValidationError(
                    f"Ya existe un cliente con el correo {email}. Por favor, usa un correo diferente o verifica el nombre."
                )
        return cleaned_data

    def save(self, commit=True):
        # Buscar cliente por nombre y email (si se proporciona)
        email = self.cleaned_data.get('cliente_email')
        cliente = None
        if email:
            cliente = Cliente.objects.filter(nombre=self.cleaned_data['cliente_nombre'], email=email).first()
        if not cliente:
            cliente = Cliente.objects.filter(nombre=self.cleaned_data['cliente_nombre'], email__isnull=True).first()
        if not cliente:
            cliente = Cliente.objects.create(
                nombre=self.cleaned_data['cliente_nombre'],
                telefono=self.cleaned_data['cliente_telefono'],
                email=email if email else None,
                direccion=self.cleaned_data['cliente_direccion'],
            )

        cita = super().save(commit=False)
        cita.cliente = cliente
        if commit:
            cita.save()
        return cita