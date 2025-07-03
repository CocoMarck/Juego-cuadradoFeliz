# Se tendera que hacer el juego de esta manera

# Pantalla de juego y ventana

### Este patron se llama `render target + scale`
El juego estara contenido en un `Surface` este tendra todos los colliders y sprites.  
El `Surface` que contenga el juego, siempre mantendra su resolución.

El juego se vera en una ventana que sera llamada `window`, esta mostrara el `Surface` antes mencionado.  
El `Surface` que contenga el juego siempre sera escalado al tamaño del `window`. 
Con fin de que se vea coherente en la ventana.


# Colliders y sprites separados
Los colliders y los sprites deben estar bien separados.  
Los colliders les da igual que resolucion tenga la pantalla, ellos siempre tendran la misma.  
Los sprites si se escalaran dependiendo la resolución de la pantalla. Lo anterior mencionado esta enredado de hacer, pero se puede.

# Utilizar sqlite DB para la configuracion del juego.
Este me ayuda a configurar todo de manera mas sencilla y controlada


# Programar en MVC y en tres capas.
Tener bien claro que va en `data, models, controllers, entities, core, util`.  
Por ahora los objetos `Sprite` pueden ir en `entities/pygame`  
Y las func generles para usar en pygame en `core/pygame`  
