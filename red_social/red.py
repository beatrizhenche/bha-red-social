import json
from collections import Counter

from red_social.usuario import Usuario


class RedSocial:
    def __init__(self):
        self.usuarios = {} # Diccionario de usuarios, clave: alias - valor: objeto Usuario
        self.publicaciones = [] 

 
    def anadir(self,usuario):
        # Comprobamos que el usuario no exista en el diccionario.
        if usuario.alias in self.usuarios:
            raise ValueError("El usuario ya existe")
        # Guardamos el objeto Usuario en el diccionario.
        self.usuarios[usuario.alias] = usuario
        # Devolvemos el mismo objeto que acabamos de guardar.
        return usuario

    def registrar(self,nombre,alias):
            # Creamos un nuevo objeto usuario.
            usuario = Usuario(nombre,alias)
            # Utilizamos el método añadir para guardar el usuario. 
            return self.anadir(usuario)
            

    def publicar(self,publicacion):
        # Añadimos el obejo publicación al final de la lista de publicaciones.
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
        # Recopilamos todos los hashtags de todas las publicaciones.
        for publicacion in self.publicaciones:
            todos_hashtags += publicacion.hashtags 
        # Devuelve un iterable Counter con tuplas (hashtag,frecuencia).
        frecuencia_hashtags = Counter(todos_hashtags) 
        # Devuelve el top n en formato lista.
        most_common_hashtags = frecuencia_hashtags.most_common(n)
        return most_common_hashtags 


            
    def mostrar_timeline(self,alias):
        print(f"\nTimeline de {self.usuarios[alias].nombre} ({alias}):")
        # Recorremos la lista de publicaciones del timeline del usuario, para mostrarlo.
        for publicacion in self.timeline(self.usuarios[alias]):
            print(f"  {publicacion}")


    @classmethod
    def desde_json(cls,ruta):
        with open(ruta, encoding="utf-8") as f:
            datos = json.load(f)

        red = cls() # Creamos un objeto de tipo RedSocial, donde vamos a cargar usuarios.
        # Extraemos todos los diccionarios del json paara convertirlos en objetos Usuario.
        for datos_usuario in datos["usuarios"]:
            usuario = Usuario.desde_dict(datos_usuario)
            red.anadir(usuario) #Añadimos los usuarios a la red 

        # Establecemos las relaciones entre usuarios, ya cargados en la red.
        # Recorremos las listas [quien_sigue, a_quien] dentro de la clave seguimientos.
        for quien_sigue, a_quien in datos["seguimientos"]:
            # Recuperamos los ususarios a partir de la red con el alias.
            usuario_quien_sigue = red.usuarios[quien_sigue] 
            usuario_a_quien = red.usuarios[a_quien]
            # Establecemos el seguimiento.
            usuario_quien_sigue.seguir(usuario_a_quien) 
        # Devolvemos la red, como haría el init, pero con los usuarios ya cargados y actualizados.    
        return red
    


    def __len__(self):
        # Obtenemos cuántos usuarios hay registrados en la red.
        return len(self.usuarios)
    
    
    def __iter__(self):
        # Recorremos directamente la red.
        for alias in sorted(self.usuarios):
        # En cada vuelta recuperamos el objeto Usuario asociado a ese alias y lo devolvemos uno a uno con yield.
            yield self.usuarios[alias]
    
    def __contains__(self,alias): 
        # Confirmamos que el alias sea una clace de self.usuarios, devolviendo True, si no devuleve False.
        return alias in self.usuarios

    def __getitem__(self,alias):
        # Accedemos a un usuario como si RedSocial fuese un diccionario.
        if self.__contains__(alias):
            return self.usuarios[alias] # Si el alias existe, devolvemos el objeto Usuario.
        else:
            # Si no existe, lanzamos KeyError.
            raise KeyError(f"El alias {alias} no pertenece a ningun usuario registrado en la red")



        





    
    
