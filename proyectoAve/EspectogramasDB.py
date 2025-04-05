import os
import shutil

# Carpeta original
origen = "espectrogramas"
# Nueva carpeta con clases suficientes
destino = "espectrogramas_filtrados"

# Mínimo de imágenes por clase
minimo = 20

# Crear carpeta destino si no existe
os.makedirs(destino, exist_ok=True)

for especie in os.listdir(origen):
    ruta_clase = os.path.join(origen, especie)
    if os.path.isdir(ruta_clase):
        cantidad = len([f for f in os.listdir(ruta_clase) if f.endswith(('.png', '.jpg', '.jpeg'))])
        if cantidad >= minimo:
            shutil.copytree(ruta_clase, os.path.join(destino, especie), dirs_exist_ok=True)
            print(f"Copiada: {especie} ({cantidad} imágenes)")
