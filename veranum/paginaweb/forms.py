from django import forms
from django.forms import ModelForm
from .models import Promocion


#MARKETING
class PromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = [
            'hotel',
            'tipo_habitacion',
            'codigo_promocion',
            'nombre_promocion',
            'fecha_inicio',
            'fecha_fin',
            'porc_descuento',
            'desc_promocion',
            'imagen_promocion'
        ]
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-select'}),
            'tipo_habitacion': forms.Select(attrs={'class': 'form-select'}),
            'codigo_promocion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_promocion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'porc_descuento': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc_promocion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen_promocion': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'tipo_habitacion': 'Habitación',
            'codigo_promocion': 'Código',
            'nombre_promocion': 'Nombre de la promoción',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de finalización',
            'porc_descuento': 'Porcentaje de descuento',
            'desc_promocion': 'Descripción de la promoción',
            'imagen_promocion': 'Carga la imagen de la promoción'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                self.add_error('fecha_fin', 'La fecha de fin debe ser mayor que la fecha de inicio.')
        return cleaned_data


#GERENCIA
class GerenciaPromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['comentario']
        widgets = {'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),}
