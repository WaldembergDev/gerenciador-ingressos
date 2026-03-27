from .models import Cliente
from django import forms


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ["usuario"]
        widgets = {
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "rg": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "sexo": forms.Select(attrs={"class": "form-select"}),
        }
