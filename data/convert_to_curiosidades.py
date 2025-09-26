import json
from datetime import date

# Configuración: archivo de entrada y salida
input_file = "data.json"
output_file = "curiosidades.json"

# Función para asignar categoría según palabras clave
def asignar_categoria(dato_texto):
    dato_lower = dato_texto.lower()
    if any(palabra in dato_lower for palabra in ["roma", "historia", "coliseo", "muralla", "antigua"]):
        return "Historia"
    else:
        return "Ciencia"

# Cargar datos originales
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Fecha de hoy
hoy = date.today().isoformat()

# Transformar datos al formato nuevo
curiosidades = []
for item in data:
    fact = item.get("dato", "")
    explanation = item.get("explicacion", "")
    category = asignar_categoria(fact)
    curiosidades.append({
        "fact": fact,
        "explanation": explanation,
        "category": category,
        "date": hoy
    })

# Guardar en archivo de salida
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(curiosidades, f, indent=2, ensure_ascii=False)

print(f"Archivo '{output_file}' generado correctamente con {len(curiosidades)} entradas.")
