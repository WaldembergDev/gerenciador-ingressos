from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.models import Session


# Create your models here.
class MeuUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=120, verbose_name="Nome")
    last_name = models.CharField(max_length=120, verbose_name="Sobrenome")
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(
        verbose_name="Endereço de E-mail", max_length=255, unique=True
    )
    autoriza_notificacoes = models.BooleanField(default=True, verbose_name='Autoriza notificações')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MeuUserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email


class AcessoGeral(models.Model):
    senha = models.CharField(max_length=120)

    def save(self, *args, **kwargs):
        self.senha = make_password(self.senha)
        Session.objects.all().delete()
        super().save(*args, **kwargs)

    def verificar_senha(self, valor):
        return check_password(valor, self.senha)
