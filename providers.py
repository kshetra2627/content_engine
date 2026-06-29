"""All API provider calls — text (Groq), image (Pollinations), video (Replicate)."""
from config import GROQ_KEY, REPLICATE_KEY, MAX_RETRIES
import requests, time, os, base64, json, re
from urllib.parse import quote

# ── Text ───────────────────────────────────────────────────────────────────────
def generate_text(system: str, user: str, model: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
    if not GROQ_KEY:
        return "[Error: GROQ_API_KEY missing]"
    H = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    for attempt in range(MAX_RETRIES):
        try:
            x = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=H,
                json={"model": model, "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}],
                    "temperature": min(temperature, 2.0),
                    "max_tokens": max_tokens},
                timeout=60)
            if x.status_code == 200:
                return x.json()["choices"][0]["message"]["content"].strip()
            err = x.json().get("error", {}).get("message", x.text[:100])
            print(f"Groq {x.status_code}: {err}")
            time.sleep(15 if x.status_code == 429 else 2)
        except Exception as e:
            print(f"Groq error: {e}")
            time.sleep(2)
    return "[Error]"

# ── Image ──────────────────────────────────────────────────────────────────────
def generate_image(prompt: str, neg_prompt: str = "", width: int = 1280, height: int = 720, seed: int = None) -> str | None:
    encoded = quote(prompt[:500])
    params  = f"width={width}&height={height}&nologo=true"
    if seed:  params += f"&seed={seed}"
    url = f"https://image.pollinations.ai/prompt/{encoded}?{params}"
    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, timeout=90)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image"):
                path = f"_gen_img_{int(time.time())}.png"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            time.sleep(3)
        except Exception as e:
            print(f"Image error: {e}")
            time.sleep(3)
    return None

# ── Video ──────────────────────────────────────────────────────────────────────
def generate_video(image_path: str, prompt: str, model: str, resolution: str = "480p", duration: int = 5) -> str | None:
    if not REPLICATE_KEY:
        return None
    img_input = _to_input(image_path)
    if not img_input:
        return None
    H = {"Authorization": f"Bearer {REPLICATE_KEY}", "Content-Type": "application/json", "Prefer": "wait"}
    payload = {"input": {"image": img_input, "prompt": prompt, "resolution": resolution,
                         "num_frames": max(25, duration * 16)}}
    for _ in range(MAX_RETRIES):
        try:
            x = requests.post(f"https://api.replicate.com/v1/models/{model}/predictions",
                              headers=H, json=payload, timeout=180)
            if x.status_code in (200, 201):
                d = x.json()
                if d.get("status") == "succeeded":
                    return _dl_video(d["output"], d["id"][:8])
                pid = d.get("id")
                if pid:
                    return _poll_video(pid, H)
            print(f"Replicate {x.status_code}: {x.text[:200]}")
        except Exception as e:
            print(f"Video error: {e}")
        time.sleep(3)
    return None

def _poll_video(pid: str, H: dict, m: int = 60) -> str | None:
    for _ in range(m):
        try:
            x = requests.get(f"https://api.replicate.com/v1/predictions/{pid}", headers=H, timeout=15)
            if x.status_code == 200:
                d = x.json()
                s = d.get("status")
                if s == "succeeded":
                    return _dl_video(d["output"], pid[:8])
                if s in ("failed", "canceled"):
                    return None
        except Exception as e:
            print(f"Poll error: {e}")
        time.sleep(5)
    return None

def _dl_video(output, name: str) -> str | None:
    url = output if isinstance(output, str) else (output[0] if output else None)
    if not url:
        return None
    r = requests.get(url, timeout=120)
    path = f"_gen_vid_{name}.mp4"
    with open(path, "wb") as f:
        f.write(r.content)
    return path

def _to_input(img: str) -> str | None:
    if not img:
        return None
    if img.startswith("http"):
        return img
    if os.path.isfile(img):
        b64 = base64.b64encode(open(img, "rb").read()).decode()
        return f"data:image/png;base64,{b64}"
    if img.startswith("data:image"):
        return img
    return None

# ── Utilities ──────────────────────────────────────────────────────────────────
def parse_json_response(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip().strip("`")
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    return {}
