import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import uuid

# Cargar modelo entrenado
modelo = tf.keras.models.load_model("modelo_espectrogramas_cnn.keras")

# Obtener nombres de clases
class_names = sorted(os.listdir("espectrogramas"))

def generar_espectrograma(audio_path, img_path, size=(128, 128)):
    y, sr = librosa.load(audio_path, sr=None)
    plt.figure(figsize=(2.56, 2.56), dpi=50)
    plt.axis('off')
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_DB, sr=sr, cmap='magma')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def predecir_especie(audio_path):
    temp_name = f"temp_{uuid.uuid4().hex}.png"
    generar_espectrograma(audio_path, temp_name)

    # Preprocesar imagen
    img = image.load_img(temp_name, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predecir
    pred = modelo.predict(img_array)
    clase_predicha = np.argmax(pred)
    os.remove(temp_name)  # Borrar archivo temporal

    return class_names[clase_predicha]

# ========= USO =========
ruta_audio = "audioPrueba/audio1.mp3"  # puede ser .wav o .mp3
especie = predecir_especie(ruta_audio)
print(f"🔊 El modelo predice que el ave es: {especie}")
