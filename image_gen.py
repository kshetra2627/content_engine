"""Image via Pollinations.AI (free, no API key)."""
import requests, time
from urllib.parse import quote

_S = {"playful": "bright flat illustration bold colours minimalist",
      "premium": "photorealistic studio lighting high detail",
      "eco": "watercolour natural tones soft lighting"}

def gen_image(prod, tag, tone):
    s = _S.get(tone.lower(), "clean modern professional")
    prompt = quote(f"{s}, {prod}, centred, no text, no logos, 16:9")
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=1280&height=720&nologo=true&seed={int(time.time())}"
    for _ in range(3):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200 and r.headers.get("content-type","").startswith("image"):
                path = f"_gen_img_{int(time.time())}.png"
                with open(path, "wb") as f:
                    f.write(r.content)
                return path
            time.sleep(3)
        except Exception as e:
            print(f"Img Error: {e}"); time.sleep(3)
    return None
