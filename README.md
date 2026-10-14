# Red Social ( Desarrollado: Beatriz Henche )

Proyecto desarrollado en Python que simula el funcionamiento básico de una red social similar a Twitter.

La aplicación permite registrar usuarios, establecer relaciones de seguimiento entre ellos y crear distintos tipos de publicaciones. También permite consultar el timeline de un usuario, extraer hashtags, contabilizar tendencias y gestionar los "me gusta" de las publicaciones.

Los usuarios y sus relaciones iniciales se cargan desde el fichero `datos/usuarios.json`.

## Estructura del proyecto

```text
bha-red-social/
├── datos/
│   └── usuarios.json
├── red_social/
│   ├── publicacion.py
│   ├── red.py
│   └── usuario.py
├── tests/
│   ├── conftest.py
│   ├── test_publicacion.py
│   ├── test_red.py
│   └── test_usuario.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Clases principales

### Usuario

La clase `Usuario` representa a cada usuario registrado en la red social.

Cada usuario contiene:

- Un nombre.
- Un alias, que siempre comienza por `@`.
- Una lista de otros objetos `Usuario` a los que sigue.

Entre sus principales funcionalidades se encuentran seguir a otros usuarios, comprobar si sigue a un usuario concreto, consultar el número de usuarios seguidos y convertir sus datos entre objetos y diccionarios.

También se controla que un usuario no pueda seguirse a sí mismo ni seguir dos veces al mismo usuario.

### Publicacion

`Publicacion` es una clase abstracta que contiene el comportamiento común de todas las publicaciones de la red.

Una publicación contiene:

- Un autor, representado mediante un objeto `Usuario`.
- Un texto.
- Un contador de "me gusta".
- Los hashtags incluidos en el texto.

El texto de una publicación no puede estar vacío y tiene un límite máximo de 280 caracteres.

La clase también contiene la lógica para localizar hashtags mediante una expresión regular, convertirlos a minúsculas y eliminar hashtags duplicados.

Al ser una clase abstracta, `Publicacion` no se instancia directamente, sino que sirve como clase padre para los distintos tipos de publicaciones.

### Tweet

`Tweet` hereda de `Publicacion` y representa una publicación normal realizada por un usuario.

```text
Publicacion
    └── Tweet
```

Utiliza los atributos y métodos definidos en la clase padre y define su propia representación mediante el método `__str__`.

### Respuesta

`Respuesta` también hereda de `Publicacion`.

Además de los atributos comunes de una publicación, almacena una referencia a la publicación original a la que está respondiendo.

```text
Publicacion
    └── Respuesta
          └── contiene una referencia a otra Publicacion
```

De esta forma se utiliza tanto **herencia**, porque `Respuesta` es un tipo de `Publicacion`, como **composición**, porque cada respuesta contiene otra publicación como atributo `original`.

### Retweet

`Retweet` hereda igualmente de `Publicacion`.

Un retweet contiene:

- El usuario que realiza el retweet.
- Una referencia a la publicación original.
- El mismo texto que la publicación original.

```text
Publicacion
    └── Retweet
          └── contiene una referencia a otra Publicacion
```

Al igual que en `Respuesta`, se combina herencia con composición.

### RedSocial

La clase `RedSocial` se encarga de gestionar el conjunto de usuarios y publicaciones.

Mantiene dos estructuras principales:

- Un diccionario de usuarios, donde la clave es el alias y el valor es un objeto `Usuario`.
- Una lista de objetos `Publicacion`.

Entre sus funcionalidades se encuentran:

- Registrar y añadir usuarios.
- Publicar contenido.
- Obtener el timeline de un usuario.
- Calcular los hashtags más utilizados mediante `Counter`.
- Mostrar el timeline.
- Cargar usuarios y relaciones de seguimiento desde un fichero JSON.

También implementa métodos especiales de Python que permiten utilizar objetos `RedSocial` de una forma más natural:

- `len(red)` devuelve el número de usuarios.
- `for usuario in red` permite recorrer los usuarios ordenados por alias.
- `"@ana" in red` permite comprobar si existe un alias.
- `red["@ana"]` permite acceder directamente al objeto `Usuario` asociado a un alias.

## Herencia y relación entre objetos

La jerarquía principal de clases del proyecto es:

```text
                Publicacion
                    │
        ┌───────────┼───────────┐
        │           │           │
      Tweet     Respuesta     Retweet
                    │           │
                    └─────┬─────┘
                          │
                  Publicacion original
