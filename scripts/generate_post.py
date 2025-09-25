#!/usr/bin/env python3
"""
Genera 5 datos curiosos usando Hugging Face Inference API y los guarda:
- _posts/YYYY-MM-DD-slug.md
- curiosidades.json

Versión mejorada: explicaciones largas y estilo educativo.
"""

import os, requests, json, time, random, re, datetime

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise SystemExit("ERROR: HF_TOKEN no encontrado en variables de entorno.")

MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
API = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

random.seed()

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9áéíóúñ]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:60]

def call_hf(prompt, max_new_tokens=900, temperature=0.7):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": 0.95
        },
        "options": {"wait_for_model": True}
    }
    r = requests.post(API, headers=HEADERS, json=payload, timeout=180)
    if r.status_code != 200:
        raise Exception(f"Hugging Face API error {r.status_code}: {r.text}")
    data = r.json()
    if isinstance(data, list):
        text = "".join([d.get("generated_text","") for d in data])
    elif isinstance(data, dict) and "generated_text" in data:
        text = data["generated_text"]
    else:
        text = json.dumps(data)
    return text.strip()

def extract_json(text):
    m = re.search(r'(\{.*\})', text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

CATEGORIES = [
    "Historia", "Ciencia", "Tecnología", "Arte", "Geografía",
    "Biología", "Astronomía", "Inventos", "Cultura", "Deportes"
]

def make_prompt(category):
    return (
        f"Eres un redactor experto en educación y curiosidades. "
        f"Tu tarea es generar UN dato curioso original y fascinante sobre el tema: {category}.\n\n"
        f"Requisitos:\n"
        "- Explicación extensa y detallada, estilo blog educativo, mínimo 300 palabras.\n"
        "- Usar lenguaje claro, ejemplos o anécdotas si es posible.\n"
        "- Mantener tono entretenido y didáctico.\n"
        "- Generar SOLO JSON válido con claves:\n"
        "  - title (string, <100 caracteres)\n"
        "  - body (string, explicación larga)\n"
        "  - tags (lista de 3-6 strings)\n"
        "  - image_prompt (string breve para generar imagen)\n"
        "  - source (string, fuente si se conoce o '' si no)\n"
        "IMPORTANTE: Devuelve SOLO JSON sin texto extra."
    )

def ensure_unique_title(title, seen):
    base = title
    i = 1
    while title in seen:
        i += 1
        title = f"{base} ({i})"
    seen.add(title)
    return title

def main():
    os.makedirs("_posts", exist_ok=True)
    results = []
    seen_titles = set()
    tries = 0
    while len(results) < 5 and tries < 15:
        tries += 1
        category = random.choice(CATEGORIES)
        prompt = make_prompt(category)
        try:
            raw = call_hf(prompt, max_new_tokens=900, temperature=0.7)
        except Exception as e:
            print("HF ERROR:", e)
            time.sleep(5)
            continue
        data = extract_json(raw)
        if not data:
            print("No se pudo extraer JSON, HF devolvió (primeros 300 chars):")
            print(raw[:300])
            time.sleep(1)
            continue
        title = data.get("title","Dato curioso")
        title = ensure_unique_title(title, seen_titles)
        body = data.get("body","")
        tags = data.get("tags",[])
        image_prompt = data.get("image_prompt","")
        slug = slugify(title)
        date = datetime.date.today().isoformat()
        filename = f"_posts/{date}-{slug}.md"
        md = f"---\ntitle: \"{title}\"\ndate: {date}\ntags: {json.dumps(tags)}\nimage_prompt: \"{image_prompt}\"\n---\n\n{body}\n"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)
        results.append({
            "title": title,
            "slug": slug,
            "date": date,
            "tags": tags,
            "image_prompt": image_prompt,
            "body": body,
            "source": data.get("source","")
        })
        print("Generado:", title)
        time.sleep(2)
    with open("curiosidades.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Generados {len(results)} datos curiosos. Archivos en _posts/ y curiosidades.json")

if __name__ == "__main__":
    main()
