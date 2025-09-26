import json
import random

# Rutas de archivos
INPUT_FILE = "curiosidades.json"
OUTPUT_FILE = "curiosidades_moderno.json"

# Lista de imágenes por categoría (puedes agregar más)
imagenes = {
    "ciencia": [
        "https://cdn.pixabay.com/photo/2017/08/30/01/05/bee-2693129_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/29/09/32/mount-everest-1869442_1280.jpg"
    ],
    "historia": [
        "https://cdn.pixabay.com/photo/2017/03/27/14/56/egypt-2189886_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/02/19/10/00/roman-1202642_1280.jpg"
    ],
    "animales": [
        "https://cdn.pixabay.com/photo/2020/01/07/16/48/shrimp-4744823_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/08/30/01/05/bee-2693129_1280.jpg"
    ]
}

# Categorías posibles
categorias = list(imagenes.keys())

def convertir():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

    nuevos_datos = []
    for d in datos:
        texto = d.get("dato", "Dato curioso sin texto")
        
        # Generar un título corto (primeras 6 palabras)
        titulo = " ".join(texto.split()[:6]) + "..."
        
        # El resto como descripción
        descripcion = texto

        # Categoría aleatoria
        categoria = random.choice(categorias)

        # Imagen aleatoria de esa categoría
        imagen = random.choice(imagenes[categoria])

        nuevos_datos.append({
            "titulo": titulo,
            "descripcion": descripcion,
            "imagen": imagen,
            "categoria": categoria
        })

    # Guardar en nuevo archivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(nuevos_datos, f, ensure_ascii=False, indent=2)

    print(f"✅ Conversión completa. Guardado en {OUTPUT_FILE}")

if __name__ == "__main__":
    convertir()
