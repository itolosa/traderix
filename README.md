# Traderine

Bot de telegram para consultar precios de criptomonedas.

Actualmente solo consulta el precio de la Chaucha.

Instalación
===========

Solo basta con clonar el repositorio e instalar las dependencias:
```bash
$ git clone git@github.com:itolosa/traderine.git
$ cd traderine && pip install -r requirements.txt
```

**Nota: Se recomienda fuertemente usar [virtualenv](https://virtualenv.pypa.io/en/stable/) para evitar conflictos con otros paquetes del sistema al instalar las dependencias.**

Posteriormente se debe modificar el archivo `connvars.py` para agregar un token. Para generar un Access Token, se debe hablar con [BotFather](https://telegram.me/botfather) y seguir una serie de pasos sencillos (descrito [aquí](https://core.telegram.org/bots#6-botfather)).

Finalmente se puede correr el bot:
```bash
$ python traderine.py
```

Al inicio aparecerán algunos datos que hay que llenar en la línea de comandos referentes a la cuenta usada para hacer consultas en orionx.io. Para configuración más detallada véase la librería [orionx-api-client](https://github.com/itolosa/orionx-api-client)
