import os
import requests
import json
import time

# --- CONFIGURACIÓN ---
HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
MAX_RETRIES = 3

# Modelos que funcionan con API
MODEL_TITULOS = "microsoft/Phi-3-mini-4k-instruct"
MODEL_EXPLICACION = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"

# Número de curiosidades a generar
NUM_CURIOSIDADES = 5

# --- FUNCIONES ---
def query_model(model_name, prompt):
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    for intento in range(1, MAX_RETRIES + 1):
        response = requests.post(url, headers=HEADERS, json={"inputs": prompt})
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            return data
        else:
            print(f"Intento {intento} fallido para {model_name}: {response.status_code} {response.reason}")
            time.sleep(2)
    raise RuntimeError(f"No se pudo obtener respuesta del modelo {model_name} después de {MAX_RETRIES} intentos.")

def generar_curiosidades():
    curiosidades = []
    for i in range(NUM_CURIOSIDADES):
        prompt_titulos = "Genera un dato curioso interesante y breve sobre cualquier tema."
        raw_title = query_model(MODEL_TITULOS, prompt_titulos)

        # Enriquecemos con explicación larga usando segundo modelo
        prompt_explicacion = f"Explica con detalle y de forma entretenida este dato curioso: {raw_title}"
        raw_explicacion = query_model(MODEL_EXPLICACION, prompt_explicacion)

        curiosidades.append({
            "titulo": raw_title.strip(),
            "explicacion": raw_explicacion.strip()
        })
        print(f"Curiosidad {i+1} generada.")
    return curiosidades

def guardar_curiosidades(curiosidades):
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, indent=2, ensure_ascii=False)
    print("Curiosidades guardadas en curiosidades.json")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    print("Generando curiosidades...")
    curiosidades = generar_curiosidades()
    guardar_curiosidades(curiosidades)
