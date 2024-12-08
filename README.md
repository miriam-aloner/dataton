**Transparencia en Acción: Explorando las Contrataciones Públicas**
Este proyecto presenta un tablero interactivo desarrollado en Dash para facilitar el análisis y monitoreo de datos sobre contrataciones públicas. El objetivo principal es promover la transparencia mediante indicadores visuales y gráficos dinámicos.

Descripción del Proyecto
El tablero permite analizar datos relevantes, como indicadores de planificación, licitación, adjudicación y ejecución. A través de filtros interactivos, gráficos, y un diseño intuitivo, los usuarios pueden explorar información detallada de manera eficiente.

Características Principales
  Generación de datos aplanados:
    *Los datos originales en formato JSON son procesados para generar un DataFrame estructurado.
  
  Cálculo de indicadores:
    *Variables clave son creadas para monitorear cumplimiento y desempeño.

  Visualización interactiva:
    *Filtros por ID, año, estado, y más.
    *Gráficos dinámicos de barras, pastel, y mapas geográficos.
  
  Publicación remota:
    *Integración con ngrok para compartir el tablero desde Colab.
    *Publicación alternativa en Gradio para entornos colaborativos.

Cómo Usarlo
El proyecto está dividido en varias fases, cada una correspondiente a un archivo Python:

1. CrearData.py
Este archivo se utiliza para:
  Aplanar las claves de los archivos JSON originales.
  Seleccionar las variables relevantes que alimentarán el tablero.
Uso:
  Coloca los archivos JSON en la carpeta indicada.
  El resultado será un archivo df_data.csv que se usará en las siguientes etapas.

2. CrearFlags.py
Este script genera las variables adicionales necesarias para los indicadores del tablero.

Uso:
    Asegúrate de que el archivo df_data.csv esté en la misma carpeta.
    Esto producirá un archivo actualizado con variables como flag.planning, flag.tender, entre otras.

3. CrearDashboard.py
Este archivo contiene el código principal para construir el tablero en Dash.

Uso:
    Asegúrate de que el archivo generado por CrearFlags.py esté en la misma carpeta.
    El tablero estará disponible localmente en http://127.0.0.1:8050.

4. conoce.ngrok.py
Este archivo contiene las instrucciones para publicar el tablero desde Google Colab utilizando ngrok.

Uso:
    Abre tu notebook en Google Colab.
    Ejecuta el script siguiendo las instrucciones para autenticar y configurar ngrok.
    Se generará un enlace público para acceder al tablero.

5. dashboardcongradio.py
Este archivo es una alternativa para publicar el tablero utilizando Gradio.

Uso:
    Abre el script en tu entorno local o Google Colab.
    Un enlace público será generado automáticamente para compartir el tablero.

*Requisitos*
Asegúrate de instalar las siguientes bibliotecas antes de comenzar:
  <pip install pandas plotly dash gradio>

Estructura del Proyecto
CrearData.py: Aplana claves de archivos JSON y selecciona datos relevantes.
CrearFlags.py: Genera variables de monitoreo de indicadores.
CrearDashboard.py: Construye el tablero interactivo en Dash.
conoce.ngrok.py: Publica el tablero usando ngrok desde Google Colab.
dashboardcongradio.py: Publica el tablero en Gradio como alternativa.
df_data.csv: Archivo de datos estructurados generado por CrearData.py.
README.md: Documentación del proyecto.

*Tecnologías Usadas*
Dash: Para la creación del tablero interactivo.
Plotly: Para gráficos dinámicos y atractivos.
Gradio: Para compartir el tablero de forma remota.
ngrok: Para publicar el tablero desde Google Colab.
Pandas: Para el procesamiento y limpieza de datos.

Contribuciones
Este proyecto está abierto a contribuciones. Si tienes sugerencias o mejoras, crea un fork del repositorio y envía un pull request.

Autores: 
Miriam Alonso 
Hugo Alonso 
  Consultor: Arturo Guzmán 
