import random, datetime, requests, os, json

# --------------------------
# Lista de curiosidades con explicación más larga
# --------------------------
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

# --------------------------
# Crear carpeta pública para imágenes
# --------------------------
os.makedirs("public/images", exist_ok=True)

# --------------------------
# Configuración Hugging Face
# --------------------------
api_url = "https://api-inference.huggingface.co/models/hogiahien/counterfeit-v30-edited"
api_key = os.getenv("HF_API_KEY")  # Token guardado en GitHub Secrets
headers = {"Authorization": f"Bearer {api_key}"}

curiosidades_json = []

# --------------------------
# Generar 5 posts
# --------------------------
for _ in range(5):
    c = random.choice(curiosidades)
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = c["dato"].lower().replace(" ", "-").replace("¿","").replace("?","").replace(".","")
    
    nombre_archivo = f"_posts/{fecha}-{slug}.md"
    nombre_imagen = f"public/images/{fecha}-{slug}.png"

    # Generar imagen usando Hugging Face
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

    # Crear post Markdown
    contenido = f"""---
layout: post
title: "¿Sabías que {c['dato']}?"
date: {fecha}
---

{c['explicacion']} {c['explicacion']}  # Explicación más larga

![Imagen relacionada](/images/{fecha}-{slug}.png)
"""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    # Agregar al JSON
    curiosidades_json.append({
        "dato": c["dato"],
        "explicacion": c["explicacion"]*2,
        "imagen": f"images/{fecha}-{slug}.png"
    })

# Guardar JSON
with open("public/curiosidades.json", "w", encoding="utf-8") as f:
    json.dump(curiosidades_json, f, ensure_ascii=False, indent=2)

print("✅ Se generaron 5 posts con imágenes y JSON actualizado.")
