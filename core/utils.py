from django.contrib.auth.models import AbstractBaseUser, AnonymousUser


def superuser_check(usuario: AbstractBaseUser | AnonymousUser) -> bool:
    return usuario.is_authenticated and usuario.is_superuser # type: ignore
