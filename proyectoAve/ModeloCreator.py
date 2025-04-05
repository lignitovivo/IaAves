import os
import numpy as np
np.complex = complex  # Parche para librosa
import librosa
import pandas as pd

def extraer_perfil_acustico(carpeta_base="audios_colombia", salida_csv="perfiles_acusticos.csv"):
    perfiles = []

    for especie in os.listdir(carpeta_base):
        carpeta_especie = os.path.join(carpeta_base, especie)
        if not os.path.isdir(carpeta_especie):
            continue

        # Listas por especie
        frecuencias = []
        energias = []
        duraciones = []
        centroides = []
        mfccs_prom = []

        for archivo in os.listdir(carpeta_especie):
            if archivo.endswith(".mp3"):
                ruta_audio = os.path.join(carpeta_especie, archivo)
                try:
                    y, sr = librosa.load(ruta_audio)

                    # Duración del audio
                    duraciones.append(librosa.get_duration(y=y, sr=sr))

                    # Espectro de frecuencias
                    stft = np.abs(librosa.stft(y))
                    freqs = librosa.fft_frequencies(sr=sr)
                    energia_por_banda = stft.mean(axis=1)
                    idx_max = np.argmax(energia_por_banda)
                    frecuencia_pico = freqs[idx_max]
                    energia_total = np.sum(energia_por_banda)

                    # Centroide espectral
                    centroide = librosa.feature.spectral_centroid(y=y, sr=sr).mean()

                    # MFCCs promedio
                    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                    mfcc_mean = mfcc.mean(axis=1)  # Promedio por coeficiente

                    # Agregar valores
                    frecuencias.append(frecuencia_pico)
                    energias.append(energia_total)
                    centroides.append(centroide)
                    mfccs_prom.append(mfcc_mean)

                except Exception as e:
                    print(f"⚠️ Error procesando {archivo}: {e}")

        if frecuencias:
            mfccs_mean_final = np.mean(mfccs_prom, axis=0) if mfccs_prom else [0]*13

            perfil = {
                "especie": especie.replace("_", " "),
                "frecuencia_promedio": np.mean(frecuencias),
                "frecuencia_maxima": np.max(frecuencias),
                "frecuencia_minima": np.min(frecuencias),
                "energia_promedio": np.mean(energias),
                "duracion_promedio": np.mean(duraciones),
                "centroide_espectral": np.mean(centroides)
            }

            # Agregar MFCCs al perfil
            for i, valor in enumerate(mfccs_mean_final):
                perfil[f"mfcc_{i+1}"] = valor

            perfiles.append(perfil)

    # Crear nuevo DataFrame
    df_nuevo = pd.DataFrame(perfiles)

    # Si ya existe un CSV, unir y eliminar duplicados por especie
    if os.path.exists(salida_csv):
        df_existente = pd.read_csv(salida_csv)
        df_total = pd.concat([df_existente, df_nuevo]).drop_duplicates(subset="especie", keep="last")
    else:
        df_total = df_nuevo

    df_total.to_csv(salida_csv, index=False)
    print(f"✅ Perfil acústico actualizado en {salida_csv}")

# Ejecutar
extraer_perfil_acustico()
