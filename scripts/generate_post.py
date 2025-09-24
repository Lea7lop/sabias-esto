import random, datetime, requests, os, json

# Lista de datos curiosos con explicaciones más largas
curiosidades = [
    {
        "dato": "El pulpo tiene tres corazones.",
        "explicacion": (
            "Dos bombean sangre a las branquias y uno al resto del cuerpo. "
            "Lo curioso es que el principal se detiene cuando nada, lo que significa "
            "que el pulpo tiene una forma única de distribuir oxígeno y conservar energía. "
            "Además, su sangre es de color azul debido a la hemocianina, lo que mejora el transporte "
            "de oxígeno en aguas frías y con poca disponibilidad de este."
        )
    },
    {
        "dato": "Los plátanos son bayas, pero las frutillas no.",
        "explicacion": (
            "Botánicamente, el plátano es una baya simple porque se desarrolla a partir de un solo ovario "
            "y contiene semillas diminutas dentro de la pulpa. "
            "Por otro lado, la frutilla es un fruto agregado, formado por varios ovarios de la misma flor, "
            "lo que la hace diferente de una baya real. Esta clasificación científica es distinta a la percepción común."
        )
    },
    {
        "dato": "En Júpiter y Saturno puede llover diamantes.",
        "explicacion": (
            "La presión atmosférica en estos planetas es tan alta que el carbono presente en la atmósfera "
            "se cristaliza formando diamantes sólidos que caen como lluvia. "
            "Este fenómeno ha sido teorizado mediante modelos de laboratorio y nos muestra cómo las condiciones extremas "
            "pueden crear minerales de formas inesperadas en otros mundos."
        )
    }
]

# Crear carpeta pública de imágenes
os.makedirs("public/images", exist_ok=True)

# Lista para actualizar JSON
curiosidades_json = []

# Generar 5 posts
for _ in range(5):
    c = random.choice(curiosidades)
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = c["dato"].lower().replace(" ", "-").replace("¿", "").replace("?", "").replace(".", "")
    
    nombre_archivo = f"_posts/{fecha}-{slug}.md"
    nombre_imagen = f"public/images/{fecha}-{slug}.png"
    
    # Generar imagen usando API
    api_url = "TU_API_DE_IMAGEN"  # Reemplaza con Raphael AI o la IA que uses
    api_key = os.getenv("RAPHAEL_API_KEY")

    response = requests.post(api_url, json={"prompt": c["dato"]}, headers={"Authorization": f"Bearer {api_key}"})
    
    if response.status_code == 200:
        img_url = response.json().get("image_url")
        if img_url:
            img_data = requests.get(img_url).content
            with open(nombre_imagen, "wb") as handler:
                handler.write(img_data)
    else:
        print("No se generó imagen; el post se creará sin imagen")

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

    # Agregar al JSON con explicación larga
    curiosidades_json.append({
        "dato": c["dato"],
        "explicacion": c["explicacion"],  # ya es larga
        "imagen": f"images/{fecha}-{slug}.png"
    })

# Guardar JSON
with open("public/curiosidades.json", "w", encoding="utf-8") as f:
    json.dump(curiosidades_json, f, ensure_ascii=False, indent=2)
