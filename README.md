# Reporte sociodemográfico

Aplicación en Python para generar un reporte sociodemográfico a partir de datos almacenados en SQL Server, exportarlos a Excel y enviarlos por correo.

## Requisitos previos

- Python 3.10 o superior
- pip actualizado
- Controlador ODBC de SQL Server instalado en Windows (recomendado: ODBC Driver 17/18 for SQL Server)
- Acceso a la base de datos y SMTP del entorno correspondiente

## Estructura del proyecto

- `src/`: código fuente de la aplicación
- `recurso/`: recursos del proyecto
- `logs/`: archivos de log
- `.env`: variables de entorno de la aplicación

## 1) Clonar o abrir el proyecto

Desde la carpeta raíz del proyecto:

```bash
cd "C:\ruta\al\proyecto\reporte_sociodemografico"
```

## 2) Crear entorno virtual

```bash
python -m venv .venv
```

Activar el entorno virtual:

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

## 3) Instalar dependencias

```bash
python -m pip install --upgrade pip
pip install pandas pyodbc python-dotenv openpyxl
```

Si `pyodbc` falla al instalarse, instala primero el driver ODBC de SQL Server en el sistema.

## 4) Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con este contenido (ajusta los valores reales de tu entorno):

```env
SERVIDOR_SQL=10.224.217.140
USUARIO_SQL=usretl
BASE_DE_DATOS=Conexion
BD_DATASTEWARD=DATASTEWARD
CONTRASENA_SQL=tu_password

SERVIDOR_SMTP=100.89.32.76
PUERTO_SERVIDOR_SMTP=25
CORREO_REMITENTE=infoExtranet@renault.com
EMAIL_DESTINATARIOS=correo1@ejemplo.com;correo2@ejemplo.com
EMAIL_BODY="Este correo se envía automáticamente desde el sistema Extranet.\n\nPor favor, no responda a este correo."
```

Importante:
- El proyecto busca el archivo `.env` automáticamente en la raíz del proyecto.
- La variable `BD_DATASTEWARD` también se usa en la lógica de conexión; asegúrate de que coincida con el nombre de la base de datos de trabajo.

## 5) Ejecutar la aplicación

Desde la raíz del proyecto y con el entorno virtual activado:

```bash
python -m src.main
```

También puede ejecutarse directamente desde la carpeta `src`:

```bash
python src\main.py
```

## 6) Salida esperada

- Genera el archivo Excel del reporte en la carpeta `recurso/`
- Guarda logs en `logs/log.txt`
- Envía el correo configurado en `.env` si la lógica de envío está habilitada

## 7) Solución si el entorno virtual no tiene pip

Si `python -m venv` no crea `pip`, puedes ejecutar:

```bash
python -m ensurepip --default-pip
```

## 8) Troubleshooting

- Error de `pyodbc`: revisar que el controlador ODBC de SQL Server esté instalado.
- Error de conexión a SQL Server: verificar `SERVIDOR_SQL`, `USUARIO_SQL`, `CONTRASENA_SQL` y `BASE_DE_DATOS`.
- Error de correo: verificar `SERVIDOR_SMTP`, `PUERTO_SERVIDOR_SMTP` y `CORREO_REMITENTE`.
- Error de importación de módulos: confirmar que el entorno virtual esté activado y que todas las dependencias estén instaladas.

## 9) Dependencias principales

- `pandas`
- `pyodbc`
- `python-dotenv`
- `openpyxl`

Si quieres, puedo dejarte también un archivo `requirements.txt` para instalar todo con un solo comando.
