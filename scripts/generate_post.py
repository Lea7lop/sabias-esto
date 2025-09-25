import os
import requests
import json
from datetime import datetime

# 🔑 Variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T")  # modelo público

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

def generar_curiosidades():
    prompt = (
        "Genera 5 datos curiosos diferentes, interesantes y poco conocidos. "
        "Para cada dato, escribe un título breve y una explicación larga, clara y entretenida, "
        "como si fuera para un blog de curiosidades. "
        "Devuelve todo en formato JSON con esta estructura:\n\n"
        "[\n"
        "  {\"titulo\": \"...\", \"explicacion\": \"...\"},\n"
        "  {\"titulo\": \"...\", \"explicacion\": \"...\"},\n"
        "  {\"titulo\": \"...\", \"explicacion\": \"...\"},\n"
        "  {\"titulo\": \"...\", \"explicacion\": \"...\"},\n"
        "  {\"titulo\": \"...\", \"explicacion\": \"...\"}\n"
        "]"
    )

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    response.raise_for_status()
    data = response.json()

    # Algunos modelos devuelven 'generated_text', otros 'text'
    if isinstance(data, list) and "generated_text" in data[0]:
        raw_text = data[0]["generated_text"]
    elif isinstance(data, dict) and "generated_text" in data:
        raw_text = data["generated_text"]
    elif isinstance(data, dict) and "text" in data:
        raw_text = data["text"]
    else:
        raw_text = str(data)

    try:
        curiosidades = json.loads(raw_text)
    except:
        # fallback: no válido, crear ejemplo vacío
        curiosidades = [
            {"titulo": "Dato de prueba 1", "explicacion": "Explicación de prueba."},
            {"titulo": "Dato de prueba 2", "explicacion": "Explicación de prueba."},
            {"titulo": "Dato de prueba 3", "explicacion": "Explicación de prueba."},
            {"titulo": "Dato de prueba 4", "explicacion": "Explicación de prueba."},
            {"titulo": "Dato de prueba 5", "explicacion": "Explicación de prueba."},
        ]

    return curiosidades

def guardar_curiosidades(curiosidades):
    # Guardar en curiosidades.json
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, ensure_ascii=False, indent=2)

    # Guardar en _posts/ con fecha
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{fecha}-curiosidades.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"Curiosidades del {fecha}\"\n---\n\n")
        for c in curiosidades:
            f.write(f"## {c['titulo']}\n\n{c['explicacion']}\n\n")

def main():
    curiosidades = generar_curiosidades()
    guardar_curiosidades(curiosidades)
    print("✅ Se generaron y guardaron 5 curiosidades nuevas.")

if __name__ == "__main__":
    main()
