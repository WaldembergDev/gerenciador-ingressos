from django.db import models

# Create your models here.
class Time(models.Model):
    nome = models.CharField(max_length=50, unique=True, verbose_name='Nome')
    escudo = models.ImageField(verbose_name='Escudo', upload_to='escudos/')

    def __str__(self):
        return self.nome