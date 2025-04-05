import requests
import os
import time
from requests.exceptions import RequestException

def descargar_audios_colombia():
    carpeta_salida = "audios_colombia"
    if not os.path.exists(carpeta_salida):
        print("❌ No existe la carpeta 'audios_colombia'.")
        return

    especies_carpetas = [d for d in os.listdir(carpeta_salida) if os.path.isdir(os.path.join(carpeta_salida, d))]

    if not especies_carpetas:
        print("⚠️ No hay carpetas de especies para procesar.")
        return

    print(f"📂 Se encontraron {len(especies_carpetas)} carpetas de especies.")

    url_base = "https://www.xeno-canto.org/api/2/recordings"

    for carpeta in especies_carpetas:
        especie = carpeta.replace("_", " ")
        carpeta_especie = os.path.join(carpeta_salida, carpeta)

        archivos_actuales = [f for f in os.listdir(carpeta_especie) if f.endswith(".mp3")]
        audios_existentes = set(archivos_actuales)
        total_actual = len(audios_existentes)

        if total_actual >= 15:
            print(f"✅ {especie}: ya tiene {total_actual} audios, saltando...")
            continue

        print(f"\n🔎 Buscando audios para: {especie} (actual: {total_actual}/15)")
        pagina = 1
        descargados = 0

        while total_actual < 15:
            parametros = {"query": f'cnt:Colombia "{especie}"', "page": pagina}

            try:
                resp = requests.get(url_base, params=parametros, timeout=10)
                resp.raise_for_status()
            except RequestException as e:
                print(f"❌ Error al obtener grabaciones: {e}")
                break

            datos = resp.json()
            grabaciones = datos.get("recordings", [])
            if not grabaciones:
                print("⚠️ No se encontraron más grabaciones.")
                break

            for grabacion in grabaciones:
                archivo_url = grabacion.get("file", "")
                if not archivo_url:
                    continue

                if not archivo_url.startswith("http"):
                    archivo_url = "https:" + archivo_url

                id_audio = archivo_url.split("/")[-2]
                nombre_archivo = f"{id_audio}.mp3"

                if nombre_archivo in audios_existentes:
                    continue  # Ya descargado

                ruta_archivo = os.path.join(carpeta_especie, nombre_archivo)

                # Descargar
                intentos = 0
                while intentos < 3:
                    try:
                        print(f"⬇️ Descargando {nombre_archivo} (intento {intentos+1})...")
                        audio = requests.get(archivo_url, timeout=30)
                        audio.raise_for_status()
                        with open(ruta_archivo, "wb") as f:
                            f.write(audio.content)
                        print(f"✅ Guardado en {ruta_archivo}")
                        total_actual += 1
                        descargados += 1
                        break
                    except RequestException as e:
                        print(f"⚠️ Error al descargar {archivo_url}: {e}")
                        intentos += 1
                        time.sleep(3)

                if total_actual >= 15:
                    break

                time.sleep(2)

            pagina += 1
            if pagina > int(datos.get("numPages", 1)):
                break

        print(f"🎵 Descargados {descargados} nuevos audios para {especie}.\n")

    print("🏁 Descarga completa para todas las carpetas.")

descargar_audios_colombia()
