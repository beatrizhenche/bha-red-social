import pytest

from red_social.publicacion import Publicacion, Respuesta, Retweet, Tweet


@pytest.mark.parametrize(
    "texto",
    [
        "",          # Texto vacío.
        "   ",       # Texto formado solo por espacios.
        "a" * 281,   # Texto que supera el límite de 280 caracteres.
    ],
)
def test_texto_invalido_lanza_error(ana, texto):

    # Ejecutamos el test una vez por cada valor definido en la lista de parametrize.
    
    with pytest.raises(ValueError): # En los tres casos esperamos que crear un Tweet falle.
        Tweet(ana, texto)




@pytest.mark.parametrize(
    "texto, esperado",
    [
        # Un texto sin hashtags debe devolver una lista vacía.
        ("Hola a todos", []),

        # Los hashtags deben devolverse en minúsculas.
        (
            "Hola #Python #PYTEST",
            ["#python", "#pytest"],
        ),

        # Los hashtags repetidos solo deben aparecer una vez.
        (
            "#python y otra vez #python",
            ["#python"],
        ),

        # Eliminamos la puntuación final de cada hashtag.
        (
            "Me gusta #python, y mucho #pytest!",
            ["#python", "#pytest"],
        ),
    ],
)
def test_extraer_hashtags(texto, esperado):
    # Llamamos directamente al método estático de Publicacion.
    resultado = Publicacion.extraer_hashtags(texto)

    # Comprobamos que la lista obtenida coincide con la esperada para cada caso del parametrize.
    assert resultado == esperado


def test_retweet_comparte_el_texto_del_original(tweet, luis):
    # Creamos un retweet cuyo autor es Luis y cuya publicación original es el tweet de Ana.
    retweet = Retweet(luis, tweet)

    # Comprobamos que guarda exactamente el mismo objeto Tweet con is.
    assert retweet.original is tweet

    # Comprobamos que el retweet tiene el mismo texto que la publicación original.
    assert retweet.texto == tweet.texto

    # Comprobamos que también tienen los mismos hashtags.
    assert retweet.hashtags == tweet.hashtags

    # Comprobamos que el autor del retweet es Luis.
    assert retweet.autor is luis


#Test incluidos para la mejora de la correción del ejercicio: 

def test_str_tweet(tweet):
    # Comprobamos la representación textual de un Tweet.
    assert str(tweet) == "@ana: Hola a todos #python #pytest"


def test_str_respuesta(tweet, luis):
    # Creamos una respuesta de Luis al tweet de Ana.
    respuesta = Respuesta(luis, "¡Bienvenida! #Python", tweet)

    # Debe mostrar al autor de la respuesta y al autor del original.
    assert str(respuesta) == "@luis ↩ @ana: ¡Bienvenida! #Python"


def test_str_retweet(tweet, luis):
    # Creamos un retweet de Luis sobre el tweet de Ana.
    retweet = Retweet(luis, tweet)

    # Después del símbolo de retweet debe aparecer str(original).
    assert str(retweet) == "@luis 🔁 @ana: Hola a todos #python #pytest"