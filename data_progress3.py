import pandas as pd
from datetime import date
#cargar del  dataset
df = pd.read_csv("pipol_dataset.csv")

#Calcular la edad apartir de la fecha de nacimiento
df["birthday"] = pd.to_datetime(df["birthday"], dayfirst=True) 
today = date.today()
df["age"] = df["birthday"].apply(lambda b: today.year - b.year - ((today.month, today.day) < (b.month, b.day)))

print("=" * 60)
print("  AGRUPACIONES MULTINIVEL CON PANDAS")
print("=" * 60)

#Agrupar por pais y ciudad con GET_GRUOP()
#FILTRAR MEXICO / DUSTY CITY

print("\n---- Agrupacion Multinivel: Pais y Ciudad ----")
print("Grupo Mexico / Dusty City\n")
grupo_pais_ciudad = df.groupby(["country", "city"])
mexico_dusty = grupo_pais_ciudad.get_group(("Mexico", "Dusty City" ))

cols = ["name", "last_name", "age", "city", "country"]
print(mexico_dusty[cols].to_string(index=False))
print(f"\nTotal de personas en Mexico / Dusty City: {len(mexico_dusty)}")

#Edad promedio por pais con uso de .AGG() y .MEAN()
print("\n Edad Promedio por Pais con (.agg y .mean)")
#Metodo usando AGG()
edad_agg = df.groupby("country")["age"].agg(
    Promedio = "mean",
    Minima = "min",
    Maxima = "max",
    Total = "count"
).round(2)

print("Con .agg() Tenemos el resumen estadisitco de edad por pais:")
print (edad_agg.to_string())

#Usando .MEAN()
print("\n Con .mean() obtendremos solo promedio de edad por pais")
edad_mean = df.groupby("country")["age"].mean().round(2)
print(edad_mean.to_string())

#Tabla con pais y ciudad
print("\n Edad promedio por pais y ciudad")
resumen = df.groupby(["country", "city",])["age"].agg(
    Promedio = "mean",
    Personas = "count"
).round(2)
print(resumen.to_string())

print("\n "+" = " * 60)
print("Fin del analisis de agrupaciones multnivel con .agg() y .mean()")
print(" = " * 60)