```

`Tweet`, `Respuesta` y `Retweet` heredan de la clase abstracta `Publicacion`.

Por otro lado, los objetos se relacionan entre sí mediante composición:

- Una `Publicacion` contiene un objeto `Usuario` como autor.
- Un `Usuario` contiene una lista de otros objetos `Usuario` a los que sigue.
- Una `Respuesta` contiene una referencia a otra `Publicacion`.
- Un `Retweet` contiene una referencia a otra `Publicacion`.
- `RedSocial` contiene objetos `Usuario` y objetos `Publicacion`.

## Decorador de "me gusta"

Como en el main.py se printean las publicaciones añadiendo el número de "me gustas" de cada una, se ha creado en el módulo `publicacion.py` el decorador `megusta`.

Este decorador se aplica al método `__str__` de los distintos tipos de publicaciones y añade a su representación el número de "me gusta" junto al símbolo de un corazón.

De esta forma, la funcionalidad se define una única vez y se reutiliza en `Tweet`, `Respuesta` y `Retweet`.

En el caso de las publicaciones `Retweet` aparecen tanto los "me gusta" de la publicacion original como los que ha recibido el propio retweet.

Dado que en la corrección del ejercicio se detecta como error el haber modificado el `main.py`, se crea un `main_with_decorator.py` alternativo, y para su ejecución es necesario descomentar el decorador @megusta de las clases `Tweet`, `Respuesta` y `Retweet` y la definición del mismo al incio de `publicacion.py`

## Datos iniciales

Los usuarios y las relaciones de seguimiento iniciales se almacenan en:

```text
datos/usuarios.json
```

El método `RedSocial.desde_json()` lee este fichero, crea los objetos `Usuario` correspondientes y establece posteriormente las relaciones de seguimiento entre ellos.

## Requisitos

El proyecto utiliza Python 3.12 y está gestionado mediante `uv`.

Las dependencias de desarrollo utilizadas son:

- `pytest`
- `pytest-mock`
- `ruff`

Para instalar y sincronizar las dependencias del proyecto se puede ejecutar:

```bash
uv sync
```

## Ejecución del proyecto

El punto de entrada del proyecto es `main.py`.

Para ejecutar la aplicación utilizando el entorno gestionado por `uv`:

```bash
uv run main.py
```

El programa carga los usuarios desde el fichero JSON y muestra distintos ejemplos del funcionamiento de la red social: usuarios, seguimientos, publicaciones, "me gusta", hashtags, timeline y tendencias.

Si se quisiera ejecutar teniendo en cuenta el decorador `@megusta` añadido, sería necesario descomentarlo de las clases en `publicacion.py` y ejecutar:

```bash
uv run main_with_decorator.py
```

## Tests

Los tests unitarios están implementados con `pytest`.

Se comprueban, entre otros aspectos:

- La creación y comportamiento de los usuarios.
- Las restricciones al seguir usuarios.
- La validación del texto de las publicaciones.
- La extracción y eliminación de hashtags duplicados.
- El funcionamiento de los retweets.
- La generación del timeline.
- La carga de usuarios y seguimientos desde JSON.
- La lectura del fichero mediante mocking.

Para ejecutar todos los tests:

```bash
uv run pytest -v
```

Las fixtures compartidas utilizadas por los tests se encuentran en:

```text
tests/conftest.py
```

Para probar la lectura del JSON sin depender de un fichero físico se utiliza `pytest-mock`, sustituyendo temporalmente `open()` por un mock.

## Calidad y formato del código

El proyecto utiliza Ruff para revisar y mantener el código formateado.

Para comprobar el código:

```bash
uv run ruff check .
```
