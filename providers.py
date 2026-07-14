"""All API provider calls — text (Groq), image (OpenAI), video (OpenRouter | Replicate).

Fixed vendor URLs are defined as module-level constants.
Credentials and mutable config are imported exclusively from config.py (env-sourced).
"""
from config import (
    GROQ_KEY, OPENAI_KEY, OPENROUTER_KEY, REPLICATE_KEY,
    GROQ_API_BASE, OPENAI_API_BASE, OPENROUTER_API_BASE,
    VIDEO_PROVIDER, MAX_RETRIES, OUTPUT_DIR,
)
import requests, time, os, base64, json, re
from pathlib import Path

# ── Fixed vendor URLs (not credentials — fine as constants) ───────────────────
_REPLICATE_PREDICTIONS = "https://api.replicate.com/v1/models/{model}/predictions"
_REPLICATE_POLL        = "https://api.replicate.com/v1/predictions/{pid}"


# ══════════════════════════════════════════════════════════════════════════════
# TEXT  — Groq
# ══════════════════════════════════════════════════════════════════════════════
def generate_text(system: str, user: str, model: str,
                  temperature: float = 0.7, max_tokens: int = 500) -> str:
    if not GROQ_KEY:
        return "[Error: GROQ_API_KEY missing]"
    H = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    url = f"{GROQ_API_BASE}/chat/completions"
    for attempt in range(MAX_RETRIES):
        try:
            x = requests.post(
                url, headers=H,
                json={"model": model,
                      "messages": [{"role": "system", "content": system},
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


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE  — OpenAI Images API (DALL-E 3 / gpt-image-1)
# --- PRO ADDITION: image provider ---
# ══════════════════════════════════════════════════════════════════════════════
def generate_image(prompt: str, neg_prompt: str = "",
                   width: int = 1024, height: int = 1024,
                   seed: int = None, model: str = "dall-e-3",
                   quality: str = "standard") -> str | None:
    """Generate an image via OpenAI Images API.

    Returns a local file path on success, None on failure.
    The function signature is compatible with the original Pollinations call
    used in app.py — only internals changed.
    """
    if not OPENAI_KEY:
        print("[Error: OPENAI_API_KEY missing]")
        return None

    # Map width×height to the closest DALL-E 3 supported size
    size = _resolve_dalle_size(width, height)

    H = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    url = f"{OPENAI_API_BASE}/images/generations"

    payload: dict = {
        "model":   model,
        "prompt":  prompt[:4000],   # DALL-E 3 max prompt length
        "n":       1,
        "size":    size,
    }
    # DALL-E 3 supports quality param; gpt-image-1 does not use it the same way
    if model == "dall-e-3":
        payload["quality"] = quality
    # DALL-E 3 does not support negative prompts natively — append as instruction
    if neg_prompt:
        payload["prompt"] += f". Avoid: {neg_prompt[:200]}"

    for attempt in range(MAX_RETRIES):
        try:
            x = requests.post(url, headers=H, json=payload, timeout=120)
            if x.status_code == 200:
                data = x.json()["data"][0]
                # API returns either a URL or b64_json depending on response_format
                img_url = data.get("url")
                b64     = data.get("b64_json")
                if img_url:
                    r = requests.get(img_url, timeout=60)
                    if r.status_code == 200:
                        return _save_image(r.content)
                elif b64:
                    return _save_image(base64.b64decode(b64))
            err = x.json().get("error", {}).get("message", x.text[:200])
            print(f"OpenAI Images {x.status_code}: {err}")
            time.sleep(15 if x.status_code == 429 else 3)
        except Exception as e:
            print(f"Image error (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None


def _resolve_dalle_size(width: int, height: int) -> str:
    """Map arbitrary dimensions to the nearest DALL-E 3 supported size."""
    if width == height:
        return "1024x1024"
    if width > height:
        return "1792x1024"
    return "1024x1792"


def _save_image(content: bytes) -> str:
    path = OUTPUT_DIR / f"gen_img_{int(time.time())}.png"
    path.write_bytes(content)
    return str(path)


# ══════════════════════════════════════════════════════════════════════════════
# VIDEO  — OpenRouter (primary) | Replicate (fallback)
# --- PRO ADDITION: swappable video provider ---
# ══════════════════════════════════════════════════════════════════════════════
def generate_video(image_path: str, prompt: str, model: str,
                   resolution: str = "720p", duration: int = 5,
                   aspect_ratio: str = "16:9") -> str | None:
    """Generate a video using the configured VIDEO_PROVIDER.

    Tries OpenRouter first if VIDEO_PROVIDER='openrouter', falls back to
    Replicate if the key is present and the OpenRouter attempt fails.
    """
    if VIDEO_PROVIDER == "replicate":
        return _generate_video_replicate(image_path, prompt, model, resolution, duration)
    # Default: OpenRouter
    result = _generate_video_openrouter(image_path, prompt, model,
                                        resolution, duration, aspect_ratio)
    if result is None and REPLICATE_KEY:
        print("OpenRouter video failed — falling back to Replicate")
        # Use the Replicate model only when falling back
        replicate_model = os.getenv("REPLICATE_VIDEO_MODEL", "wan-video/wan-2.2-i2v-fast")
        result = _generate_video_replicate(image_path, prompt, replicate_model,
                                           resolution, duration)
    return result


# ── OpenRouter video backend ───────────────────────────────────────────────────
def _generate_video_openrouter(image_path: str, prompt: str, model: str,
                                resolution: str, duration: int,
                                aspect_ratio: str) -> str | None:
    if not OPENROUTER_KEY:
        print("[Error: OPENROUTER_API_KEY missing]")
        return None

    H = {"Authorization": f"Bearer {OPENROUTER_KEY}",
         "Content-Type": "application/json",
         "HTTP-Referer": "https://content-engine-pro",
         "X-Title": "Content Engine Pro"}

    submit_url = f"{OPENROUTER_API_BASE}/videos"

    payload: dict = {
        "model":       model,
        "prompt":      prompt,
        "resolution":  resolution,
        "duration":    duration,
        "aspect_ratio": aspect_ratio,
        "generate_audio": False,
    }

    # Attach the hero image as the first frame (image-to-video)
    img_input = _to_image_url(image_path)
    if img_input:
        payload["frame_images"] = [
            {"type": "image_url",
             "image_url": {"url": img_input},
             "frame_type": "first_frame"}
        ]

    for attempt in range(MAX_RETRIES):
        try:
            x = requests.post(submit_url, headers=H, json=payload, timeout=60)
            if x.status_code in (200, 202):
                d = x.json()
                job_id = d.get("id")
                if job_id:
                    return _poll_openrouter_video(job_id, H)
                print(f"OpenRouter video: unexpected response {d}")
                return None
            print(f"OpenRouter video {x.status_code}: {x.text[:300]}")
            time.sleep(5 if x.status_code == 429 else 3)
        except Exception as e:
            print(f"OpenRouter video error (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None


def _poll_openrouter_video(job_id: str, H: dict,
                            max_polls: int = 120, interval: int = 10) -> str | None:
    """Poll /api/v1/videos/{job_id} until completed or failed."""
    poll_url = f"{OPENROUTER_API_BASE}/videos/{job_id}"
    for _ in range(max_polls):
        try:
            r = requests.get(poll_url, headers=H, timeout=30)
            if r.status_code == 200:
                d = r.json()
                status = d.get("status", "")
                if status == "completed":
                    urls = d.get("unsigned_urls") or []
                    if urls:
                        return _download_video(urls[0], H, job_id[:8])
                    return None
                if status in ("failed", "cancelled", "expired"):
                    print(f"OpenRouter video job {job_id}: {status} — {d.get('error','')}")
                    return None
                # pending / in_progress — keep polling
        except Exception as e:
            print(f"OpenRouter poll error: {e}")
        time.sleep(interval)
    print(f"OpenRouter video job {job_id}: timed out after polling")
    return None


def _download_video(url: str, H: dict, name: str) -> str | None:
    """Download video bytes from a URL (with auth header) and save to disk."""
    try:
        r = requests.get(url, headers=H, timeout=180)
        if r.status_code == 200:
            path = OUTPUT_DIR / f"gen_vid_{name}_{int(time.time())}.mp4"
            path.write_bytes(r.content)
            return str(path)
    except Exception as e:
        print(f"Video download error: {e}")
    return None


# ── Replicate video backend ────────────────────────────────────────────────────
def _generate_video_replicate(image_path: str, prompt: str, model: str,
                               resolution: str = "480p", duration: int = 5) -> str | None:
    if not REPLICATE_KEY:
        print("[Error: REPLICATE_API_TOKEN missing]")
        return None
    img_input = _to_image_url(image_path)
    if not img_input:
        return None
    H = {"Authorization": f"Bearer {REPLICATE_KEY}",
         "Content-Type": "application/json",
         "Prefer": "wait"}
    payload = {"input": {"image": img_input, "prompt": prompt,
                          "resolution": resolution,
                          "num_frames": max(25, duration * 16)}}
    for attempt in range(MAX_RETRIES):
        try:
            x = requests.post(
                _REPLICATE_PREDICTIONS.format(model=model),
                headers=H, json=payload, timeout=180)
            if x.status_code in (200, 201):
                d = x.json()
                if d.get("status") == "succeeded":
                    return _dl_replicate_video(d["output"], d["id"][:8])
                pid = d.get("id")
                if pid:
                    return _poll_replicate_video(pid, H)
            print(f"Replicate {x.status_code}: {x.text[:200]}")
        except Exception as e:
            print(f"Replicate video error: {e}")
        time.sleep(3)
    return None


def _poll_replicate_video(pid: str, H: dict, max_polls: int = 60) -> str | None:
    for _ in range(max_polls):
        try:
            x = requests.get(_REPLICATE_POLL.format(pid=pid), headers=H, timeout=15)
            if x.status_code == 200:
                d = x.json()
                s = d.get("status")
                if s == "succeeded":
                    return _dl_replicate_video(d["output"], pid[:8])
                if s in ("failed", "canceled"):
                    return None
        except Exception as e:
            print(f"Replicate poll error: {e}")
        time.sleep(5)
    return None


def _dl_replicate_video(output, name: str) -> str | None:
    url = output if isinstance(output, str) else (output[0] if output else None)
    if not url:
        return None
    r = requests.get(url, timeout=120)
    path = OUTPUT_DIR / f"gen_vid_{name}.mp4"
    path.write_bytes(r.content)
    return str(path)


# ── Shared image-input helper ──────────────────────────────────────────────────
def _to_image_url(img: str) -> str | None:
    """Convert a local path, data-URI, or URL to something the APIs accept."""
    if not img:
        return None
    if img.startswith("http"):
        return img
    if img.startswith("data:image"):
        return img
    if os.path.isfile(img):
        b64 = base64.b64encode(open(img, "rb").read()).decode()
        return f"data:image/png;base64,{b64}"
    return None

# Keep old alias so any external callers are not broken
_to_input = _to_image_url


# ══════════════════════════════════════════════════════════════════════════════
# TTS  — Google gTTS (free, no API key required)
# --- PRO ADDITION: voiceover TTS ---
# ══════════════════════════════════════════════════════════════════════════════
def generate_tts(text: str, voice: str = "alloy", model: str = "tts-1") -> str | None:
    """Convert text to speech via gTTS (free) and save as .mp3.

    voice and model params kept for signature compatibility but unused by gTTS.
    Returns local file path on success, None on failure.
    """
    try:
        from gtts import gTTS
        tts = gTTS(text=text[:4000], lang="en", slow=False)
        path = OUTPUT_DIR / f"voiceover_{int(time.time())}.mp3"
        tts.save(str(path))
        return str(path)
    except ImportError:
        print("[Error: gtts not installed — run: pip install gtts]")
    except Exception as e:
        print(f"gTTS error: {e}")
    return None


# ══════════════════════════════════════════════════════════════════════════════
# Utilities
# ══════════════════════════════════════════════════════════════════════════════
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
