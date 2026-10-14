import pytest

from red_social.publicacion import Tweet
from red_social.red import RedSocial
from red_social.usuario import Usuario


@pytest.fixture
def ana():
    # Creamos un usuario Ana nuevo para usarlo en los tests.
    return Usuario("Ana", "@ana")


@pytest.fixture
def luis():
    # Creamos un usuario Luis nuevo para usarlo en los tests.
    return Usuario("Luis", "@luis")

@pytest.fixture
def tweet(ana):
    # Creamos un Tweet de Ana para usarlo en los tests.
    return Tweet(ana, "Hola a todos #python #pytest")

@pytest.fixture
def red():
    red = RedSocial()

    # Creamos una RedSocial preparada con varios usuarios y un seguimiento.
    red.registrar("Ana", "@ana")
    red.registrar("Luis", "@luis")
    red.registrar("Marta", "@marta")

    red["@luis"].seguir(red["@ana"])

    return red