import pytest


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