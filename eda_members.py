import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#cargar conjunto de datos de seaborn
df = sns.load_dataset("titanic")

# inspeccion de datos
print("Primeras 5 filas del dataset")
print(df.head())

print("Informacion general")
print(df.info())

print("Estadisticas descriptivas")
print(df.describe())

# limpieza de datos, detectar valores nulos

print("\n Conteo de valores nulos por cada columno")
print(df.isnull().sum())

# Graficar los datos con analisis univariado
plt.figure(figsize=(8,5))
sns.histplot(df['age'].dropna(), kde=True, color='teal', bins=30)
plt.title('Distribucion de edades en el Titanic')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.show()

# Graficar con analisis bivariadio
plt.figure(figsize=(8,5))
sns.countplot(data=df, x='pclass', hue='survived', palette='Set2')
plt.title('Supervivencia por clase de pasajero')
plt.xlabel('Clase (1= Alta, 2 = Media, 3 = Baja)')
plt.ylabel('Cantidad de pasajeros')
plt.legend(title='Sobrevivio?', label=['No','Si'])
plt.show()

# Graficacion con analisis multivariado
numeric_cols = df.select_dtypes(include=['float64, int64'])
plt.figure(figsize=(8,6))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlacion entre variables numericas')
plt.show()

