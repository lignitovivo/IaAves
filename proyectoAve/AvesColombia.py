import requests
import os
import time
from requests.exceptions import RequestException

def descargar_audios_colombia():
    # Crear carpeta para almacenar los audios
    carpeta_salida = "audios_colombia"
    os.makedirs(carpeta_salida, exist_ok=True)

    # Parámetros de búsqueda: aves en Colombia
    url_base = "https://www.xeno-canto.org/api/2/recordings"
    parametros = {"query": "cnt:Colombia"}

    # Consultar el total de páginas
    try:
        respuesta = requests.get(url_base, params=parametros, timeout=10)
        respuesta.raise_for_status()
    except RequestException as e:
        print(f"❌ Error al conectar con la API: {e}")
        return

    datos = respuesta.json()
    total_paginas = int(datos['numPages'])
    print(f"📊 Total de páginas: {total_paginas}")

    # Iterar sobre cada página
    for pagina in range(1, total_paginas + 1):
        print(f"\n🔍 Descargando página {pagina} de {total_paginas}")
        parametros["page"] = pagina

        try:
            respuesta = requests.get(url_base, params=parametros, timeout=15)
            respuesta.raise_for_status()
        except RequestException as e:
            print(f"❌ Error al cargar la página {pagina}: {e}")
            continue

        datos = respuesta.json()
        grabaciones = datos["recordings"]
        print(f"🎵 Audios en esta página: {len(grabaciones)}")

        for grabacion in grabaciones:
            especie = grabacion["gen"] + " " + grabacion["sp"]
            archivo_url = grabacion['file']

            # Validar si la URL ya tiene "http" o agregar "https:"
            if not archivo_url.startswith("http"):
                archivo_url = "https:" + archivo_url

            # Crear carpeta por especie
            carpeta_especie = os.path.join(carpeta_salida, especie.replace(" ", "_"))
            os.makedirs(carpeta_especie, exist_ok=True)

            # Contar los archivos .mp3 en la carpeta de la especie
            archivos_existentes = [f for f in os.listdir(carpeta_especie) if f.endswith(".mp3")]
            if len(archivos_existentes) >= 11:
                print(f"⏭️ Ya hay 5 audios de {especie}, saltando...")
                continue  # Salta a la siguiente grabación

            # Generar un nombre de archivo único con la extensión .mp3
            id_audio = archivo_url.split("/")[-2]  # Obtiene el ID del audio
            nombre_archivo = os.path.join(carpeta_especie, f"{id_audio}.mp3")

            # Descargar el archivo si no existe
            if not os.path.isfile(nombre_archivo):
                intentos = 0
                exito = False
                while intentos < 3 and not exito:  # Hasta 3 reintentos
                    try:
                        print(f"⬇️ Descargando: {nombre_archivo} (Intento {intentos + 1}/3)")
                        audio = requests.get(archivo_url, timeout=30)
                        audio.raise_for_status()

                        with open(nombre_archivo, "wb") as f:
                            f.write(audio.content)

                        print(f"✅ Descarga exitosa: {nombre_archivo}")
                        exito = True
                    except RequestException as e:
                        print(f"⚠️ Error al descargar {archivo_url}: {e}")
                        intentos += 1
                        time.sleep(5)  # Esperar 5 segundos antes de reintentar

                if not exito:
                    print(f"❌ No se pudo descargar: {archivo_url} después de 3 intentos.")

                # Pausa entre descargas (para evitar bloqueos)
                time.sleep(3)

    print("\n✅ Descarga completada.")

descargar_audios_colombia()
