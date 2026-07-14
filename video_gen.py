"""Standalone video generation helper — wraps providers.generate_video.

--- PRO ADDITION: swappable video provider ---
The actual backend (OpenRouter or Replicate) is controlled by the VIDEO_PROVIDER
env var.  This file is kept for standalone/test use; app.py calls
providers.generate_video() directly.

OpenRouter video models confirmed available (July 2026):
  alibaba/wan-2.7          — image-to-video, up to 1080p  (default)
  google/veo-3.1-fast      — text+image input, 720p/1080p
  kwaivgi/kling-v3.0-pro   — image-to-video, 3-15 s, 16:9/9:16/1:1
  minimax/hailuo-2.3       — image-to-video, cinematic
  bytedance/seedance-2.0   — image-to-video, strong character consistency

Replicate fallback models:
  wan-video/wan-2.2-i2v-fast  (env: REPLICATE_VIDEO_MODEL)
"""
from config import _OPENROUTER_VIDEO_MODEL, VIDEO_PROVIDER
from providers import generate_video


def gen_video(img: str, prompt: str = "", model: str = _OPENROUTER_VIDEO_MODEL,
              resolution: str = "720p", duration: int = 5,
              aspect_ratio: str = "16:9") -> str | None:
    """Animate a hero image into a short promotional video.

    Args:
        img:          Local path, data-URI, or URL of the hero image.
        prompt:       Motion/scene description.
        model:        Video model slug (OpenRouter or Replicate, depending on provider).
        resolution:   Output resolution (e.g. '720p', '1080p').
        duration:     Clip length in seconds.
        aspect_ratio: Output aspect ratio (e.g. '16:9').

    Returns:
        Path to the saved .mp4, or None on failure.
    """
    if not prompt:
        prompt = "Slow cinematic push-in, soft light shifts, product reveal"
    return generate_video(
        image_path=img,
        prompt=prompt,
        model=model,
        resolution=resolution,
        duration=duration,
        aspect_ratio=aspect_ratio,
    )
