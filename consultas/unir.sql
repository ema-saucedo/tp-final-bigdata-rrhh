CREATE OR REPLACE TABLE tabla_final AS
WITH union_total AS (
    SELECT 
        id_empleado,
        TRIM(nombre) AS nombre,
        TRIM(apellido) AS apellido,
        TRIM(email) AS email,
        CAST(fecha_ingreso AS DATE) AS fecha_ingreso,
        departamento,
        cargo,
        CAST(salario AS DOUBLE) AS salario,
        LOWER(TRIM(modalidad)) AS modalidad
    FROM validos

    UNION ALL

    SELECT 
        id_empleado,
        nombre,
        apellido,
        email,
        CAST(fecha_ingreso AS DATE) AS fecha_ingreso,
        departamento,
        cargo,
        CAST(salario AS DOUBLE) AS salario,
        modalidad
    FROM rechazados_limpios
)
SELECT DISTINCT * FROM union_total;
