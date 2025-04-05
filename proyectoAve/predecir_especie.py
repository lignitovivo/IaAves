import numpy as np
import librosa
import joblib
import sys

# Cargar modelo y codificador
modelo = joblib.load("modelo_aves.pkl")
codificador = joblib.load("codificador_etiquetas.pkl")

def extraer_caracteristicas(audio_path):
    y, sr = librosa.load(audio_path, duration=10.0)  # límite de duración si el audio es muy largo

    # Características
    duracion = librosa.get_duration(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = mfcc.mean(axis=1)

    centroides = librosa.feature.spectral_centroid(y=y, sr=sr)
    centroides_mean = centroides.mean()

    stft = np.abs(librosa.stft(y))
    energia_por_banda = stft.mean(axis=1)
    freqs = librosa.fft_frequencies(sr=sr)
    frecuencia_pico = freqs[np.argmax(energia_por_banda)]
    energia_total = np.sum(energia_por_banda)

    # Vector final de características
    caracteristicas = np.concatenate([
        [duracion, frecuencia_pico, energia_total, centroides_mean],
        mfcc_mean
    ])

    return caracteristicas.reshape(1, -1)

# Ruta del audio a predecir
if len(sys.argv) < 2:
    print("❗ Proporciona la ruta del audio como argumento. Ejemplo:\npython predecir_especie.py nuevo_audio.mp3")
    sys.exit(1)

ruta_audio = sys.argv[1]

# Extraer características y predecir
try:
    X_nuevo = extraer_caracteristicas(ruta_audio)
    prediccion = modelo.predict(X_nuevo)
    especie = codificador.inverse_transform(prediccion)[0]
    print(f"🕊️ El audio corresponde a la especie: {especie}")
except Exception as e:
    print(f"⚠️ Error al analizar el audio: {e}")
