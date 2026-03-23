from .models import CustomUser


def superuser_check(usuario: CustomUser):
    if usuario.is_authenticated and usuario.is_superuser:
        return True
    return False
