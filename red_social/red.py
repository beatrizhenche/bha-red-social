import json
from collections import Counter

from red_social.usuario import Usuario


class RedSocial:
    def __init__(self):
        self.usuarios = {}
        self.publicaciones = []

 
    def anadir(self,usuario):
        #Comprobaamos que el usuario no exista en el diccionario.
        if usuario.alias in self.usuarios:
            raise ValueError("El usuario ya existe")
        # Guardamos el objeto Usuario en el diccionario.
        self.usuarios[usuario.alias] = usuario
        #Devolvemos el mismo objeto que acabamos de guardar.
        return usuario

    def registrar(self,nombre,alias):
            #Creamos un nuevo objeto usuario.
            usuario = Usuario(nombre,alias)
            #Para guardar el usuario, utilizamos el método añadir.
            return self.anadir(usuario)
            

    def publicar(self,publicacion):
        #Añadimos el obejo publicación al final de la lista de publicaciones.
        self.publicaciones.append(publicacion)
        # Devolvemos ese mismo objeto publicación.
        return publicacion


    def timeline(self,usuario):
        publicaciones_timeline = []

        for publicacion in self.publicaciones:
            if publicacion.autor in usuario.seguidos:
                publicaciones_timeline.append(publicacion)
        publicaciones_timeline.reverse()
        return publicaciones_timeline
        
                         

    def tendencias(self,n=3):
        todos_hashtags = []
        #Se recopilan todos los hashtags de todas las publicaciones.
        for publicacion in self.publicaciones:
            todos_hashtags += publicacion.hashtags 
        #Devuelve un iterable Counter con tuplas (hashtag,frecuencia).
        frecuencia_hashtags = Counter(todos_hashtags) 
        #Devuelve el top n en formato lista.
        most_common_hashtags = frecuencia_hashtags.most_common(n)
        return most_common_hashtags 


            
    def mostrar_timeline(self,alias):
        print(f"\nTimeline de {self.usuarios[alias].nombre} ({alias}):")
        for publicacion in self.timeline(self.usuarios[alias]):
            print(f"  {publicacion}")


    @classmethod
    def desde_json(cls,ruta):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)

        red = cls()

        for datos_usuario in datos["usuarios"]:
            usuario = Usuario.desde_dict(datos_usuario)
            red.anadir(usuario)
        return red



    

        





    
    
