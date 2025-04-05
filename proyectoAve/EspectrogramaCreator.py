'''
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def generar_espectrogramas(carpeta_base="audios_colombia", carpeta_salida="espectrogramas"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for especie in os.listdir(carpeta_base):
        carpeta_especie = os.path.join(carpeta_base, especie)
        if not os.path.isdir(carpeta_especie):
            continue

        carpeta_salida_especie = os.path.join(carpeta_salida, especie)
        os.makedirs(carpeta_salida_especie, exist_ok=True)

        for archivo in os.listdir(carpeta_especie):
            if archivo.endswith(".mp3"):
                ruta_audio = os.path.join(carpeta_especie, archivo)
                try:
                    y, sr = librosa.load(ruta_audio)
                    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
                    S_dB = librosa.power_to_db(S, ref=np.max)

                    # Crear y guardar imagen
                    plt.figure(figsize=(10, 4))
                    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
                    plt.axis('off')
                    nombre_salida = os.path.splitext(archivo)[0] + ".png"
                    ruta_salida = os.path.join(carpeta_salida_especie, nombre_salida)
                    plt.savefig(ruta_salida, bbox_inches='tight', pad_inches=0)
                    plt.close()

                    print(f"✅ Espectrograma guardado: {ruta_salida}")

                except Exception as e:
                    print(f"⚠️ Error con {archivo}: {e}")

# Ejecutar
generar_espectrogramas()
'''
'''
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generar_espectrogramas(carpeta_base="audios_colombia", carpeta_salida="espectrogramas", duracion=5.0, tamano=(224, 224)):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for especie in os.listdir(carpeta_base):
        carpeta_especie = os.path.join(carpeta_base, especie)
        if not os.path.isdir(carpeta_especie):
            continue

        carpeta_salida_especie = os.path.join(carpeta_salida, especie)
        os.makedirs(carpeta_salida_especie, exist_ok=True)

        for archivo in os.listdir(carpeta_especie):
            if archivo.endswith(".mp3"):
                ruta_audio = os.path.join(carpeta_especie, archivo)
                try:
                    # Cargar solo los primeros segundos
                    y, sr = librosa.load(ruta_audio, duration=duracion)

                    # Generar espectrograma mel
                    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
                    S_dB = librosa.power_to_db(S, ref=np.max)

                    # Graficar sin ejes
                    fig, ax = plt.subplots(figsize=(3, 3))  # Tamaño visual
                    librosa.display.specshow(S_dB, sr=sr, x_axis=None, y_axis=None, ax=ax)
                    ax.axis('off')

                    # Guardar imagen temporal
                    temp_path = "temp.png"
                    plt.savefig(temp_path, bbox_inches='tight', pad_inches=0)
                    plt.close(fig)

                    # Redimensionar y guardar la imagen final
                    img = Image.open(temp_path).convert("RGB")
                    img = img.resize(tamano)
                    nombre_salida = os.path.splitext(archivo)[0] + ".png"
                    ruta_salida = os.path.join(carpeta_salida_especie, nombre_salida)
                    img.save(ruta_salida)

                    os.remove(temp_path)  # Borrar temporal
                    print(f"✅ Espectrograma guardado: {ruta_salida}")

                except Exception as e:
                    print(f"⚠️ Error con {archivo}: {e}")

# Ejecutar
generar_espectrogramas()
'''
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generar_espectrogramas(carpeta_base="audios_colombia", carpeta_salida="espectrogramas", tamano=(224, 224)):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for especie in os.listdir(carpeta_base):
        carpeta_especie = os.path.join(carpeta_base, especie)
        if not os.path.isdir(carpeta_especie):
            continue

        carpeta_salida_especie = os.path.join(carpeta_salida, especie)
        os.makedirs(carpeta_salida_especie, exist_ok=True)

        for archivo in os.listdir(carpeta_especie):
            if archivo.endswith(".mp3"):
                ruta_audio = os.path.join(carpeta_especie, archivo)
                try:
                    # Cargar audio completo (sin límite de duración)
                    y, sr = librosa.load(ruta_audio)

                    # Generar espectrograma mel
                    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
                    S_dB = librosa.power_to_db(S, ref=np.max)

                    # Graficar sin ejes
                    fig, ax = plt.subplots(figsize=(3, 3))
                    librosa.display.specshow(S_dB, sr=sr, x_axis=None, y_axis=None, ax=ax)
                    ax.axis('off')

                    # Guardar imagen temporal
                    temp_path = "temp.png"
                    plt.savefig(temp_path, bbox_inches='tight', pad_inches=0)
                    plt.close(fig)

                    # Redimensionar y guardar la imagen final
                    img = Image.open(temp_path).convert("RGB")
                    img = img.resize(tamano)
                    nombre_salida = os.path.splitext(archivo)[0] + ".png"
                    ruta_salida = os.path.join(carpeta_salida_especie, nombre_salida)
                    img.save(ruta_salida)

                    os.remove(temp_path)
                    print(f"✅ Espectrograma guardado: {ruta_salida}")

                except Exception as e:
                    print(f"⚠️ Error con {archivo}: {e}")

# Ejecutar
generar_espectrogramas()
