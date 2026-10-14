class Usuario:
    def __init__ (self,nombre,alias):
        self.nombre = nombre
        self.alias = alias
        self.seguidos = []
        # El alias siempre tiene que empezar por @.
        # Si no lo tiene, se lo añadimos.
        if not self.alias.startswith("@"):
            self.alias = "@" + self.alias

    def seguir(self,otro):
        # Evitamos que un usuario pueda seguirse a sí mismo.
        if otro is self:
            raise ValueError("Un usuario no se puede seguir a sí mismo")
        elif otro in self.seguidos:
        # Evitamos guardar dos veces el mismo usuario.
            raise ValueError("Este usuario ya le está siguiendo")
        # Si todo está correcto, guardamos el objeto Usuario en la lista.
        else:
            self.seguidos.append(otro)

    def sigue_a(self,otro):
        return otro in self.seguidos

    def a_dict(self):
        # Convertimos el objeto Usuario en un diccionario.
        usuario_dict = {}
        usuario_dict["nombre"] = self.nombre
        usuario_dict["alias"] = self.alias
        return usuario_dict

    @property
    def numero_seguidos(self):
        # Devuelve cuántos objetos Usuario hay en self.seguidos.
        return len(self.seguidos)

    @classmethod
    def desde_dict(cls,datos):
        # Hacemos el camino contrario a a_dict().
        return cls(datos["nombre"], datos["alias"])

    def __str__(self):
        # Decidimos cómo se muestra el objeto cuando hacemos print(usuario).
        return f"{self.nombre} ({self.alias})"

    def __eq__(self,otro):
        # Consideremos a dos usuarios iguales cuando tienen el mismo alias.
        return self.alias == otro.alias

