"""Standalone text generation helpers — wraps providers.generate_text.

This file is a thin compatibility shim for standalone scripts.
app.py calls providers.generate_text() directly.

--- PRO ADDITION: config fix ---
Removed the broken MAX_R import alias (config.py never exported MAX_R).
All endpoint/key config now sourced from config.py, not hardcoded.
"""
from config import MAX_RETRIES  # was wrongly imported as MAX_R in original
from providers import generate_text, parse_json_response

_DEFAULT_MODEL = "llama-3.3-70b-versatile"

_EX = {
    "playful": "Ex: Slip into joy",
    "premium": "Ex: Crafted for those who never settle",
    "eco":     "Ex: Grown not made",
}


def tagline(prod: str, aud: str, tone: str, model: str = _DEFAULT_MODEL) -> str:
    e = _EX.get(tone.lower(), "")
    sys = "Creative director. ONE tagline. Max 10 words. No hashtags."
    usr = f"{e}\nProduct:{prod}\nAudience:{aud}\nTone:{tone}\nTagline:"
    return generate_text(sys, usr, model, temperature=0.8, max_tokens=60)


def blog(prod: str, aud: str, tone: str, tag: str,
         model: str = _DEFAULT_MODEL) -> str:
    sys = f"Content strategist writing for {aud}."
    usr = f"50-word blog intro for {prod}. Weave in tagline:\"{tag}\". Tone:{tone}."
    return generate_text(sys, usr, model, temperature=0.7, max_tokens=200)


def social(prod: str, aud: str, tone: str,
           model: str = _DEFAULT_MODEL) -> dict:
    sys = "Output only valid JSON."
    usr = (
        f"Social posts for {prod} aud:{aud} tone:{tone}. "
        "ONLY JSON keys: twitter(max280) instagram(max2200) linkedin(max700). No fences."
    )
    raw = generate_text(sys, usr, model, temperature=0.7, max_tokens=600)
    parsed = parse_json_response(raw)
    if parsed:
        return parsed
    return {"twitter": raw[:280], "instagram": raw[:2200], "linkedin": raw[:700]}
