import os
import requests
import json
from datetime import datetime

# 🔑 Cargar variables de entorno
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

def generar_curiosidades():
    prompt = (
        "Genera 5 datos curiosos diferentes, interesantes y poco conocidos. "
        "Para cada dato, escribe un título breve y una explicación larga, clara y entretenida, "
        "como si fuera para un blog de curiosidades. "
        "El resultado debe estar en formato JSON con esta estructura:\n\n"
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

    # Hugging Face puede devolver lista o dict
    if isinstance(data, list) and "generated_text" in data[0]:
        raw_text = data[0]["generated_text"]
    elif isinstance(data, dict) and "generated_text" in data:
        raw_text = data["generated_text"]
    else:
        raise ValueError(f"Respuesta inesperada del modelo: {data}")

    # Intentar parsear como JSON
    try:
        curiosidades = json.loads(raw_text)
    except:
        # fallback: limpiar texto y reintentar
        raw_text = raw_text.strip().split("\n")
        curiosidades = []
        for line in raw_text:
            if "titulo" in line.lower() or "explicacion" in line.lower():
                curiosidades.append(line)

    return curiosidades

def guardar_curiosidades(curiosidades):
    # 📂 Guardar en curiosidades.json
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(curiosidades, f, ensure_ascii=False, indent=2)

    # 📂 Guardar en _posts/ con fecha
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
