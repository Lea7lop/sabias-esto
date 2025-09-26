#!/usr/bin/env python3
import os, json, random, datetime, unicodedata, textwrap

# Config
FACTS_FILE = "data/facts.json"
HIST_PUBLIC = "public/curiosidades.json"
HIST_ROOT = "curiosidades.json"
POSTS_DIR = "_posts"
NUM_NEW = 5

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs("public", exist_ok=True)

# Utilidades
def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    for ch in [' ', '/', '\\', '"', "'", ":", ";", ",", "(", ")", "?" , "¿", "¡", "!", "."]:
        text = text.replace(ch, "-")
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")[:80]

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S +0000")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# Generador de explicación larga (plantillas + variación)
def expand_explanation(base_short):
    parts = []
    # Primera frase: la base como introducción
    intro = base_short.strip().rstrip(".") + "."
    parts.append(intro)

    connectors = [
        "Esto ocurre principalmente porque",
        "En términos sencillos, significa que",
        "Además, conviene destacar que",
        "Un ejemplo práctico es que",
        "Como consecuencia,",
        "Históricamente se ha observado que",
        "Es interesante saber que"
    ]

    facts_detail = [
        "involucra procesos biológicos y estructurales que explican su funcionamiento",
        "se relaciona con adaptaciones que mejoran la supervivencia",
        "está influenciado por factores ambientales y evolutivos",
        "tiene implicaciones en cómo estos organismos interactúan con su entorno",
        "se explica por la anatomía y fisiología específicas de la especie"
    ]

    examples = [
        "la alimentación y comportamiento",
        "la regulación térmica",
        "la movilidad y el desplazamiento",
        "la polinización y dispersión de semillas",
        "la protección frente a depredadores"
    ]

    templates = [
        "{conn} {detail}.",
        "{conn} {detail}, y por eso {example}.",
        "{conn} {detail}. Además, {extra}.",
        "{conn} {detail}, lo cual resulta en {example}."
    ]

    extras = [
        "esto ha sido estudiado por biólogos marinos y fisiólogos",
        "los científicos usan modelos y observaciones para entender mejor este fenómeno",
        "estudiarlo ayuda a comprender procesos más grandes en la naturaleza"
    ]

    # Generar 3 frases adicionales
    for _ in range(3):
        conn = random.choice(connectors)
        temp = random.choice(templates)
        detail = random.choice(facts_detail)
        example = random.choice(examples)
        extra = random.choice(extras)
        phrase = temp.format(conn=conn, detail=detail, example=example, extra=extra)
        parts.append(phrase)

    # Cierre
    parts.append("Si te interesa saber más, investigar este tema revela conexiones fascinantes entre la naturaleza y la ciencia.")

    texto = " ".join(parts)
    return textwrap.fill(texto, width=100)

# MAIN
def main():
    facts = load_json(FACTS_FILE)
    if not facts:
        print("ERROR: data/facts.json no encontrado o vacío.")
        return

    historico = load_json(HIST_PUBLIC)  # historial
    usados = set([h.get("dato") for h in historico if h.get("dato")])

    candidatos = [f for f in facts if f.get("dato") not in usados]
    random.shuffle(candidatos)

    nuevos = []
    idx = 0
    # Si no hay suficientes nuevos candidatos, te avisamos y usamos reposición controlada
    while len(nuevos) < NUM_NEW:
        if idx < len(candidatos):
            f = candidatos[idx]
            idx += 1
        else:
            # si ya no quedan nuevos, tomar aleatorio de todos (pero evitar duplicados dentro de esta ejecución)
            f = random.choice(facts)
            if f.get("dato") in [n["dato"] for n in nuevos]:
                continue

        dato = f.get("dato")
        base = f.get("explicacion", "")
        explicacion_larga = expand_explanation(base)
        fecha = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        slug = slugify(dato)
        filename = f"{POSTS_DIR}/{fecha}-{slug}.md"
        md_date = now_iso()
        contenido = f"""---
layout: post
title: "¿Sabías que {dato}?"
date: {md_date}
---

{explicacion_larga}

"""
        with open(filename, "w", encoding="utf-8") as ff:
            ff.write(contenido)

        entry = {"dato": dato, "explicacion": explicacion_larga, "date": md_date}
        historico.insert(0, entry)
        nuevos.append(entry)
        print("Creado:", filename)

    # Guardar histórico (tanto en public como copia raíz para index.html)
    save_json(historico, HIST_PUBLIC)
    save_json(historico, HIST_ROOT)

    print(f"✅ Se generaron {len(nuevos)} datos curiosos nuevos y se actualizó {HIST_PUBLIC}.")

if __name__ == "__main__":
    main()
    
