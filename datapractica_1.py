import sqlite3 
import pandas as pd
import re

DB = "members.db"
CSV = "members.csv"
# cargar el archivo members a sqlite3
def cargar_en_sqlite(csv_path: str = CSV) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(DB)
    df.to_sql("members", conn, if_exists="replace", index=False)
    conn.close()
    return

# encontrar todos los registros con numeros que tiene +62

def patron_plus62(df: pd.DataFrame) -> pd.DataFrame:
    patron = r'\+62'
    mascara = df['phone_number'].str.contains(patron, na=False)
    resultado = df[mascara][['first_name', 'last_name', 'phone_number']].copy()
    resultado['patron_encontrado'] = df.loc[mascara, 'phone_number'].str.extract(
        r'(\+62)', expand=False
    )
    
    print(f"\n {'='*60}")
    print(f"Patron 1: numeros que contienen '+62'")
    print(f"RegeEx explicado : {patron}")
    print(f"  Coincidencias  : {len(resultado):,} de {len(df):,} registros")
    print(resultado.head(10).to_string(index=False))
    return resultado

#Encontrar numeros que comienzan con parentesis y tienen guion
def patron_parentesis_guion(df: pd.DataFrame) -> pd.DataFrame:
    patron = r'^\(\d+\)\s*\d+-'
    mascara = df['phone_number'].str.contains(patron, na=False, regex=True)
    resultado = df[mascara][['first_name', 'last_name', 'phone_number']].copy()
    print(f"\n{'='*60}")
    print(f"PATRÓN 2: numeros que comienzan con (  ) y contienen guion '-'")
    print(f"  RegEx aplicado : {patron}")
    print(f"  Coincidencias  : {len(resultado):,} de {len(df):,} registros")
    print(resultado.head(10).to_string(index=False))
    return resultado
 # Encontrar todos los espacios vacios en campo numero de telefono
def patron_espacios(df: pd.DataFrame) -> pd.DataFrame:
    patron = r'\s'
    mascara = df['phone_number'].str.contains(patron, na=False)
    resultado = df[mascara][['first_name', 'last_name', 'phone_number']].copy()
    resultado['num_espacios'] = resultado['phone_number'].str.count(patron)
    resultado['sin_espacios'] = resultado['phone_number'].str.replace(

        patron, '', regex=True

    )

    print(f"\n{'='*60}")
    print(f"PATRÓN 3: numeros que contienen espacios vacios")
    print(f"  RegEx aplicado : {patron}")
    print(f"  Coincidencias  : {len(resultado):,} de {len(df):,} registros")
    print(resultado.head(10).to_string(index=False))
    return resultado  

#Guardar los resultados en el sqlite
def guardar_resultados(r1, r2, r3) -> None:
    conn = sqlite3.connect(DB)
    r1.to_sql("resultado_patron1_plus62",        conn, if_exists="replace", index=False)
    r2.to_sql("resultado_patron2_parentesis",     conn, if_exists="replace", index=False)
    r3.to_sql("resultado_patron3_espacios",       conn, if_exists="replace", index=False)
    conn.close()
    print(f"\n[OK] Resultados guardados en '{DB}':")
    print(f"     → tabla resultado_patron1_plus62      ({len(r1):,} filas)")
    print(f"     → tabla resultado_patron2_parentesis  ({len(r2):,} filas)")
    print(f"     → tabla resultado_patron3_espacios    ({len(r3):,} filas)")
 
 
# ----------------------
# EJECUCIÓN PRINCIPAL
# ----------------------
if __name__ == "__main__":
    SEPARADOR = "=" * 60
    print(SEPARADOR)
    print("  Actividad Individual  Patrones RegEx en phone_number")
    print(SEPARADOR)
    df = cargar_en_sqlite(CSV)
    r1 = patron_plus62(df)
    r2 = patron_parentesis_guion(df)
    r3 = patron_espacios(df)
    guardar_resultados(r1, r2, r3)
    print(f"\n{SEPARADOR}")
    print("  Proceso completado exitosamente.")
    print(SEPARADOR)


