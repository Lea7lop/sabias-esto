import requests, json, datetime, os, random

# Carpetas
json_file = "curiosidades.json"
posts_folder = "_posts/"
images_folder = "images/"

os.makedirs(posts_folder, exist_ok=True)
os.makedirs(images_folder, exist_ok=True)

# --- Función para generar texto automáticamente ---
def generar_curiosidad():
    # Lista de ideas iniciales; luego se puede reemplazar por IA de texto real
    datos_ejemplo = [
        "El pulpo tiene tres corazones",
        "Los plátanos son bayas, pero las frutillas no",
        "En Júpiter y Saturno puede llover diamantes",
        "Las abejas tienen cinco ojos",
        "El agua puede hervir y congelarse al mismo tiempo",
        "Los gatos tienen más huesos en la cola que los humanos",
        "Los delfines tienen nombres para identificarse entre sí",
        "La miel nunca se echa a perder"
    ]
    explicacion = "Esta curiosidad es interesante porque ofrece un dato poco conocido que despierta la curiosidad del lector y fomenta el aprendizaje sobre la naturaleza y la ciencia."
    dato = random.choice(datos_ejemplo)
    return {"dato": dato, "explicacion": explicacion}

# --- Función para generar imagen con Raphael AI ---
def generar_imagen(prompt):
    url = "https://raphaelai.org/generate"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "aspect_ratio": "16:9", "style": "realismo"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get("image_url")
        else:
            print("Error generando imagen, se usará placeholder")
            return "placeholder.png"
    except:
        return "placeholder.png"

# --- Generar 5 curiosidades ---
curiosidades = []
for _ in range(5):
    c = generar_curiosidad()
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = c["dato"].lower().replace(" ", "-").replace("?", "").replace(".", "")
    nombre_archivo = f"{posts_folder}{fecha}-{slug}.md"
    nombre_imagen = f"{images_folder}{fecha}-{slug}.png"

    # Generar imagen
    imagen_url = generar_imagen(c["dato"])
    if imagen_url != "placeholder.png":
        img_data = requests.get(imagen_url).content
        with open(nombre_imagen, "wb") as handler:
            handler.write(img_data)
    else:
        nombre_imagen = "placeholder.png"

    # Explicación larga
    explicacion_larga = c["explicacion"] + " Además, esta información permite entender mejor fenómenos curiosos que sorprenden a cualquier persona y son excelentes para aprender mientras te entretienes."

    # Crear post Markdown
    contenido = f"""---
layout: post
title: "¿Sabías que {c['dato']}?"
date: {fecha}
---

{explicacion_larga}

![Imagen relacionada](/{nombre_imagen})
"""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    # Guardar info en JSON
    c["imagen"] = nombre_imagen
    curiosidades.append(c)
    print(f"Post creado: {nombre_archivo}")

# Actualizar JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(curiosidades, f, ensure_ascii=False, indent=2)
