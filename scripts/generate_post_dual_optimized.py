import os
import requests
import json
from datetime import datetime
import time

# 🔑 Variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")

# Modelos seguros
MODEL_TITULOS = "microsoft/Phi-3-mini-4k-instruct"
MODEL_EXPLICACIONES = "microsoft/Phi-3.5-mini-instruct"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
MAX_RETRIES = 3
WAIT_SECONDS = 2

def query_model(model_name, prompt):
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    for attempt in range(1, MAX_RETRIES+1):
        try:
            response = requests.post(url, headers=HEADERS, json={"inputs": prompt})
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            else:
                raise ValueError(f"Respuesta inesperada del modelo {model_name}: {data}")
        except Exception as e:
            print(f"Intento {attempt} fallido para {model_name}: {e}")
            time.sleep(WAIT_SECONDS)
    raise RuntimeError(f"No se pudo obtener respuesta del modelo {model_name} después de {MAX_RETRIES} intentos.")

def generar_curiosidades():
    # 1️⃣ Generar títulos y breve explicación
    prompt_titulos = (
        "Genera 5 títulos cortos y llamativos para datos curiosos, "
        "y junto a cada título escribe una breve explicación de 2-3 líneas, "
        "separados por líneas nuevas.\n"
        "(Ejemplo: 'La abeja que reconoce caras: Las abejas pueden distinguir rostros humanos, lo que demuestra su capacidad cognitiva.')"
    )
    raw = query_model(MODEL_TITULOS, prompt_titulos)
    lineas = [line.strip() for line in raw.split("\n") if line.strip()]
    
    curiosidades = []
    for linea in lineas[:5]:
        if ':' in linea:
            titulo, breve_exp = linea.split(":", 1)
        else:
            titulo = linea
            breve_exp = ""
        curiosidades.append({"titulo": titulo.strip(), "breve_exp": breve_exp.strip()})

    # 2️⃣ Expandir explicaciones con el segundo modelo
    for c in curiosidades:
        prompt_exp = (
            f"Título: {c['titulo']}\n"
            f"Explicación breve: {c['breve_exp']}\n\n"
            "Genera ahora una explicación larga, clara y entretenida, lista para un blog de curiosidades:"
        )
        c['explicacion'] = query_model(MODEL_EXPLICACIONES, prompt_exp).strip()
        del c['breve_exp']  # eliminar la breve explicación

    return curiosidades

def guardar_curiosidades(curiosidades):
    # Guardar JSON
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, ensure_ascii=False, indent=2)

    # Guardar Markdown en _posts/
    fecha = datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{fecha}-curiosidades.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"---\nlayout: post\ntitle: \"Curiosidades del {fecha}\"\n---\n\n")
        for c in curiosidades:
            f.write(f"## {c['titulo']}\n\n{c['explicacion']}\n\n")

def main():
    curiosidades = generar_curiosidades()
    guardar_curiosidades(curiosidades)
    print("✅ Se generaron y guardaron 5 curiosidades largas y coherentes.")

if __name__ == "__main__":
    main()
