import requests, datetime, os, json

# Carpeta para posts
os.makedirs("_posts", exist_ok=True)
os.makedirs("public", exist_ok=True)

# API de Hugging Face para texto (modelo GPT)
api_url = "https://api-inference.huggingface.co/models/gpt2"  # Puedes cambiar a otro modelo
api_key = os.getenv("HF_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}

curiosidades_json = []

for i in range(5):
    # Pedimos al modelo que genere un dato curioso con explicación
    prompt = "Escribe un dato curioso interesante y su explicación detallada en español, que la gente pueda leer y aprender:"
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        salida = response.json()
        try:
            texto = salida[0]['generated_text']
        except:
            texto = "Dato curioso no generado correctamente."
    else:
        texto = "Error al generar dato curioso."

    # Dividir el texto en "dato" y "explicacion"
    if ". " in texto:
        dato, explicacion = texto.split(". ", 1)
        dato = dato.strip()
        explicacion = explicacion.strip()
    else:
        dato = texto
        explicacion = texto

    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    slug = dato.lower().replace(" ", "-").replace("¿","").replace("?","").replace(".","")

    # Crear Markdown
    nombre_archivo = f"_posts/{fecha}-{slug}.md"
    contenido = f"""---
layout: post
title: "¿Sabías que {dato}?"
date: {fecha}
---

{explicacion}
"""
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    # Agregar al JSON
    curiosidades_json.append({
        "dato": dato,
        "explicacion": explicacion,
        "imagen": None
    })

# Guardar JSON
with open("public/curiosidades.json", "w", encoding="utf-8") as f:
    json.dump(curiosidades_json, f, ensure_ascii=False, indent=2)

print("✅ Se generaron 5 posts con datos curiosos nuevos y JSON actualizado.")
