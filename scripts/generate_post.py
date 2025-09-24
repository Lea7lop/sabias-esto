#!/usr/bin/env python3
import os
import time
import json
import requests
import datetime
import unicodedata

# ---------- Config ----------
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_ENV_NAME = "HF_API_KEY"  # nombre del secret en GitHub
MAX_NEW = 5
MAX_INTENTOS = 60
OUTPUT_JSON_PUBLIC = "public/curiosidades.json"
OUTPUT_JSON_ROOT = "curiosidades.json"
POSTS_DIR = "_posts"
os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs("public", exist_ok=True)

# ---------- Utilidades ----------
def slugify(text):
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

# ---------- Histórico (evitar repetidos) ----------
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

# ---------- Generador (Hugging Face) ----------
def generar_con_hf(prompt, headers, max_retries=3, wait=1):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 120, "temperature": 0.8}}
    for intento in range(max_retries):
        try:
            resp = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        except Exception as e:
            last_err = e
            time.sleep(wait)
            continue
        if resp.status_code == 200:
            try:
                data = resp.json()
                # respuesta común: [{'generated_text': '...'}]
                if isinstance(data, list) and len(data) and "generated_text" in data[0]:
                    return data[0]["generated_text"].strip()
                # algunos modelos/dev returns text in other format:
                if isinstance(data, dict) and "generated_text" in data:
                    return data["generated_text"].strip()
                # fallback: if API returns plain text (rare)
                try:
                    return resp.text.strip()
                except:
                    return None
            except ValueError:
                # si no es JSON, puede ser texto
                return resp.text.strip()
        else:
            last_err = f"{resp.status_code} {resp.text}"
            time.sleep(wait)
    # si falla
    print("ERROR HF:", last_err)
    return None

# ---------- Prompt (formato claro para parseo) ----------
PROMPT_TEMPLATE = (
    "Genera UN ÚNICO dato curioso en español en una sola frase (máx ~20 palabras), "
    "seguido exactamente por '||' y a continuación una explicación clara y didáctica de 2-3 oraciones. "
    "Devuelve únicamente: DATO||EXPLICACIÓN (sin texto extra). Ejemplo: "
    "Los plátanos son bayas||Explicación corta..."
)

# ---------- MAIN ----------
def main():
    hf_key = os.getenv(HF_ENV_NAME)
    if not hf_key:
        print(f"ERROR: no se encontró la variable de entorno {HF_ENV_NAME}. Añádela en GitHub Secrets.")
        return

    headers = {"Authorization": f"Bearer {hf_key}"}
    historico = cargar_historico(OUTPUT_JSON_PUBLIC)  # usamos public como histórico principal
    existentes = set([h.get("dato") for h in historico if h.get("dato")])

    nuevos = []
    intentos = 0

    while len(nuevos) < MAX_NEW and intentos < MAX_INTENTOS:
        intentos += 1
        salida = generar_con_hf(PROMPT_TEMPLATE, headers, max_retries=3, wait=1)
        if not salida:
            continue

        # parseo por '||'
        if "||" in salida:
            dato, explicacion = salida.split("||", 1)
            dato = dato.strip().rstrip(".")
            explicacion = explicacion.strip()
        else:
            # fallback: separar por primer punto y espacio
            if ". " in salida:
                dato, explicacion = salida.split(". ", 1)
                dato = dato.strip().rstrip(".")
                explicacion = explicacion.strip()
            else:
                # si no se puede parsear, ignorar
                continue

        if not dato or dato in existentes:
            # repetido o inválido
            continue

        # ok: nuevo
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
        # escribir .md
        with open(filename, "w", encoding="utf-8") as f:
            f.write(contenido)

        entry = {"dato": dato, "explicacion": explicacion, "date": md_date}
        historico.insert(0, entry)  # insertar al inicio
        existentes.add(dato)
        nuevos.append(entry)
        print("Creado:", filename)

    # guardar histórico en public y también copia raíz para compatibilidad con index.html
    guardar_historico(historico, OUTPUT_JSON_PUBLIC)
    guardar_historico(historico, OUTPUT_JSON_ROOT)

    if nuevos:
        print(f"✅ Se generaron {len(nuevos)} datos curiosos nuevos.")
    else:
        print("⚠️ No se generaron datos nuevos (intenta aumentar MAX_INTENTOS o revisar el token/API).")

if __name__ == "__main__":
    main()
    
