from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import AcessoGeral, CustomUser
from django.forms import ValidationError


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Senha", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class CustomUserForm(forms.ModelForm):
    password2 = forms.CharField(
        label="Confirmar Senha",
        max_length=100,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise ValidationError("As senhas digitadas não são iguais!")
        return cleaned_data


class AcessoGeralForm(forms.ModelForm):
    class Meta:
        model = AcessoGeral
        fields = "__all__"
        widgets = {"senha": forms.PasswordInput(attrs={"class": "form-control"})}


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "is_active", 'autoriza_notificacoes']
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_active": forms.Select(
                attrs={"class": "form-select"},
                choices=[(True, "Ativo"), (False, "Inativo")],
            ),
            "autoriza_notificacoes": forms.Select(
                attrs={'class': 'form-select'},
                choices=[(True, 'Sim'), (False, 'Não')]
            )
        }
