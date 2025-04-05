import pandas as pd

# Carga tu archivo CSV
df = pd.read_csv('perfiles_acusticos.csv')  # Cambia esto si ya tienes el DataFrame

# Ver cuántas muestras hay por especie
conteo_especies = df['especie'].value_counts()
print(conteo_especies)
