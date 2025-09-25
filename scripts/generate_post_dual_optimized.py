import os
import requests
import json
from time import sleep

# Modelos públicos y accesibles
MODEL_TITULOS = "microsoft/Phi-3-mini-128k-instruct"
MODEL_EXPLICACIONES = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"

HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

MAX_RETRIES = 3

def query_model(model_name, prompt):
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(url, headers=HEADERS, json={"inputs": prompt})
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except requests.exceptions.HTTPError as e:
            print(f"Intento {attempt} fallido para {model_name}: {e}")
            sleep(2)
    raise RuntimeError(f"No se pudo obtener respuesta del modelo {model_name} después de {MAX_RETRIES} intentos.")

def generar_curiosidades():
    curiosidades = []

    for i in range(5):
        # 1️⃣ Generar título
        prompt_titulos = "Genera un título de dato curioso interesante y llamativo."
        raw_title = query_model(MODEL_TITULOS, prompt_titulos)
        title = raw_title.strip()

        # 2️⃣ Generar explicación
        prompt_explicacion = f"Explica detalladamente el siguiente dato curioso: {title}"
        raw_explanation = query_model(MODEL_EXPLICACIONES, prompt_explicacion)
        explanation = raw_explanation.strip()

        curiosidades.append({
            "title": title,
            "explanation": explanation
        })

    return curiosidades

def guardar_json(curiosidades):
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, indent=4, ensure_ascii=False)

def main():
    print("Generando curiosidades...")
    curiosidades = generar_curiosidades()
    guardar_json(curiosidades)
    print("¡Curiosidades generadas y guardadas en curiosidades.json!")

if __name__ == "__main__":
    main()
