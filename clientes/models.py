from django.db import models
import uuid
from core.models import CustomUser


# Create your models here.
class Cliente(models.Model):
    class SexoEnum(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMININO = "F", "Feminino"
        OUTRO = "O", "Outro"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    rg = models.CharField(max_length=13, verbose_name="RG", null=True, blank=True)
    cpf = models.CharField(
        max_length=14, unique=True, verbose_name="CPF", null=True, blank=True
    )
    sexo = models.CharField(
        max_length=2, choices=SexoEnum.choices, null=True, blank=True
    )
    usuario = models.OneToOneField(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.usuario.first_name

    @property
    def obter_status(self):
        return "Ativo" if self.usuario.is_active else "Inativo"


class Endereco(models.Model):
    class UfEnum(models.TextChoices):
        ACRE = "AC", "Acre"
        ALAGOAS = "AL", "Alagoas"
        AMAPA = "AP", "Amapá"
        AMAZONAS = "AM", "Amazonas"
        BAHIA = "BA", "Bahia"
        CEARA = "CE", "Ceará"
        ESPIRITO_SANTO = "ES", "Espírito Santo"
        GOIAS = "GO", "Goiás"
        DISTRITO_FEDERAL = "DF", "Distrito Federal"
        MARANHAO = "MA", "Maranhão"
        MATO_GROSSO = "MT", "Mato Grosso"
        MATO_GROSSO_DO_SUL = "MS", "Mato Grosso do Sul"
        MINAS_GERAIS = "MG", "Minas Gerais"
        PARA = "PA", "Pará"
        PARAIBA = "PB", "Paraíba"
        PARANA = "PR", "Paraná"
        PERNAMBUCO = "PE", "Pernambuco"
        PIAUI = "PI", "Piauí"
        RIO_DE_JANEIRO = "RJ", "Rio de Janeiro"
        RIO_GRANDE_DO_NORTE = "RN", "Rio Grande do Norte"
        RIO_GRANDE_DO_SUL = "RS", "Rio Grande do Sul"
        RONDONIA = "RO", "Rondônia"
        SANTA_CATARINA = "SC", "Santa Catarina"
        SAO_PAULO = "SP", "São Paulo"
        SERGIPE = "SE", "Sergipe"
        TOCANTINS = "TO", "Tocantins"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=120)
    numero = models.CharField(max_length=15)
    complemento = models.CharField(max_length=120, null=True, blank=True)
    bairro = models.CharField(max_length=25)
    cidade = models.CharField(max_length=25)
    estado = models.CharField(max_length=25)
    uf = models.CharField(max_length=2, choices=UfEnum.choices)
    cliente = models.OneToOneField(Cliente, on_delete=models.PROTECT)

    def __str__(self):
        return self.logradouro
