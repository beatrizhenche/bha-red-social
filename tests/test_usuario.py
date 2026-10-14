import pytest

from red_social.usuario import Usuario


def test_usuario_basico(ana):
    # Comprobamos que el usuario se crea correctamente.
    assert ana.nombre == "Ana"
    assert ana.alias == "@ana"
    assert ana.seguidos == []


def test_seguir_anade_al_otro_usuario(ana, luis):
    # Obtebemos dos objetos usuario, gracias a las fixtures 'ana' y 'luis'.
    
    ana.seguir(luis) 

    assert ana.sigue_a(luis) is True  # Comprobamos que Ana sigue a Luis.
    assert ana.numero_seguidos == 1 # Comprobamos que la lista de usuarios de Ana contiene 1 usuario.
    assert luis.sigue_a(ana) is False # Comprobamos que el seguimiento no es recíproco.



def test_seguirse_a_si_mismo_lanza_error(ana):

    with pytest.raises(ValueError): # Comprobamos que se lanza la excepción que esperamos.

        ana.seguir(ana) # Intentamos que Ana se siga a sí misma.Nuestro método Usuario.seguir() debe impedirlo.


# Tests añadidos para mejorar la correción del ejercicio: 
def test_seguir_usuario_seguido_lanza_error(ana, luis):
    ana.seguir(luis)
    with pytest.raises(ValueError): # Comprobamos que se lanza la excepción que esperamos.        
        ana.seguir(luis) # Deberia generar un error por ser un usuario que ya se sigue


def test_a_dict_convierte_usuario_en_diccionario(ana):
    # El metodo a_dict() no se esta utilizando en ningun caso. No hay escrituras que lo necesiten 
    
    # Convertimos el objeto Usuario en un diccionario.
    resultado = ana.a_dict()

    # Comprobamos el diccionario generado
    assert resultado == {"nombre": "Ana","alias": "@ana"}

def test_desde_dict_crea_usuario():
    # Creamos los datos con el mismo formato que tendría cualquiera de los dicts del json
    datos_dict = {"nombre": "Ana","alias": "@ana"}

    # Convertimos el diccionario en un objeto Usuario.
    usuario = Usuario.desde_dict(datos_dict)

    assert usuario.nombre == "Ana"
    assert usuario.alias == "@ana"
    assert usuario.seguidos == []
