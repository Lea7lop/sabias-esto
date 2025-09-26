import json
import random
import os
import datetime
import unicodedata
import re

# ---------- Función para crear slugs bonitos ----------
def slugify(text):
    if not text:
        return "curiosidad"
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text)
    return text.strip("-").lower()

# ---------- Cargar datos ----------
def cargar_datos():
    with open("data/facts.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- Guardar en JSON ----------
def guardar_curiosidades(curiosidades):
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, ensure_ascii=False, indent=2)

# ---------- Crear post ----------
def crear_post(dato, explicacion):
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(dato)
    filename = f"_posts/{fecha}-{slug}.md"

    contenido = f"""---
layout: post
title: "{dato}"
date: {fecha}
---
{explicacion}
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(contenido)

# ---------- MAIN ----------
def main():
    datos = cargar_datos()
    seleccion = random.sample(datos, 5)  # 5 aleatorios sin repetición

    # Guardar en curiosidades.json
    curiosidades = [{"dato": d["dato"], "explicacion": d["explicacion"]} for d in seleccion]
    guardar_curiosidades(curiosidades)

    # Generar posts
    os.makedirs("_posts", exist_ok=True)
    for d in seleccion:
        crear_post(d["dato"], d["explicacion"])

    print("✅ Se generaron 5 posts con explicaciones largas y JSON actualizado.")

if __name__ == "__main__":
    main()
