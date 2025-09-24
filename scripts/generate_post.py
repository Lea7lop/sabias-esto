import random, datetime, requests, os, json

# Lista de datos curiosos con explicaciones largas
curiosidades = [
    {
        "dato": "El pulpo tiene tres corazones.",
        "explicacion": (
            "Dos bombean sangre a las branquias y uno al resto del cuerpo. "
            "El corazón principal se detiene cuando nada, lo que ayuda a conservar energía. "
            "Su sangre es azul por la hemocianina, lo que permite transportar oxígeno en aguas frías."
        )
    },
    {
        "dato": "Los plátanos son bayas, pero las frutillas no.",
        "explicacion": (
            "Botánicamente, el plátano es una baya simple porque se desarrolla a partir de un solo ovario. "
            "La frutilla es un fruto agregado formado por varios ovarios de la misma flor, lo que la hace diferente. "
            "Esta diferencia científica suele sorprender a muchas personas."
        )
    },
    {
        "dato": "En Júpiter y Saturno puede llover diamantes.",
        "explicacion": (
            "La presión atmosférica en estos planetas es tan alta que el carbono se cristaliza en diamantes sólidos "
            "que caen como lluvia. Este fenómeno demuestra cómo las condiciones extremas pueden crear minerales "
            "de formas inesperadas en otros mundos."
        )
    }
]

# Carpeta pública para imágenes
os.makedirs("public/images", exist_ok=True)

# Lista para JSON
curiosidades_json = []

# Token y URL de Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def generar_imagen(prompt, path):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
        return True
    else:
        print("Error al generar imagen:", response.status_code, response.text)
        return False

# Generar 5 posts
for _ in range(5):
    c = random.choice(curiosidades)
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = c["dato"].lower().replace(" ", "-").replace("¿","").replace("?","").replace(".","")

    nombre_archivo = f"_posts/{fecha}-{slug}.md"
    nombre_imagen = f"public/images/{fecha}-{slug}.png"

    # Generar imagen
    generar_imagen(c["dato"], nombre_imagen)

    # Crear post Markdown
    contenido = f"""---
layout: post
title: "¿Sabías que {c['dato'].lower()}?"
date: {fecha}
---

{c['explicacion']}

![Imagen relacionada](/images/{fecha}-{slug}.png)
"""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    # Agregar al JSON
    curiosidades_json.append({
        "dato": c["dato"],
        "explicacion": c["explicacion"],
        "imagen": f"images/{fecha}-{slug}.png"
    })

# Guardar JSON
with open("public/curiosidades.json", "w", encoding="utf-8") as f:
    json.dump(curiosidades_json, f, ensure_ascii=False, indent=2)

print("Se generaron 5 posts con imágenes y JSON actualizado.")
