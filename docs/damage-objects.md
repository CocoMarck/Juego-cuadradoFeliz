# Grupo de sprites; `damage_objects`
Estos tipo de objetos, tendran varias caractaristicas: Seran generales, aplicables a cualquier sprite. Se usaran para dañar otros personajes, u objetos.

Este tipo de objetos, funcionan de manera sencilla, pero muy bien. 

## Usos practicos:
Objetos que dañen a objetos tipo character. El character tambien podra hacer daño, pero dependiendo del tipo de `identifer` del character, se hara daño o no

### Supongamos que existen dos objetos tipo `character`, estos son `ally` y `enemy`.
Los `ally` reciven daño de los `enemy` y viceversa, pero los `ally` no reciven daño de `ally`. A pesar de que `ally` tambien es un objeto dañino, al compartir`identifer` con los character `ally`, se ignora el daño.

# Parametros
Seran tres parametros, cantidad de daño, identificador de objeto, y daño activa o desactivado.

## `damage = int or float`
Valor de daño, numeros iguales o menores a 0 hacen instakill.


## `identifer = string`
Necesario, con este se podra determinar que hace daño al objeto y que no.
Por ejemplo, los `damage_objects` con `identifer == character`, no haran daño al `character`.


## `damage_activated = bool`
Este determina si se hara daño o no. Función parecida a identifer, pero menos abstracto.

## Code de ejemplo
```python
if (self.identifer != damage_object.identifer) and (damage_object.damage_activated == True):
    self.hp -= damage_object.damage
```


# Problema actual
Los `player_objects` hacen de `damage_objects`, a pesar de que si tengo `damage_objects`, solo que tal y como tengo los `damage_objects`, tengo que añadir code. Basicamente añadirles los parametros necesarios a los objetos pertenecientes al grupo `damage_objects`
