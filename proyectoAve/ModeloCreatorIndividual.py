import os
import numpy as np
np.complex = complex  # Parche para librosa
import librosa
import pandas as pd

def extraer_perfil_acustico_por_audio(carpeta_base="audios_colombia", salida_csv="perfiles_individuales.csv"):
    perfiles = []

    for especie in os.listdir(carpeta_base):
        carpeta_especie = os.path.join(carpeta_base, especie)
        if not os.path.isdir(carpeta_especie):
            continue

        for archivo in os.listdir(carpeta_especie):
            if archivo.endswith(".mp3"):
                ruta_audio = os.path.join(carpeta_especie, archivo)
                try:
                    y, sr = librosa.load(ruta_audio)
                    duracion = librosa.get_duration(y=y, sr=sr)
                    stft = np.abs(librosa.stft(y))
                    freqs = librosa.fft_frequencies(sr=sr)
                    energia_por_banda = stft.mean(axis=1)
                    idx_max = np.argmax(energia_por_banda)
                    frecuencia_pico = freqs[idx_max]
                    energia_total = np.sum(energia_por_banda)
                    centroide = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
                    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                    mfcc_mean = mfcc.mean(axis=1)

                    perfil = {
                        "archivo": archivo,
                        "ruta_audio": ruta_audio,
                        "especie": especie.replace("_", " "),
                        "frecuencia_pico": frecuencia_pico,
                        "energia_total": energia_total,
                        "duracion": duracion,
                        "centroide_espectral": centroide
                    }

                    for i, valor in enumerate(mfcc_mean):
                        perfil[f"mfcc_{i+1}"] = valor

                    perfiles.append(perfil)

                except Exception as e:
                    print(f"⚠️ Error procesando {archivo}: {e}")

    df = pd.DataFrame(perfiles)
    df.to_csv(salida_csv, index=False)
    print(f"✅ Perfiles individuales guardados en {salida_csv}")
