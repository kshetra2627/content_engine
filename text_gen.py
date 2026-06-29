"""Text via Groq API (free)."""
from config import GROQ_KEY, MAX_R
import requests, json, time

U = "https://api.groq.com/openai/v1/chat/completions"
_H = lambda: {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}

def _c(prompt, system, r=MAX_R):
    for _ in range(r):
        try:
            x = requests.post(U, headers=_H(),
                json={"model": "llama-3.3-70b-versatile", "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}], "temperature": 0.7},
                timeout=30)
            if x.status_code == 200:
                return x.json()["choices"][0]["message"]["content"].strip()
            print(f"Groq Error {x.status_code}: {x.text[:100]}")
            time.sleep(5)
        except Exception as e:
            print(f"Groq Error: {e}"); time.sleep(2)
    return "[Error]"

_EX = {"playful": "Ex: Slip into joy", "premium": "Ex: Crafted for those who never settle", "eco": "Ex: Grown not made"}

def tagline(prod, aud, tone):
    e = _EX.get(tone.lower(), "")
    return _c(f"{e}\nProduct:{prod}\nAudience:{aud}\nTone:{tone}\nTagline:",
              "Creative director. ONE tagline. Max 10 words. No hashtags.")

def blog(prod, aud, tone, tag):
    return _c(f"50-word blog intro for {prod}. Weave in tagline:\"{tag}\". Tone:{tone}.",
              f"Content strategist writing for {aud}.")

def social(prod, aud, tone):
    r = _c(f"Social posts for {prod} aud:{aud} tone:{tone}. ONLY JSON keys: twitter(max280) instagram(max2200) linkedin(max700). No fences.",
           "Output only valid JSON.")
    try:
        return json.loads(r)
    except:
        return {"twitter": r[:280], "instagram": r[:2200], "linkedin": r[:700]}
