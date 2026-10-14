import pytest

from red_social.publicacion import Retweet, Tweet
from red_social.red import RedSocial


def test_timeline_solo_tiene_publicaciones_de_los_seguidos(red):
    # Recuperamos de la red los objetos Usuario que ya creó la fixture.
    ana = red["@ana"]
    luis = red["@luis"]

    # Publicamos dos tweets de Ana.
    primer_tweet = red.publicar(Tweet(ana, "Primer tweet"))
    segundo_tweet = red.publicar(Tweet(ana, "Segundo tweet"))

    # Publicamos también un tweet de Luis (No debería aparecer en su propio timeline).
    red.publicar(Tweet(luis, "Tweet de Luis"))

    # Obtenemos el timeline de Luis.
    timeline_luis = red.timeline(luis)

    # Comprobamos que Luis vea solo las publicaciones de Ana, con la más reciente primero.
    assert timeline_luis == [segundo_tweet, primer_tweet]

    # Comprobamos que el timeline de Ana está vacío.
    assert red.timeline(ana) == []


def test_desde_json_construye_usuarios_y_seguimientos(mocker):
    # Creamos un JSON con dos usuarios y una relación de seguimiento entre ellos.
    contenido = """
    {
        "usuarios": [
            {"nombre": "Ana", "alias": "@ana"},
            {"nombre": "Luis", "alias": "@luis"}
        ],
        "seguimientos": [
            ["@luis", "@ana"]
        ]
    }
    """

    # Sustituimos open() por un mock para simular la lectura del JSON.
    abrir_falso = mocker.patch("builtins.open", mocker.mock_open(read_data=contenido))

    # Ejecutamos el método que queremos probar.
    red = RedSocial.desde_json("ruta/falsa.json")

    # Comprobamos que open() se llamó una sola vez con la ruta recibida y la codificación correcta.
    abrir_falso.assert_called_once_with(
        "ruta/falsa.json",
        encoding="utf-8",
    )

    # Comprobamos que se han creado los dos usuarios del JSON.
    assert len(red) == 2

    # Comprobamos que Luis sigue a Ana.
    assert red["@luis"].sigue_a(red["@ana"]) is True

    # Comprobamos también que el seguimiento no se ha aplicado al revés.
    assert red["@ana"].sigue_a(red["@luis"]) is False


# Test añadidos para la corrección del ejercicio
def test_contains_comprueba_si_alias_existe(red):
    # Comprobamos el funcionamiento del Dunder __contains__ con "in".
    assert "@ana" in red
    assert "@pablo" not in red


def test_get_devuelve_usuario_por_alias(red):
    # Comprobamos que el Dunder __getitem__ nos devuelve un suario de la red utilizando el alias
    usuario = red["@ana"]

    assert usuario.nombre == "Ana"
    assert usuario.alias == "@ana"


def test_usuario_ya_existe_en_red(red):

    with pytest.raises(ValueError):  # Comprobamos que se lanza la excepción que esperamos
        red.anadir(red["@luis"])


def test_usuario_no_existe_en_red(red):

    with pytest.raises(KeyError):  # Comprobamos que se lanza la excepción que esperamos
        red["@francisco"]


def test_tendencias_devuelve_hashtags_mas_usados(red):
    # Obtenemos los usuarios de la red
    ana = red["@ana"]
    luis = red["@luis"]
    marta = red["@marta"]

    # Generamos publicaciones con distintos hashtags.
    tweet_ana = red.publicar(Tweet(ana, "Hola #python #pytest"))
    red.publicar(Tweet(luis, "Aprendiendo #python"))

    # El retweet comparte el texto y los hashtags del tweet original.
    red.publicar(Retweet(marta, tweet_ana))

    
    assert red.tendencias(2) == [
        ("#python", 3),
        ("#pytest", 2),
    ]


def test_iter_devuelve_usuarios_ordenados_por_alias(red):
    
    # Iteramos sobre la red:
    usuarios = list(red)
    
    alias_usuarios = [usuario.alias for usuario in usuarios]

    assert alias_usuarios == ["@ana", "@luis", "@marta"]