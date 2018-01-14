# Traderix

Bot de telegram para consultar precios de criptomonedas.

Actualmente solo consulta el precio de la Chaucha.

Instalación
===========

**Se recomienda fuertemente usar [virtualenv](https://virtualenv.pypa.io/en/stable/) para evitar conflictos con otros paquetes del sistema al instalar las dependencias.**

En un entorno con virtualenv, solo basta con clonar el repositorio e instalar las dependencias:
```bash
$ git clone git@github.com:itolosa/traderix.git
$ cd traderix && pip install -r requirements.txt
```

Posteriormente se debe crear el archivo `connvars.py` para agregar un token. Para ello se puede usar el archivo `connvars.example.py` como referencia. Para generar un Access Token, se debe hablar con [BotFather](https://telegram.me/botfather) y seguir una serie de pasos sencillos (descrito [aquí](https://core.telegram.org/bots#6-botfather)).

Finalmente se puede correr el bot:
```bash
$ python traderix.py
```

Al inicio aparecerán algunos datos que hay que llenar en la línea de comandos referentes a la cuenta usada para hacer consultas en orionx.io. Para configuración más detallada véase la librería [orionx-api-client](https://github.com/itolosa/orionx-api-client)

Librerias usadas
================

* [ccxt](https://github.com/ccxt/ccxt)
* [orionx-api-client](https://github.com/itolosa/orionx-api-client)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

Donaciones
==========

Se aceptan aportes voluntarios en cualquiera de las siguientes direcciones:

* Chaucha: cbgZyHdUZuEecs4owjUang3gsPpxtt8to3
* Bitcoin: 14foW9hVWzqYTRoQkiiBUvZtcxEdxnsCmi
* Litecoin: LLkZc1Emt61dfYoP7hNVvMufWwS3GJd7BP
* Ethereum: 0xFe8c7e7aC07b68EF19B695ED218784c3F897BD55

gracias! ;)