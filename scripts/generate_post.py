#!/usr/bin/env python3
# scripts/generate_post.py
import random, datetime, requests, os, re
from pathlib import Path

# ---- Config ----
CUR_DIR = Path(__file__).parent.parent
POSTS_DIR = CUR_DIR / "_posts"
IMAGES_DIR = CUR_DIR / "images"
API_URL = "https://api.deepai.org/api/text2img"
API_KEY = os.getenv("DEEP_AI_KEY")  # añadir en GitHub Secrets

curiosidades = [
    {
        "dato": "El pulpo tiene tres corazones.",
        "explicacion": "Dos bombean sangre a las branquias y uno al resto del cuerpo. Lo curioso es que el principal se detiene cuando nada."
    },
    {
        "dato": "Los plátanos son bayas, pero las frutillas no.",
        "explicacion": "Botánicamente, el plátano califica como baya simple, mientras que la frutilla es un fruto agregado."
    },
    {
        "dato": "En Júpiter y Saturno puede llover diamantes.",
        "explicacion": "La presión atmosférica es tan alta que transforma el carbono en diamantes sólidos que caen como lluvia."
    }
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    return text[:80]

def ensure_dirs():
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def generar_imagen(prompt, destino_path):
    if not API_KEY:
        print("No hay DEEP_AI_KEY en el entorno. Saltando generación de imagen.")
        return None
    try:
        resp = requests.post(API_URL, data={'text': prompt}, headers={'api-key': API_KEY}, timeout=60)
    except Exception as e:
        print("Error al conectar con la API de imagen:", e)
        return None

    if resp.status_code != 200:
        print("Error generando imagen:", resp.status_code, resp.text)
        return None

    data = resp.json()
    img_url = data.get('output_url') or (data.get('output', [{}])[0].get('url') if isinstance(data.get('output'), list) else None)
    if not img_url:
        print("No se encontró output_url en la respuesta:", data)
        return None

    try:
        r2 = requests.get(img_url, timeout=60)
        r2.raise_for_status()
        with open(destino_path, "wb") as f:
            f.write(r2.content)
        return destino_path.name
    except Exception as e:
        print("Error descargando imagen:", e)
        return None

def crear_post(dato_dict, imagen_nombre):
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0000")
    fecha_filename = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(dato_dict['dato'])
    filename = f"{fecha_filename}-{slug}.md"
    filepath = POSTS_DIR / filename
    imagen_md = f"/images/{imagen_nombre}" if imagen_nombre else ""
    contenido = f"""---
layout: post
title: "¿Sabías que {dato_dict['dato']}"
date: {fecha}
---

{dato_dict['explicacion']}

"""
    if imagen_md:
        contenido += f"![Imagen relacionada]({imagen_md})\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(contenido)

    return filepath

def main():
    ensure_dirs()
    elegido = random.choice(curiosidades)
    slug = slugify(elegido['dato'])
    fecha_short = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    nombre_img = f"{fecha_short}-{slug}.png"
    destino_img = IMAGES_DIR / nombre_img

    print("Generando imagen para:", elegido['dato'])
    imagen_generada = generar_imagen(elegido['dato'], destino_img)

    if imagen_generada:
        print("Imagen guardada en:", destino_img)
    else:
        print("No se generó imagen; el post se creará sin imagen.")

    post_file = crear_post(elegido, imagen_generada)
    print("Post creado:", post_file)

if __name__ == "__main__":
    main()
