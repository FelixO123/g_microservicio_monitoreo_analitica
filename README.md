# Microservicio de Monitoreo y Analítica

Este microservicio se encarga de almacenar indicadores clave de desempeño, métricas de avance, utilización de recursos y estado general de la organización dentro del ecosistema del proyecto, estos datos se usaran en el frontend para visualizarlos a traves de un panel interactivo (Dashboard).

## Tecnologías utilizadas
* **Lenguaje:** Python 3.12.2
* **Framework:** FastAPI
* **Base de Datos:** PostgreSql (NeonDb)
* **Dependencias principales:** 
- FastAPI: El framework web que usas.

- Uvicorn: El servidor ASGI para ejecutar la app.

- SQLAlchemy: El ORM para manejar la base de datos.

- Psycopg2-binary: El driver para conectar con PostgreSQL.

- Pydantic: Para la validación de datos y esquemas.

- Python-dotenv: Para la gestión de variables de entorno (el archivo .env).

- Pytest: El framework que usaste para las pruebas (testing).

## Estructura del Proyecto
* `app/`: Contiene el código fuente del microservicio.
* `.env`: Archivo de configuración para variables de entorno (no incluido en Git).
* `venv/`: Carpeta del entorno virtual donde se instalan las librerías necesarias para el microservicio. (Excluido de Git).
* `requirements.txt`: Lista de librerías necesarias.

## Instalación y Configuración Local

Sigue estos pasos para levantar el servicio:

1. **Clonar el repositorio y abrir proyecto github clonado**
- Ejecutar comando git clone https://github.com/FelixO123/g_microservicio_monitoreo_analitica.git en la ruta que se desee (Recomendacion en el Escritorio).

- Entrar a la carpeta del repositorio con el editor de texto preferido (VS code, etc.)

2. **Crear y activar entorno venv** 
- Ejecutar desde carpeta raiz: 

    - python -m venv venv
    - .\venv\Scripts\activate

Si todo esta bien deberia verse (venv) en color verde al principio de la ruta (Vs Code)

3. **Instalar dependencias**
- Ejecutar desde carpeta raiz:
    
    - pip install -r requirements.txt

Si se pide actualizar el pip realizarlo.

4. **Configurar variables de entorno**

Para que el microservicio funcione, crea un archivo `.env` en la raíz del proyecto y define las siguientes variables:

- `DATABASE_URL`: URL de conexión a PostgreSQL (Proyecto NeonDb)
- `PORT`: Puerto en el que correrá el servidor (ej. `8000`)


5. **Ejecutar el servidor**

- Ejecutar desde la carpeta raiz: uvicorn app.main:app --reload

## API endpoints

- **CRUD KPI**:

    - GET /api/analisis/kpi: Listar todos los KPIs registrados

    - GET /api/analisis/kpi/{id}: Obtener detalle de un KPI en especifico.

    - POST /api/analisis/kpi: Crear un nuevo indicador clave para un proyecto.

    - PUT /api/analisis/kpi/{id}: Actualiza un Kpi

    - DELETE /api/analisis/kpi/{id}: Eliminar un registro de KPI.

    - POST /api/analisis/reportes/periodico: función que recolecta los datos de los otros microservicios

    - GET /api/analisis/alertas: Para detectar si un proyecto tiene un porcentaje de avance bajo comparado con la fecha final de la tarea.

- **CRUD UTILIZACIÓN DE PERSONAL**:

    - GET /api/analisis/ocupacion: % de carga de trabajo de todo el personal.

    - GET /api/analisis/ocupacion/{id_usuario}: Ver el porcentaje de ocupación de un usuario específico.

- **DASHBOARD**:

    - GET /api/analisis/dashboard: todos los datos consolidados para los gráficos del sistema.

    - GET /api/analisis/reportes: Listar reportes con su resumen y estado_general.

    - GET /api/analisis/reportes/{id_reporte}: Muestra un reporte en especifico por su id.

    - POST /api/analisis/reportes: Generar un nuevo reporte.

    - PUT /api/analisis/reportes/{id_reportes}: Actualizar un reporte

    - DELETE /api/analisis/reportes/{id_reportes}: Eliminar un reporte

- **CRUD DE METRICAS DE PROYECTOS**:

    - GET /api/analisis/metricas: Muestra todas las metricas de los proyectos

    - GET /api/analisis/metrica/{id_metrica}: Muestra una métrica en especifico

    - GET /api/analisis/metricas/proyectos/{id_proyecto}: Muestra la metrica de un proyecto en especifico

    - POST /api/analisis/metrica: Crea una metrica de proyectos

    - PUT /api/analisis/metrica/{id_metrica}: Actualiza una métrica de proyectos

    - DELETE /api/analisis/metrica/{id_metrica}: Elimina una metrica





 










