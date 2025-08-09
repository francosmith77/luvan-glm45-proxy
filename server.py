from fastapi import FastAPI
import requests, os

app = FastAPI()
OR_API = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL_ID", "zai-org/glm-4.5-air")  # cambiar a 'zai-org/glm-4.5' si querés full

@app.get("/")
def root():
    return {"ok": True, "model": MODEL}

@app.post("/chat")
def chat(body: dict):
    if not OR_KEY:
        return {"error": "Falta OPENROUTER_API_KEY"}
    headers = {"Authorization": f"Bearer {OR_KEY}", "Content-Type":"application/json"}
    payload = {
        "model": MODEL,
        "messages": body.get("messages", []),
        "reasoning": {"effort": body.get("effort", "medium")},
        "extra_body": {"chat_template_kwargs": {"enable_thinking": body.get("thinking", True)}}
    }
    r = requests.post(OR_API, json=payload, headers=headers, timeout=120)
    return r.json()
@app.post("/img")
def gen_img(body: dict):
    OR_IMG_API = "https://openrouter.ai/api/v1/images"
    if not OR_KEY:
        return {"error": "Falta OPENROUTER_API_KEY"}
    
    headers = {
        "Authorization": f"Bearer {OR_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gryphe/mythomax-l2-13b",  # Podés cambiar por otro modelo de imágenes soportado en OpenRouter
        "prompt": body.get("prompt", ""),
        "size": body.get("size", "1024x1024"),  # Tamaño por defecto
        "n": body.get("n", 1)  # Número de imágenes
    }
    r = requests.post(OR_IMG_API, json=payload, headers=headers, timeout=120)
    return r.json()
