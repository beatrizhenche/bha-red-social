from red_social.publicacion import Tweet
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
    abrir_falso = mocker.patch( "builtins.open", mocker.mock_open(read_data=contenido))

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