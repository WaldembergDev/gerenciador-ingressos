from django import forms
from .models import Time
# from django_svg_image_form_field import SvgAndImageFormField

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ["nome", "escudo"]
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'escudo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }