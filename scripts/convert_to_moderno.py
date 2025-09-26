import json
import random

# Archivos
INPUT_FILE = "curiosidades.json"
OUTPUT_FILE = "curiosidades_moderno.json"

# Imágenes organizadas por categoría
imagenes = {
    "ciencia": [
        "https://cdn.pixabay.com/photo/2017/08/30/01/05/bee-2693129_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/11/29/09/32/mount-everest-1869442_1280.jpg",
        "https://cdn.pixabay.com/photo/2015/06/24/15/45/space-820604_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/02/01/22/02/atom-2035236_1280.png",
        "https://cdn.pixabay.com/photo/2016/11/29/04/11/microscope-1862641_1280.jpg"
    ],
    "historia": [
        "https://cdn.pixabay.com/photo/2017/03/27/14/56/egypt-2189886_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/02/19/10/00/roman-1202642_1280.jpg",
        "https://cdn.pixabay.com/photo/2019/10/15/20/25/castle-4551443_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/08/06/15/13/book-2597350_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/01/14/12/59/library-1976496_1280.jpg"
    ],
    "animales": [
        "https://cdn.pixabay.com/photo/2020/01/07/16/48/shrimp-4744823_1280.jpg",
        "https://cdn.pixabay.com/photo/2017/08/30/01/05/bee-2693129_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/01/05/13/58/eagle-1125378_1280.jpg",
        "https://cdn.pixabay.com/photo/2018/05/23/23/17/lion-3428058_1280.jpg",
        "https://cdn.pixabay.com/photo/2015/11/19/21/11/dolphin-1058779_1280.jpg"
    ]
}

categorias = list(imagenes.keys())

def convertir():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        datos = json.load(f)

    nuevos_datos = []
    for d in datos:
        texto = d.get("dato", "Dato curioso sin texto")

        # Generar título corto (primeras 6 palabras)
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
