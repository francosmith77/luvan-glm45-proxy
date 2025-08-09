from fastapi import FastAPI
import requests, os

app = FastAPI()

# --- Config ---
OR_API = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_ID", "zai-org/glm-4.5-air")  # Cambiá a 'zai-org/glm-4.5' si querés el full

@app.get("/")
def root():
    return {"ok": True, "model": MODEL}

# --- Texto (GLM-4.5) ---
@app.post("/chat")
def chat(body: dict):
    if not OR_KEY:
        return {"error": "Falta OPENROUTER_API_KEY"}

    headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": body.get("messages", []),
        "reasoning": {"effort": body.get("effort", "medium")},
        "extra_body": {"chat_template_kwargs": {"enable_thinking": body.get("thinking", True)}}
    }
    r = requests.post(OR_API, json=payload, headers=headers, timeout=120)
    return r.json()

# --- Imágenes ---
@app.post("/img")
def gen_img(body: dict):
    if not OR_KEY:
        return {"error": "Falta OPENROUTER_API_KEY"}

    image_model = os.getenv("IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

    payload = {
        "model": image_model,                       # p.ej. FLUX.1-schnell / sdxl-turbo / FLUX.1-dev
        "prompt": body.get("prompt", ""),
        "n": int(body.get("n", 1)),
        "size": body.get("size", "1024x1024"),      # 512x512, 768x1024, etc.
        "response_format": body.get("response_format", "url")
    }

    headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"}
    OR_IMG_API = "https://openrouter.ai/api/v1/images/generations"

    r = requests.post(OR_IMG_API, json=payload, headers=headers, timeout=300)
    return r.json()
