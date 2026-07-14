"""Standalone image generation helper — wraps providers.generate_image.

--- PRO ADDITION: image provider ---
Replaces the old Pollinations HTTP call with the OpenAI Images API (DALL-E 3 or
gpt-image-1, configured via IMAGE_MODEL env var).  The function signature is
preserved so any legacy callers still work.

app.py calls providers.generate_image() directly, so this file is used only by
standalone scripts or tests.
"""
from config import _IMAGE_MODEL
from providers import generate_image

# Tone → visual style hint (kept from original for standalone use)
_STYLE = {
    "playful":   "bright flat illustration bold colours minimalist",
    "premium":   "photorealistic studio lighting high detail luxurious",
    "eco":       "watercolour natural tones soft lighting earthy",
    "professional": "clean modern corporate photorealistic",
}


def gen_image(prod: str, tag: str, tone: str, model: str = _IMAGE_MODEL) -> str | None:
    """Generate a hero image for a product and return a local file path.

    Args:
        prod:  Product name / description.
        tag:   Campaign tagline (woven into the prompt for context).
        tone:  Brand tone string (mapped to a visual-style hint).
        model: OpenAI image model to use (default from IMAGE_MODEL env var).

    Returns:
        Path to the saved PNG, or None on failure.
    """
    style  = _STYLE.get(tone.lower(), "clean modern professional")
    prompt = (
        f"{style}, {prod}, "
        f"centred product shot, no text, no logos, 16:9, "
        f"inspired by tagline: '{tag[:80]}'"
    )
    # Call the unified provider — already has retry/backoff
    return generate_image(
        prompt=prompt,
        neg_prompt="text, watermark, logo, blurry, distorted",
        width=1792,
        height=1024,
        model=model,
        quality="hd",
    )
