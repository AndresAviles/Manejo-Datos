import sqlite3
import pandas as pd
import os

# Cargar el CSV con Pandas

CSV_PATH = "members.csv"
DB_NAME  = "database_EP.AAA"      

print("=" * 55)
print("  ACTIVIDAD: CONEXION SQLITE3 + PANDAS")
print("=" * 55)

df = pd.read_csv(CSV_PATH)

print(f"\n[1] CSV cargado exitosamente.")
print(f"    Filas    : {len(df)}")
print(f"    Columnas : {list(df.columns)}")

print("\n[2] Tipos de datos detectados por Pandas:")
print(df.dtypes.to_string())

print("\n[3] Primeras 3 filas del DataFrame:")
print(df.head(3).to_string(index=False))

# Crear la conexion a SQLite

if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

conn   = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

print(f"\n[4] Conexion a '{DB_NAME}' establecida correctamente.")

# Insertar el DataFrame en SQLite

df.to_sql("members", conn, if_exists="replace", index=False)

print(f"[5] Tabla 'members' creada e insertada en la base de datos.")

# Mostrar el Schema SQL
print("\n" + "=" * 55)
print("  SCHEMA SQL (CREATE TABLE):")
print("=" * 55)

cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='members';")
schema = cursor.fetchone()[0]
print(schema)

# Verificacion primeras filas desde SQLite

print("\n[6] Primeras 5 filas desde SQLite (SELECT):")
cursor.execute("SELECT * FROM members LIMIT 5;")
rows = cursor.fetchall()
col_names = [description[0] for description in cursor.description]
print("  " + " | ".join(col_names))
print("  " + "-" * 80)
for row in rows:
    print("  " + " | ".join(str(v) for v in row))

# Consultas de analisis
print("\n[7] Total de registros en la tabla:")
cursor.execute("SELECT COUNT(*) FROM members;")
print(f"    {cursor.fetchone()[0]} registros.")

print("\n[8] Distribucion por genero:")
cursor.execute("SELECT gender, COUNT(*) AS total FROM members GROUP BY gender;")
for row in cursor.fetchall():
    print(f"    {row[0]}: {row[1]}")

print("\n[9] Ciudades con mayor numero de miembros (Top 5):")
cursor.execute("""
    SELECT city, COUNT(*) AS total
    FROM members
    GROUP BY city
    ORDER BY total DESC
    LIMIT 5;
""")
for row in cursor.fetchall():
    print(f"    {row[0]}: {row[1]}")

# Analisis del tipo de dato birth_date

print("\n" + "=" * 55)
print("  ANALISIS: ¿Por que birth_date es TEXT en SQLite?")
print("=" * 55)
print("""
  SQLite utiliza un sistema de tipos dinamico llamado
  'Type Affinity'. Al importar desde un CSV mediante
  Pandas, la columna 'birth_date' (con valores en
  formato 'YYYY-MM-DD' como texto) es reconocida por
  Pandas como dtype 'object' (cadena de texto).

  Al traspasar el DataFrame a SQLite con to_sql(),
  Pandas mapea 'object' -> TEXT en SQLite, ya que
  SQLite no tiene un tipo nativo DATE/DATETIME.

  SQLite almacena fechas como TEXT, REAL o INTEGER
  segun la conveniencia del desarrollador.
  El formato ISO 8601 (YYYY-MM-DD) es el recomendado
  pues permite ordenar y comparar fechas directamente
  con operadores de cadena.
""")

print("=" * 55)
print("  VENTAJA PRINCIPAL DE PANDAS EN ESTE PROCESO:")
print("=" * 55)
print("""
  Pandas permite cargar, transformar e insertar un
  CSV de 5,000 filas en SQLite con una sola linea:

      df.to_sql("members", conn, if_exists="replace")

  Sin Pandas habria que:
    - Abrir y parsear el CSV manualmente (csv.reader)
    - Construir el CREATE TABLE con los tipos correctos
    - Iterar fila por fila con cursor.executemany()
  
  Pandas automatiza inferencia de tipos, manejo de
  valores nulos, y la creacion del esquema SQL, lo
  que reduce el codigo significativamente y minimiza
  errores en la insercion masiva de datos.
""")

# Cerrar conexion
conn.close()
print(f"[FIN] Conexion cerrada. Base de datos guardada en: {DB_NAME}")
print("=" * 55)
