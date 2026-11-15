import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datos"
SQL_DIR = BASE_DIR / "consultas"
DB_PATH = BASE_DIR / "pipeline.duckdb"

def read_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text(encoding="utf-8")

def count(con, table: str) -> int:
    return con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

def run_pipeline():
    con = duckdb.connect(str(DB_PATH))

    print("1. Extracción y carga")
    con.execute(read_sql("extract.sql"), [str(DATA_DIR / "rrhh.sqlite")])
    print("Registros extraídos:", count(con, "raw_rrhh"))

    print("\n2. Validación")
    con.execute(read_sql("validar.sql"))
    print("Registros válidos:", count(con, "validos"))
    print("Registros rechazados:", count(con, "rechazados"))

    print("\n3. Limpieza de rechazados")
    con.execute(read_sql("limpiar.sql"))
    print("Registros recuperados limpios:", count(con, "rechazados_limpios"))

    print("\n4. Unión en tabla_final")
    con.execute(read_sql("unir.sql"))
    print("Total registros en tabla_final:", count(con, "tabla_final"))

    print("\n5. Preguntas de negocio")
    print("\n- Salario promedio por departamento:")
    print(con.execute("""
        SELECT departamento, ROUND(AVG(salario), 2) AS salario_promedio
        FROM tabla_final GROUP BY departamento ORDER BY salario_promedio DESC;
    """).df().to_string(index=False))

    print("\n- Masa salarial total:")
    print(con.execute("""
        SELECT ROUND(SUM(salario), 2) AS masa_salarial_total FROM tabla_final;
    """).df().to_string(index=False))

    print("\n- Empleados por modalidad:")
    print(con.execute("""
        SELECT modalidad, COUNT(*) AS cantidad_empleados
        FROM tabla_final GROUP BY modalidad ORDER BY cantidad_empleados DESC;
    """).df().to_string(index=False))

    print("\n- Empleados ingresados por año:")
    print(con.execute("""
        SELECT EXTRACT(YEAR FROM fecha_ingreso) AS anio, COUNT(*) AS cantidad
        FROM tabla_final GROUP BY anio ORDER BY anio ASC;
    """).df().to_string(index=False))

    print("\n- Top 3 cargos con mejor salario promedio:")
    print(con.execute("""
        SELECT cargo, ROUND(AVG(salario), 2) AS salario_promedio
        FROM tabla_final GROUP BY cargo ORDER BY salario_promedio DESC LIMIT 3;
    """).df().to_string(index=False))

    con.close()

if __name__ == "__main__":
    run_pipeline()
