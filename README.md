# Instrucciones

A continuación, se detallarán las instrucciones para replicar esta pequeña aplicación en su máquina local.

## Prerequisitos

Antes de ejecutar esta aplicación, debes de tener una versión actualizada de Python y MariaDB.

- Python 3.x (https://www.python.org/downloads/)
- MariaDB (https://mariadb.com/downloads/)

## Instalación

1. Clona el repositorio:

   ```powershell
   git clone https://github.com/edu-flores/jewelry-database.git
   ```

2. Navega al directorio en donde se ha clonado:

   ```powershell
   cd app/flask/ejemplo
   ```

3. Crea un ambiente virtual para instalar las dependencias (opcional):

   ```powershell
   python -m venv .venv
   ```

4. Activa el ambiente virtual:

   - Windows:

     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     .venv\Scripts\activate
     ```

   - macOS y Linux:

     ```bash
     source .venv/bin/activate
     ```

5. Instala las dependencias necesarias:

   ```powershell
   pip install -r requirements.txt
   ```

## Configuración

Es necesario tener una base de datos instalada localmente para que la aplicación no muestre errores al momento de acceder a los servicios. Para esto, hay que bajar las tablas y los SP de `database.sql` en una base de datos de tu elección. Posteriormente, configura las variables de enterno del archivo `.env`. El archivo `.env.example` tiene un ejemplo de cómo deben ser llenadas.

## Ejecutar la aplicación

Una vez que las dependencias hayan sido instaladas, y la base de datos haya sido configurada correctamente, el app puede ser ejecutada. Para esto, hay correr el siguiente comando:

```powershell
python main.py
```

Por predeterminado, el app se ejecutará en la dirección `http://localhost:5000/`. Esta puede ser visitada desde tu navegador.

## Parar la aplicación

Para parar la aplicación presiona `Ctrl + C` en tu terminal para mandar una señal de interrupción. Para salir del ambiente virtual (en caso de haberlo creado) debes correr:

```powershell
deactivate
```