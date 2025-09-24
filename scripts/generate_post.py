import random, datetime, requests, os, json

# Lista de datos curiosos con explicación más larga
curiosidades = [
    {
        "dato": "El pulpo tiene tres corazones.",
        "explicacion": "Dos bombean sangre a las branquias y uno al resto del cuerpo. Lo curioso es que el principal se detiene cuando nada, lo que hace que nadar sea más costoso energéticamente para ellos."
    },
    {
        "dato": "Los plátanos son bayas, pero las frutillas no.",
        "explicacion": "Botánicamente, el plátano califica como baya simple, mientras que la frutilla es un fruto agregado formado por múltiples ovarios de la misma flor."
    },
    {
        "dato": "En Júpiter y Saturno puede llover diamantes.",
        "explicacion": "La presión atmosférica es tan alta que transforma el carbono en diamantes sólidos que caen como lluvia, un fenómeno que no ocurre en la Tierra."
    }
]

# Carpeta pública
os.makedirs("public/images", exist_ok=True)

curiosidades_json = []

# Hugging Face API
api_url = "https://api-inference.huggingface.co/models/hogiahien/counterfeit-v30-edited"
api_key = os.getenv("HF_API_KEY")  # Tu token de Hugging Face en GitHub Secrets

headers = {"Authorization": f"Bearer {api_key}"}

for _ in range(5):
    c = random.choice(curiosidades)
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = c["dato"].lower().replace(" ", "-").replace("¿","").replace("?","").replace(".","")
    
    nombre_archivo = f"_posts/{fecha}-{slug}.md"
    nombre_imagen = f"public/images/{fecha}-{slug}.png"

    # Generar imagen
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": c["dato"]})
        if response.status_code == 200:
            img_data = response.content
            with open(nombre_imagen, "wb") as f:
                f.write(img_data)
        else:
            print(f"No se generó imagen para {c['dato']}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error al generar imagen: {e}")

    # Crear Markdown
    contenido = f"""---
layout: post
title: "¿Sabías que {c['dato']}?"
date: {fecha}
---

{c['explicacion']*2}

![Imagen relacionada](/images/{fecha}-{slug}.png)
"""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    # JSON
    curiosidades_json.append({
        "dato": c["dato"],
        "explicacion": c["explicacion"]*2,
        "imagen": f"images/{fecha}-{slug}.png"
    })

# Guardar JSON
with open("public/curiosidades.json", "w", encoding="utf-8") as f:
    json.dump(curiosidades_json, f, ensure_ascii=False, indent=2)

print("Se generaron 5 posts con imágenes y JSON actualizado.")
