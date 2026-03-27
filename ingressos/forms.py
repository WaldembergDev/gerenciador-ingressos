from django import forms
from .models import HistoricoCompra, Ingresso
from clientes.models import Cliente
from django.utils.timezone import now


class CompraForm(forms.Form):
    quantidade = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        self.ingresso = kwargs.pop("ingresso", None)
        super(CompraForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.ingresso is None:
            raise forms.ValidationError(
                "Erro interno: A informação do ingresso está faltando."
            )
        quantidade = cleaned_data.get("quantidade")
        if quantidade is not None:
            if quantidade > self.ingresso.estoque_disponivel:
                raise forms.ValidationError(
                    f"A quantidade selecionada ({quantidade}) não pode ser superior ao estoque disponível ({self.ingresso.estoque_disponivel})."
                )
        return cleaned_data


class IngressoForm(forms.ModelForm):
    class Meta:
        model = Ingresso
        fields = "__all__"
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "thumbnail": forms.FileInput(attrs={"class": "form-control"}),
            "local": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.TextInput(attrs={"class": "form-control"}),
            "data_horario": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "preco": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "estoque_disponivel": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {"preco": "Preço (R$)"}

    def __init__(self, *args, **kwargs):
        esconder_campo = kwargs.pop("esconder_campo", False)
        super().__init__(*args, **kwargs)

        if esconder_campo:
            del self.fields["status"]


class VendaRapidaForm(forms.ModelForm):
    class Meta:
        model = HistoricoCompra
        fields = ["cliente", "ingresso", "quantidade", "status"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "ingresso": forms.Select(attrs={"class": "form-select"}),
            "quantidade": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cliente"].queryset = Cliente.objects.filter(
            usuario__is_active=True
        ).all()
        self.fields['ingresso'].queryset = Ingresso.objects.filter(
           data_horario__gte=now(), status=Ingresso.StatusIngresso.ATIVO
        )
