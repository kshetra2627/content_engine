"""Video via Replicate API — $5 free credits on signup (~100 videos), no waitlist."""
from config import REPLICATE_KEY, MAX_R
import requests, time, os, base64

H = lambda: {"Authorization": f"Bearer {REPLICATE_KEY}", "Content-Type": "application/json", "Prefer": "wait"}
MODEL = "wan-video/wan-2.2-i2v-fast"

def gen_video(img):
    if not REPLICATE_KEY or not img:
        return None
    img_url = _to_data_uri(img)
    if not img_url:
        return None
    for _ in range(MAX_R):
        try:
            x = requests.post(
                f"https://api.replicate.com/v1/models/{MODEL}/predictions",
                headers=H(),
                json={"input": {"image": img_url, "prompt": "Slow cinematic push-in, soft light shifts gently", "num_frames": 81, "resolution": "480p"}},
                timeout=120,
            )
            if x.status_code in (200, 201):
                d = x.json()
                if d.get("status") == "succeeded":
                    return _download(d["output"], d["id"][:8])
                pred_id = d.get("id")
                if pred_id:
                    return _poll(pred_id)
            print(f"Vid API Error {x.status_code}: {x.text[:200]}")
        except Exception as e:
            print(f"Vid Error: {e}")
        time.sleep(3)
    return None

def _poll(pred_id, m=40):
    for _ in range(m):
        try:
            x = requests.get(f"https://api.replicate.com/v1/predictions/{pred_id}", headers=H(), timeout=15)
            if x.status_code == 200:
                d = x.json()
                s = d.get("status")
                if s == "succeeded":
                    return _download(d["output"], pred_id[:8])
                if s in ("failed", "canceled"):
                    print(f"Replicate failed: {d.get('error')}")
                    return None
        except Exception as e:
            print(f"Poll error: {e}")
        time.sleep(5)
    return None

def _download(output, name):
    url = output if isinstance(output, str) else (output[0] if output else None)
    if not url:
        return None
    r = requests.get(url, timeout=60)
    path = f"_gen_vid_{name}.mp4"
    with open(path, "wb") as f:
        f.write(r.content)
    return path

def _to_data_uri(img):
    if isinstance(img, str) and img.startswith("http"):
        return img  # Replicate accepts URLs directly
    if isinstance(img, str) and os.path.isfile(img):
        b64 = base64.b64encode(open(img, "rb").read()).decode()
        return f"data:image/png;base64,{b64}"
    if isinstance(img, str) and img.startswith("data:image"):
        return img
    return None
