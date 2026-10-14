
import re
from abc import ABC, abstractmethod


#Decorador que añade en el str el nº de "me gusta" con el corazón
def megusta(func):
    def envoltura(self):
        print = func(self)
        return f"{print} ♥ {self.me_gusta}"
    return envoltura

# Establecemos como regla un máximo de caracteres para todas las publicaciones.
LIMITE_CARACTERES = 280

class Publicacion(ABC):
    def __init__(self, autor, texto):
        self.autor = autor  # autor es un OBJETO Usuario.
        self.texto = texto # texto es un str.
        self.me_gusta = 0  
        # No permitimos que haya texto vacío ni compuesto solo por espacios.
        if texto.strip() == "":
            raise ValueError("Texto vacío")
        # Evitamos superar los 280 caracteres.
        elif len(texto) > LIMITE_CARACTERES:
            raise ValueError("Supera el máximo de caracteres")

    def dar_me_gusta(self):
        # Modificamos el atributo me_gusta de cada objeto Publicacion.
        self.me_gusta += 1

    @staticmethod
    def extraer_hashtags(texto):
        # Obtenemos un texto y localizamos sus hashtags.
        regex = r"(#[A-Za-z0-9]+)"
        hashtags = re.findall(regex,texto.lower()) #findall() busca todas las coincidencias.
        # Eliminamos duplicados.
        hashtags = list(dict.fromkeys(hashtags))
        return hashtags #Devuelve una lista con las coincidencias de la regex.

    @property
    def hashtags(self):
        return self.extraer_hashtags(self.texto)
    
    @abstractmethod
    def __str__(self):
        # Publicacion no decide cómo se muestra, cada hija tiene que implementar su propio __str__.
        pass


class Tweet(Publicacion):
    @megusta # Decorador para añadir los likes 
    def __str__(self):
        # El autor es un Usuario, por eso podemos acceder a .alias.
        return f"{self.autor.alias}: {self.texto}"

class Respuesta(Publicacion):
    def __init__(self,autor,texto,original):
        # Creamos primero toda la parte común de una Publicacion.
        super().__init__(autor,texto)

        # Guardamos la publicación a la que estamos respondiendo.
        self.original = original

    @megusta # Decorador para añadir los likes
    def __str__(self):
        return f"{self.autor.alias} ↩ {self.original.autor.alias}: {self.texto}"

class Retweet(Publicacion):
    def __init__(self, autor, original):
        # Reutilizamos el constructor de la clase base con super().
        super().__init__(autor,original.texto)
        # Guardamos dentro del retweet la publicación original completa.
        self.original = original

    @megusta # Decorador para añadir los likes
    def __str__(self):
        # self.autor.alias -> alias del usuario que hace el retweet
        # self.original -> usa el __str__ de la publicación original.
        return f"{self.autor.alias} 🔁 {self.original}"
