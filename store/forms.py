# store/forms.py
from django import forms
from .models import CitaVeterinaria, Cliente

class CitaVeterinariaForm(forms.ModelForm):
    cliente_nombre = forms.CharField(max_length=255, label="Nombre del Cliente")
    cliente_telefono = forms.CharField(max_length=20, required=False, label="Teléfono del Cliente")
    cliente_email = forms.EmailField(required=False, label="Email del Cliente")
    cliente_direccion = forms.CharField(widget=forms.Textarea, required=False, label="Dirección del Cliente")

    class Meta:
        model = CitaVeterinaria
        fields = ['fecha_hora', 'motivo']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        cliente, created = Cliente.objects.get_or_create(
            nombre=self.cleaned_data['cliente_nombre'],
            defaults={
                'telefono': self.cleaned_data['cliente_telefono'],
                'email': self.cleaned_data['cliente_email'],
                'direccion': self.cleaned_data['cliente_direccion'],
            }
        )

        cita = super().save(commit=False)
        cita.cliente = cliente
        if commit:
            cita.save()
        return cita