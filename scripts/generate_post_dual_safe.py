import os
import requests
import json
from datetime import datetime
import time

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_TITULOS = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
MODEL_EXPLICACIONES = "microsoft/Phi-3-mini-4k-instruct"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

MAX_RETRIES = 3
WAIT_SECONDS = 5

def query_model(model_name, prompt):
    """Enviar prompt al modelo y devolver texto generado con reintentos"""
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url, headers=HEADERS, json={"inputs": prompt, "options":{"wait_for_model":True}})
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            elif isinstance(data, dict) and "text" in data:
                return data["text"]
            else:
                return str(data)
        except Exception as e:
            print(f"Intento {attempt+1} fallido para {model_name}: {e}")
            time.sleep(WAIT_SECONDS)
    raise RuntimeError(f"No se pudo obtener respuesta del modelo {model_name} después de {MAX_RETRIES} intentos.")

def generar_curiosidades():
    # 1️⃣ Generar títulos con TinyLlama
    prompt_titulos = (
        "Genera 5 títulos cortos y originales para datos curiosos, "
        "interesantes y poco conocidos. Devuélvelos en JSON: [\"titulo1\", \"titulo2\", \"titulo3\", \"titulo4\", \"titulo5\"]"
    )
    raw_titles = query_model(MODEL_TITULOS, prompt_titulos)
    try:
        titles = json.loads(raw_titles)
    except:
        print("No se pudieron parsear títulos, usando fallback de prueba.")
        titles = [f"Curiosidad de prueba {i+1}" for i in range(5)]

    curiosidades = []
    # 2️⃣ Generar explicaciones con Phi-3
    for title in titles:
        prompt_exp = (
            f"Escribe una explicación larga, clara y entretenida para un dato curioso con el título: '{title}'. "
            "Devuelve un JSON con {\"titulo\": \"...\", \"explicacion\": \"...\"}"
        )
        raw_exp = query_model(MODEL_EXPLICACIONES, prompt_exp)
        try:
            exp = json.loads(raw_exp)
            curiosidades.append(exp)
        except:
            print(f"No se pudo parsear explicación para '{title}', usando texto crudo.")
            curiosidades.append({"titulo": title, "explicacion": raw_exp.strip()})

    return curiosidades

def guardar_curiosidades(curiosidades):
    # Guardar en JSON
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, ensure_ascii=False, indent=2)

    # Guardar en _posts/ para Jekyll
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{fecha}-curiosidades.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"Curiosidades del {fecha}\"\n---\n\n")
        for c in curiosidades:
            f.write(f"## {c['titulo']}\n\n{c['explicacion']}\n\n")

def main():
    curiosidades = generar_curiosidades()
    guardar_curiosidades(curiosidades)
    print("✅ Se generaron y guardaron 5 curiosidades nuevas con dos modelos de forma segura.")

if __name__ == "__main__":
    main()

