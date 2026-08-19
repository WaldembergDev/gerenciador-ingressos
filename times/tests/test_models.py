from django.core.files.uploadedfile import SimpleUploadedFile
from times.models import Time
import pytest

@pytest.mark.django_db
def test_representacao_time():
    conteudo_imagem = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
            b'\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
    
    escudo_fake = SimpleUploadedFile(
        name = 'teste.gif',
        content = conteudo_imagem,
        content_type = 'image/gif'
    )
    time = Time.objects.create(
        nome = 'generico',
        escudo = escudo_fake
    )

    assert str(time) == 'generico'