# AutoAnswer-Genesys
Este desarrollo activa la respuesta automatica de forma masiva para usuarios de Genesys Cloud

# AutoAnswer Activation for Genesys Cloud

## Descripción

Esta aplicación permite activar la función de AutoAnswer para usuarios específicos en Genesys Cloud, basándose en un archivo Excel cargado por el usuario. La aplicación incluye una interfaz web donde se puede cargar el archivo, seleccionar la organización correspondiente y ver los resultados de la activación.

### Características principales

- **Carga de Usuarios**: Permite cargar un archivo Excel con los nombres de usuario para los cuales se desea activar la función de AutoAnswer.
- **Selección de Organización**: Posibilidad de seleccionar la organización a la cual pertenecen los usuarios, para activar AutoAnswer de forma específica.
- **Visualización de Resultados**: Muestra los usuarios para los cuales se ha activado exitosamente la función, así como aquellos que no se encontraron en la base de datos.
- **Interfaz Intuitiva**: Diseño simple y amigable para facilitar la carga y selección de usuarios.

## Requisitos

- Python 3.x
- Librerías necesarias (ver `requirements.txt`):
  - `Flask`
  - `openpyxl`
  - `PureCloudPlatformClientV2`
  - `pandas`
- Un entorno de Genesys Cloud configurado con permisos para activar la función de AutoAnswer.

## Uso
- Inicia la aplicación Flask: `python app.py`
- Abre `http://localhost:5000` en tu navegador.
- Carga el archivo Excel con los nombres de usuario en la página principal.
- Selecciona la organización correspondiente.
- Haz clic en "Cargar" para visualizar los resultados y seleccionar los usuarios a los que se activará la función de AutoAnswer.
- En la página de resultados, selecciona los usuarios y haz clic en "Activar AutoAnswer".

## Estructura del Proyecto
- `app.py`: Script principal que contiene la lógica de la aplicación Flask y la integración con Genesys Cloud.
- `index.html`: Página principal donde se carga el archivo Excel y se selecciona la organización.
- `results.html`: Página de resultados donde se muestran los usuarios y se activa la función de AutoAnswer.
- `requirements.txt`: Archivo de dependencias necesarias para el proyecto.

## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

- Bryan Ganzen
- 55 75 45 65 81



