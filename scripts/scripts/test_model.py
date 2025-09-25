import requests
import os

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # Cambia a Phi-3-mini-4k-instruct si quieres probar ese

response = requests.post(
    f"https://api-inference.huggingface.co/models/{MODEL}",
    headers={"Authorization": f"Bearer {HF_TOKEN}"},
    json={"inputs": "Hola, genera un ejemplo de dato curioso."}
)

print("Status code:", response.status_code)
print("Response:", response.text)
