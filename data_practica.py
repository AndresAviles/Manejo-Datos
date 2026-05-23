import pandas as pd
import sqlite3 
# Esta libreria es empleada para el uso de expresions regulares
import re

#Funciones de transformacion ETL
# 3) Función de extracción usando RegEx (Código Postal)
def extraer_codigo_postal(df, col_origen, col_destino):
    # str.extract usando el patrón regex para buscar 5 dígitos numéricos seguidos
    patron_cp = r'(\d{5})'
    df[col_destino] = df[col_origen].str.extract(patron_cp)
    return df

# 4) Función para formatear el número de teléfono usando RegEx
def limpiar_telefono(df, col_telefono):
    # str.replace usando el patrón regex para eliminar el símbolo '+' y los paréntesis '(', ')'
    patron_tel = r'[\+\(\)]'
    df[col_telefono] = df[col_telefono].str.replace(patron_tel, '', regex=True)
    return df

# 5a) Función para mostrar la fecha de nacimiento en formato DD/MM/YYYY
def formatear_fecha_nac(df, col_fecha):
    # Convertimos a datetime y luego formateamos
    df[col_fecha] = pd.to_datetime(df[col_fecha]).dt.strftime('%d/%m/%Y')
    return df

# 5b) Función para obtener la edad en años basándose en el registro
def calcular_edad_registro(df, col_nacimiento, col_registro, col_destino):
    # Convertimos la fecha de nacimiento a datetime
    fecha_nac = pd.to_datetime(df[col_nacimiento], format='%d/%m/%Y')
    
    # La columna 'register_time' está en formato "Unix Timestamp" (segundos), la convertimos a fecha
    fecha_reg = pd.to_datetime(df[col_registro], unit='s')
    
    # Calculamos la edad (en años) que tenía la persona en el momento del registro
    df[col_destino] = (fecha_reg - fecha_nac).dt.days // 365
    return df

# ==========================================
# EJECUCIÓN DEL PROCESO ETL Y SQLITE3
# ==========================================
def main():
    print("Iniciando proceso ETL...")
    
    # 2) Utilizando el archivo "members.csv"
    try:
        df = pd.read_csv('members.csv')
    except FileNotFoundError:
        print("Error: El archivo 'members.csv' no se encuentra en el directorio.")
        return

    # Aplicando las transformaciones
    df = extraer_codigo_postal(df, 'address', 'codigo_postal')
    df = limpiar_telefono(df, 'phone_number')
    df = formatear_fecha_nac(df, 'birth_date')
    df = calcular_edad_registro(df, 'birth_date', 'register_time', 'edad_al_registro')

    print("Transformaciones completadas con éxito.")
    
    # Mostrar una muestra de los datos transformados
    print("\nMuestra de los datos transformados:")
    print(df[['address', 'codigo_postal', 'phone_number', 'birth_date', 'edad_al_registro']].head())

    # 2) Guardando en la base de datos Sqlite3
    print("\nGuardando en la base de datos SQLite3 'mlearning_db.sqlite'...")
    conexion = sqlite3.connect('mlearning_db.sqlite')
    
    # Escribir el DataFrame transformado a la tabla "members"
    df.to_sql('members_cleaned', conexion, if_exists='replace', index=False)
    
    conexion.close()
    print("Proceso finalizado y guardado exitosamente.")

if __name__ == "__main__":
    main()