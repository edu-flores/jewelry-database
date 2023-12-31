# Instrucciones de Configuración y Ejecución

A continuación, se detallarán las instrucciones para replicar esta pequeña aplicación en su máquina local.

## Prerequisitos

Antes de ejecutar esta aplicación, asegúrate de tener las siguientes herramientas instaladas en tu sistema:

- [Python 3.x](https://www.python.org/downloads/)
- [MariaDB](https://mariadb.com/downloads/)
- [Node.js](https://nodejs.org/en/download/current)

## Instalación de Requerimientos

Para ejecutar el proyecto, es necesario instalar los requerimientos. Utiliza el siguiente comando en el directorio 'jewelry-database':

```bash
pip install -r requirements.txt
```

## Configuración de la Base de Datos

Es esencial tener una base de datos local instalada para evitar errores al acceder a los servicios de la aplicación. Sigue estos pasos:

1. Ejecuta las instrucciones del archivo `database.sql` en la base de datos de tu elección.
2. Configura las variables de entorno en el archivo `.env`. Consulta el ejemplo en `.env.example` para completarlas.

```bash
mysql -u root -p < database/database.sql
```

## Ejecución de la Aplicación

Una vez que las dependencias estén instaladas y la base de datos configurada correctamente, puedes ejecutar la aplicación. En el directorio 'jewelry-database', utiliza los siguientes comandos:

```bash
export FLASK_APP=app.py
export FLASK_ENV_FILE=.env
flask run --port=5000
```

## Configuración del Socket

En el archivo del microservicio del GPS, ubicado en `services/gps.py`, cambia el valor de `cors_allowed_origins` con la URL en la que se esté ejecutando tu aplicación cliente. Esta URL se obtiene después de ejecutar el último paso de este archivo. La línea deberá ir entre las comillas después de `socketio = SocketIO(gps, cors_allowed_origins="")`.

Ejemplo:

```python
socketio = SocketIO(gps, cors_allowed_origins="http://127.0.0.1:4200")
```

## Ejecución de Microservicios

En cuatro terminales nuevas, dentro de la carpeta 'services', ejecuta los siguientes comandos (un bloque de comandos para cada terminal):

```bash
export FLASK_APP=auth.py
export FLASK_ENV_FILE=../.env
flask run --port=5001
```

```bash
export FLASK_APP=gps.py
export FLASK_ENV_FILE=../.env
flask run --port=5002
```

```bash
export FLASK_APP=routes.py
export FLASK_ENV_FILE=../.env
flask run --port=5003
```

```bash
export FLASK_APP=trucks.py
export FLASK_ENV_FILE=../.env
flask run --port=5004
```

Asegúrate de tener un archivo `.env` en la carpeta raíz configurado adecuadamente.

## Ejecución del Cliente

Para ejecutar el cliente de Angular, instala la línea de comandos **Angular CLI** usando el administrador de paquetes Node.js con el siguiente comando:

```bash
npm install -g @angular/cli
```

Después, dentro del directorio 'client', ejecuta:

```bash
npm install --legacy-peer-deps
ng serve --host 0.0.0.0
```

## Detener la Aplicación

Para detener la aplicación, presiona `Ctrl + C` en tu terminal para enviar una señal de interrupción.
