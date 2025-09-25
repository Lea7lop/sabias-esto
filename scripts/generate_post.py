#!/usr/bin/env python3
"""
Genera 5 datos curiosos usando Hugging Face Inference API y los guarda:
- _posts/YYYY-MM-DD-slug.md
- curiosidades.json
"""

import os, requests, json, time, random, re, datetime

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise SystemExit("ERROR: HF_TOKEN no encontrado en variables de entorno.")

MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
API = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

random.seed()

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9áéíóúñ]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:60]

def call_hf(prompt, max_new_tokens=700, temperature=0.7):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": 0.95
        },
        "options": {"wait_for_model": True}
    }
    r = requests.post(API, headers=HEADERS, json=payload, timeout=180)
    if r.status_code != 200:
        raise Exception(f"Hugging Face API error {r.status_code}: {r.text}")
    data = r.json()
    if isinstance(data, list):
        text = "".join([d.get("generated_text","") for d in data])
    elif isinstance(data, dict) and "generated_text" in data:
        text = data["generated_text"]
    else:
        text = json.dumps(data)
    return text.strip()

def extract_json(text):
    m = re.search(r'(\{.*\})', text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

CATEGORIES = [
    "Historia", "Ciencia", "Tecnología", "Arte", "Geografía",
    "Biología", "Astronomía", "Inventos", "Cultura", "Deportes"
]

def make_prompt(category):
    return (
        "Eres un redactor experto que genera 'datos curiosos' para un blog educativo. "
        "Genera **UN** dato curioso único sobre el tema: " + category + ".\n\n"
        "Salva la salida EXACTAMENTE en formato JSON con estas claves:\n"
        "  - title (string, <100 chars)\n"
        "  - body (string, EXPLICACIÓN LARGA y detallada, mínimo 250 palabras)\n"
        "  - tags (lista de strings, 3-6 etiquetas)\n"
        "  - image_prompt (string, descripción breve para la imagen sugerida)\n"
        "  - source (string, fuente breve si la conoces o '' si no)\n\n"
        "IMPORTANTE: devuelve SOLO JSON válido (sin texto extra)."
    )

def ensure_unique_title(ti
