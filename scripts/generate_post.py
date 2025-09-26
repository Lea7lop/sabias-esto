#!/usr/bin/env python3
import os
import json
import random
import datetime
import unicodedata

# ---------- Config ----------
MAX_NEW = 5
POSTS_DIR = "_posts"
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs("public", exist_ok=True)

OUTPUT_JSON_PUBLIC = "public/curiosidades.json"
OUTPUT_JSON_ROOT = "curiosidades.json"

# ---------- Utilidades ----------
def slugify(text):
    if not text:
        return "sin-dato"
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    for ch in [' ', '/', '\\', '"', "'", ":", ";", ",", "(", ")", "?" , "¿", "¡", "!", "."]:
        text = text.replace(ch, "-")
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")[:80]

def now_utc_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")

# ---------- Datos curiosos base ----------
DATOS_BASE = [
    {
        "dato": "El pulpo tiene tres corazones",
        "explicacion": (
            "Dos bombean sangre a las branquias y uno al resto del cuerpo. "
            "El corazón principal se detiene cuando nada, lo que ayuda a conservar energía. "
            "Su sangre es azul por la hemocianina, que permite transportar oxígeno en aguas frías."
        )
    },
    {
        "dato": "Los plátanos son bayas pero las frutillas no",
        "explicacion": (
            "Botánicamente, el plátano es una baya simple porque se desarrolla a partir de un solo ovario. "
            "La frutilla es un fruto agregado formado por varios ovarios de la misma flor. "
            "Esta diferencia científica suele sorprender a muchas personas."
        )
    },
    {
        "dato": "En Júpiter y Saturno puede llover diamantes",
        "explicacion": (
            "La presión atmosférica en estos planetas es tan alta que el carbono se cristaliza en diamantes sólidos "
            "que caen como lluvia. Este fenómeno demuestra cómo las condiciones extremas pueden crear minerales "
            "de formas inesperadas en otros mundos."
        )
    },
    {
        "dato": "La miel nunca se echa a perder",
        "explicacion": (
            "Gracias a su bajo contenido de agua y alta acidez, la miel puede durar siglos sin estropearse. "
            "Se han encontrado tarros de miel comestible en tumbas egipcias de más de 3000 años."
        )
    },
    {
        "dato": "Las abejas tienen cinco ojos",
        "explicacion": (
            "Tienen dos ojos compuestos grandes y tres ojos simples pequeños en la parte superior de la cabeza. "
            "Estos ojos les ayudan a detectar luz, movimiento y orientación mientras vuelan."
        )
    },
    {
        "dato": "Los gatos tienen más huesos en la cola que los humanos",
        "explicacion": (
            "Los gatos poseen entre 19 y 23 huesos en la cola, mientras que los humanos solo tienen un grupo de huesos fusionados (cóccix). "
            "Esto les da gran flexibilidad para el equilibrio y la comunicación mediante movimientos de cola."
        )
    }
]

# ---------- Funciones ----------
def cargar_historico(path):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_historico(hist, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

# ---------- MAIN ----------
def main():
    historico = cargar_historico(OUTPUT_JSON_PUBLIC)
    existentes = set([h.get("dato") for h in historico if h.get("dato")])

    nuevos = []
    intentos = 0
    MAX_INTENTOS = 20

    while len(nuevos) < MAX_NEW and intentos < MAX_INTENTOS:
        intentos += 1
        c = random.choice(DATOS_BASE)
        dato = c["dato"]
        explicacion = c["explicacion"]

        if not dato or dato in existentes:
            continue

        now_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        slug = slugify(dato)
        filename = f"{POSTS_DIR}/{now_date}-{slug}.md"
        md_date = now_utc_iso()
        contenido = f"""---
layout: post
title: "¿Sabías que {dato}?"
date: {md_date}
---

{explicacion}

"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(contenido)

        entry = {"dato": dato, "explicacion": explicacion, "date": md_date}
        historico.insert(0, entry)
        existentes.add(dato)
        nuevos.append(entry)
        print("Creado:", filename)

    guardar_historico(historico, OUTPUT_JSON_PUBLIC)
    guardar_historico(historico, OUTPUT_JSON_ROOT)

    if nuevos:
        print(f"✅ Se generaron {len(nuevos)} datos curiosos nuevos.")
    else:
        print("⚠️ No se generaron datos nuevos (intenta limpiar el histórico si todos ya existen).")

if __name__ == "__main__":
    main()
