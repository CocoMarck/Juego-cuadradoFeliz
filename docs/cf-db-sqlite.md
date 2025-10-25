# Cuadrado Feliz SQlite DB
Base de datos `CuadradoFeliz.sqlite`, contendre toda la información necesaria para ejecutar el juego.

El orden de las tablas mencionadas, es por pioridad de funcion.

# Tabla `Render`
Columnas:
- `ResolutionX`: INT
- `ResolutionY`: INT
- `GridSize`: INT

Por defecto: `960x540`, `16`

Función: Estos datos determinan como se renderizara y funcionara el juego.

# Tabla `RenderPrefix`
Columnas:
- `RenderPrefixId`: INT Autoincrement
- `Name`: TEXT
- `ResolutionX`: INT
- `ResolutionY`: INT
- `GridSize`: INT

Función: Configuraciones funcionales para renderizado de juego.


# Tabla `Player`
Columnas:
- `PlayerId`
- `Name`

# Tabla `Item`
Clumnas:
- `ItemId`
- `Name`

# Tabla `CurrentLevel`
Columnas:
- `CurrentLevelId`: INT
- `Level`: TEXT
- `PositionX`: INT
- `PositionY`: INT
- `Score`: INT
- `Hp`: INT
- `Deaths`: INT
- `ItemId`: INT
- `PlayerId`: INT

Función: Determina el nivel actual del jugador, su nombre, su posición, su vida, sus puntos, su vida, la cantidad de muertes, su actual item.

# Tabla `Graphic`
Columnas:
- `ResolutionX`: INT
- `ResolutionY`: INT
- `FullScreen`: BOOL/INT
- `Cloud`: BOOL/INT
- `Collider`: BOOL/INT
- `Sprite`: BOOL/INT

Por defecto: `960x540`

Función: Estos datos determinan solo lo visual del juego, no altera el gameplay.

# Tabla `Volume`
Columnas:
- `Volume`: DOUBLE
- `Music`: BOOL/INT
- `ClimateSound`: BOOL/INT
- `CurrentLevel`: TEXT

Función: Estos datos determinan el audio del juego, no altera el gameplay.

# Tabla `GameComplete`
- `GameCompleteId`: INT Autoincrement
- `Level`: TEXT
- `Date`: DATETIME/TEXT
- `Hp`: INT
- `Deaths`: INT
- `ItemId`: INT
- `PlayerId`: INT
- `Score`: INT

Función: Determina el juego completado.
