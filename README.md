# Trabajo Práctico Final Big Data: Pipeline ETL — TecnoSur S.A.

Proyecto final de Big Data enfocado en la construcción de un pipeline ETL automatizado y resiliente utilizando **DuckDB** y **Apache Airflow**, procesando datos de Recursos Humanos de **TecnoSur S.A.** con validación estricta, limpieza de inconsistencias y resolución de consultas de negocio mediante SQL.

---

## 📁 Estructura del Proyecto

```
tp_final_rrhh/
├── .gitignore                      # Exclusiones de Git (entornos, logs, temporales)
├── README.md                       # Documentación principal del proyecto
├── requirements.txt                # Dependencias requeridas
├── informe.md                      # Informe técnico de 1 página (métricas y hallazgos)
├── pipeline.py                     # Script ejecutable standalone del ETL completo
├── consultas.sql                   # Consultas SQL para responder preguntas de negocio
├── analisis.duckdb                 # Base DuckDB con todas las tablas generadas
└── dags/
    ├── main.py                     # DAG de Airflow orquestado a las 02:00 AM
    ├── data/
    │   └── rrhh.sqlite             # Base de origen en SQLite (intacta, sin modificar)
    ├── output/
    │   └── empleados_limpios.parquet # Exportación final consolidada
    └── sql/
        ├── extract.sql             # Extracción y carga cruda en 'raw_empleados'
        ├── validate.sql            # Validación con 10 reglas y separación validos/rechazados
        ├── clean.sql               # Limpieza y recuperación en 'rechazados_limpios'
        ├── final.sql               # Consolidación final en 'tabla_final' (tipada y sin duplicados)
        ├── export.sql              # Consulta de exportación
        └── consultas.sql           # Copia de consultas de negocio en carpeta SQL
```

---

## 🛠️ Instalación y Configuración del Entorno

Siguiendo la metodología del equipo mediante `uv`:

```bash
# 1. Ingresar a la carpeta del proyecto
cd tp_final_rrhh

# 2. Crear el entorno virtual con uv
uv venv env

# 3. Activar el entorno virtual
source env/bin/activate

# 4. Instalar las dependencias
uv pip install -r requirements.txt
```

---

## 🚀 Ejecución del Pipeline ETL

### Opción 1: Ejecución Directa (Standalone)
Para ejecutar todas las etapas del pipeline, validar datos, limpiar inconsistencias y responder las preguntas de negocio en consola de forma inmediata:

```bash
python pipeline.py
```

### Opción 2: Orquestación con Apache Airflow
El DAG `etl_rrhh` está programado para ejecutarse diariamente a las **02:00 AM** (`schedule="0 2 * * *"`):

```bash
# Iniciar Airflow en modo standalone (para pruebas locales)
export AIRFLOW_HOME=$(pwd)
airflow standalone
```

Acceder a la interfaz web de Airflow en `http://localhost:8080`, activar el DAG **`etl_rrhh`** y disparar la ejecución manual si se desea probar.

---

## 🧪 Batería de Reglas de Calidad (Validación)

Cada registro de `raw_empleados` se evalúa mediante 10 reglas nombradas:

| Regla | Nombre | Condición de Rechazo | Cantidad |
|---|---|---|:---:|
| **R1** | `R1_ID_NULO` | `id_empleado` nulo o vacío | 0 |
| **R2** | `R2_ID_DUPLICADO` | Identificador repetido en la carga | 75 |
| **R3** | `R3_NOMBRE_INCOMPLETO` | `nombre` nulo o en blanco | 0 |
| **R4** | `R4_APELLIDO_INCOMPLETO` | `apellido` nulo o en blanco | 0 |
| **R5** | `R5_EMAIL_INVALIDO` | `email` nulo o sin formato corporativo | 150 |
| **R6** | `R6_DEPARTAMENTO_INVALIDO` | `departamento` nulo o fuera de dominio | 150 |
| **R7** | `R7_CARGO_INVALIDO` | `cargo` nulo o inexistente | 0 |
| **R8** | `R8_SALARIO_INVALIDO` | `salario` negativo o menor/igual a cero | 100 |
| **R9** | `R9_FECHA_INGRESO_INVALIDA` | Fecha no acorde a formato ISO (`YYYY-MM-DD`) | 250 |
| **R10** | `R10_MODALIDAD_INVALIDA` | Modalidad desconocida | 0 |

- **Total Extraído:** 2.575 filas.
- **Registros Válidos Iniciales:** 1.850 filas.
- **Registros Rechazados:** 725 filas.
- **Registros Limpios Recuperados:** 650 filas (se eliminan 75 duplicados).
- **Consolidación en `tabla_final`:** **2.500 registros únicos y limpios**.

---

## 📊 Respuestas a las Preguntas de Negocio

Consultas SQL ejecutadas sobre la tabla definitiva `tabla_final`:

1. **¿Cuál es el salario promedio por departamento?**
   - Tecnología: $1.774.297,92 ARS (819 empleados)
   - Finanzas: $1.680.992,84 ARS (559 empleados)
   - RRHH: $1.466.407,60 ARS (579 empleados)
   - Comercial: $1.423.987,11 ARS (543 empleados)

2. **¿Cuánto es la masa salarial total de la empresa?**
   - **$4.015.100.000,00 ARS** mensuales.

3. **¿Cuántos empleados hay por modalidad de trabajo?**
   - Remoto: 891 (35,64%)
   - Presencial: 832 (33,28%)
   - Híbrido: 777 (31,08%)

4. **¿Cuántos empleados ingresaron por año?**
   - Distribución continua entre 2015 y 2024 (promedio de ~260 ingresos anuales).

5. **¿Cuáles son los 3 cargos con mejor salario promedio?**
   - Desarrollador: $2.037.818,18 ARS
   - Analista de datos: $1.943.978,10 ARS
   - Contador: $1.738.793,10 ARS

---

## 🐙 Instrucciones para Subir a GitHub

Para subir este proyecto a un repositorio propio en GitHub:

```bash
# 1. Ingresar a la carpeta del proyecto
cd "tp_final_rrhh"

# 2. Inicializar el repositorio Git local
git init

# 3. Agregar los archivos al stage
git add .

# 4. Crear el commit inicial
git commit -m "feat: entrega trabajo final big data - pipeline ETL TecnoSur S.A."

# 5. Configurar rama principal
git branch -M main

# 6. Vincular el repositorio remoto de GitHub (reemplazar con la URL de tu repo)
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

# 7. Subir el código
git push -u origin main
```
