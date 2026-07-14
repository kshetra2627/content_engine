"""Central configuration — all options, models, and settings live here.
Secrets and mutable defaults are sourced exclusively from environment variables
(loaded via python-dotenv). No real-looking sample data is baked into this file.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ───────────────────────────────────────────────────────────────────
GROQ_KEY          = os.getenv("GROQ_API_KEY", "")
OPENAI_KEY        = os.getenv("OPENAI_API_KEY", "")          # --- PRO ADDITION: image + TTS ---
OPENROUTER_KEY    = os.getenv("OPENROUTER_API_KEY", "")      # --- PRO ADDITION: video via OpenRouter ---
REPLICATE_KEY     = os.getenv("REPLICATE_API_TOKEN", "")

MAX_RETRIES       = 3
PROMPT_HISTORY_LIMIT = 20

# ── Endpoint bases (override for self-hosted proxies; otherwise use defaults) ──
# --- PRO ADDITION: endpoint env vars ---
GROQ_API_BASE        = os.getenv("GROQ_API_BASE",        "https://api.groq.com/openai/v1")
# If user points GROQ_API_BASE at the console/web host, normalize it to the correct OpenAI-compatible API base.
if GROQ_API_BASE.rstrip("/") == "https://console.groq.com":
    GROQ_API_BASE = "https://api.groq.com/openai/v1"

OPENAI_API_BASE      = os.getenv("OPENAI_API_BASE",      "https://api.openai.com/v1")
OPENROUTER_API_BASE  = os.getenv("OPENROUTER_API_BASE",  "https://openrouter.ai/api/v1")

# ── Provider selection ─────────────────────────────────────────────────────────
# --- PRO ADDITION: swappable video provider ---
VIDEO_PROVIDER = os.getenv("VIDEO_PROVIDER", "openrouter").lower()  # "openrouter" | "replicate"

# ── Model IDs ──────────────────────────────────────────────────────────────────
# All model IDs come from env vars with sensible defaults — never literals in code.
# --- PRO ADDITION: env-driven model IDs ---
_TEXT_MODEL_DEFAULT      = os.getenv("TEXT_MODEL_DEFAULT",      "llama-3.3-70b-versatile")
_IMAGE_MODEL             = os.getenv("IMAGE_MODEL",             "dall-e-3")
_OPENROUTER_VIDEO_MODEL  = os.getenv("OPENROUTER_VIDEO_MODEL",  "alibaba/wan-2.7")
_REPLICATE_VIDEO_MODEL   = os.getenv("REPLICATE_VIDEO_MODEL",   "wan-video/wan-2.2-i2v-fast")

TEXT_MODELS = {
    _TEXT_MODEL_DEFAULT:           "Llama 3.3 70B (Default)",
    "llama-3.1-8b-instant":        "Llama 3.1 8B (Fast)",
    "mixtral-8x7b-32768":          "Mixtral 8x7B",
    "gemma2-9b-it":                "Gemma 2 9B",
}

# --- PRO ADDITION: OpenAI image models ---
IMAGE_MODELS = {
    _IMAGE_MODEL:    f"OpenAI {_IMAGE_MODEL.upper()} (Default)",
    "dall-e-3":      "OpenAI DALL·E 3",
    "gpt-image-1":   "OpenAI GPT-Image-1",
}
# Deduplicate in case env var is one of the literals
IMAGE_MODELS = dict(dict.fromkeys(IMAGE_MODELS))

# --- PRO ADDITION: both OpenRouter and Replicate video models ---
VIDEO_MODELS = {
    _OPENROUTER_VIDEO_MODEL:       "Wan 2.7 via OpenRouter (Default)",
    "google/veo-3.1-fast":         "Veo 3.1 Fast via OpenRouter",
    "kwaivgi/kling-v3.0-pro":      "Kling v3.0 Pro via OpenRouter",
    "wan-video/wan-2.2-i2v-fast":  "Wan 2.2 Fast (Replicate fallback)",
    "wan-video/wan-2.5-i2v-fast":  "Wan 2.5 Fast (Replicate fallback)",
}

# ── Campaign Brief Fields ──────────────────────────────────────────────────────
# Defaults are loaded from default_campaign.json so no sample data lives in code.
# --- PRO ADDITION: external campaign defaults ---
def _load_campaign_defaults() -> dict:
    path = Path(__file__).parent / "default_campaign.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return {k: v for k, v in data.items() if not k.startswith("_")}
        except Exception:
            pass
    return {}

_CAMP_DEFAULTS = _load_campaign_defaults()

CAMPAIGN_FIELDS = [
    {"key": "product_name",        "label": "Product Name",        "type": "text",     "default": _CAMP_DEFAULTS.get("product_name", ""), "required": True},
    {"key": "product_category",    "label": "Product Category",    "type": "select",   "default": _CAMP_DEFAULTS.get("product_category", "Consumer Goods"),
     "options": ["Consumer Goods","SaaS","E-commerce","Healthcare","Finance","Education","Food & Beverage","Fashion","Travel","Real Estate","Technology","Other"]},
    {"key": "product_description", "label": "Product Description", "type": "textarea", "default": _CAMP_DEFAULTS.get("product_description", ""), "required": True},
    {"key": "target_audience",     "label": "Target Audience",     "type": "text",     "default": _CAMP_DEFAULTS.get("target_audience", ""), "required": True},
    {"key": "brand_tone",          "label": "Brand Tone",          "type": "select",   "default": _CAMP_DEFAULTS.get("brand_tone", "Professional"),
     "options": ["Playful","Premium","Eco-friendly","Professional","Bold","Minimalist","Luxury","Friendly","Authoritative","Inspirational"]},
    {"key": "campaign_goal",       "label": "Campaign Goal",       "type": "select",   "default": _CAMP_DEFAULTS.get("campaign_goal", "Brand Awareness"),
     "options": ["Brand Awareness","Lead Generation","Product Launch","Sales Conversion","Customer Retention","Event Promotion","App Downloads"]},
    {"key": "industry",            "label": "Industry",            "type": "select",   "default": _CAMP_DEFAULTS.get("industry", "Technology"),
     "options": ["Technology","Healthcare","Finance","Retail","Education","Food","Travel","Real Estate","Entertainment","Other"]},
    {"key": "target_region",       "label": "Target Region",       "type": "select",   "default": _CAMP_DEFAULTS.get("target_region", "Global"),
     "options": ["Global","North America","Europe","Asia Pacific","Latin America","Middle East","Africa"]},
    {"key": "language",            "label": "Language",            "type": "select",   "default": _CAMP_DEFAULTS.get("language", "English"),
     "options": ["English","Spanish","French","German","Portuguese","Arabic","Hindi","Chinese","Japanese"]},
    {"key": "call_to_action",      "label": "Call to Action",      "type": "text",     "default": _CAMP_DEFAULTS.get("call_to_action", "")},
]

# ── Image Specs ────────────────────────────────────────────────────────────────
IMAGE_SPECS = {
    "visual_style":      ["Photorealistic","Flat Illustration","3D Render","Watercolor","Minimalist","Cinematic","Vintage","Futuristic","Corporate"],
    "marketing_template":["Product Hero","Lifestyle","Feature Highlight","Social Ad","Event Banner","Billboard"],
    "subject_focus":     ["Product Only","Product with Person","Person Only","Abstract","Environment","Close-up"],
    "background":        ["Pure White","Studio Gradient","Natural Environment","Urban","Abstract","Blurred Bokeh"],
    "lighting":          ["Natural Daylight","Studio Soft Box","Golden Hour","Dramatic High Contrast","Neon","Backlit"],
    "camera_angle":      ["Eye Level","Bird's Eye","Low Angle","Macro","Wide Angle","Portrait"],
    "composition":       ["Rule of Thirds","Centered","Negative Space","Symmetrical","Dynamic"],
    "mood":              ["Energetic","Calm","Luxurious","Playful","Professional","Dramatic","Warm"],
    "color_theme":       ["Brand Colors","Monochrome","Warm Tones","Cool Tones","Pastel","Vibrant","Earth Tones"],
    "aspect_ratio":      ["1024x1024","1792x1024","1024x1792"],   # DALL-E 3 supported sizes
    "image_quality":     ["standard","hd"],                        # DALL-E 3 quality param
    "detail_level":      ["Minimal","Moderate","Highly Detailed"],
}

# ── Video Specs ────────────────────────────────────────────────────────────────
VIDEO_SPECS = {
    "duration":          ["5","8","10"],
    "motion_style":      ["Cinematic","Dynamic","Subtle","Dramatic","Smooth","Energetic"],
    "camera_movement":   ["Static","Push In","Pull Out","Pan Left","Pan Right","Tilt Up","Tilt Down","Orbit","Handheld"],
    "subject_motion":    ["None","Walk","Run","Dance","Gesture","Idle"],
    "background_motion": ["Static","Parallax","Flowing","Bokeh Shift"],
    "cinematic_style":   ["Hollywood","Documentary","Commercial","Music Video","Social Media"],
    "resolution":        ["480p","720p","1080p"],
    "motion_intensity":  ["Low","Medium","High"],
    "aspect_ratio":      ["16:9","9:16","1:1"],
}

# ── Text Settings ──────────────────────────────────────────────────────────────
TEXT_SETTINGS = {
    "creativity":     {"Low": 0.3, "Medium": 0.7, "High": 1.0, "Maximum": 1.4},
    "formality":      ["Very Casual","Casual","Neutral","Formal","Very Formal"],
    "reading_level":  ["Elementary","Middle School","High School","College","Expert"],
    "writing_style":  ["Storytelling","Listicle","Problem-Solution","How-To","Comparison","Inspirational"],
    "emotional_tone": ["Neutral","Positive","Urgent","Empathetic","Humorous","Serious"],
    "output_length":  {"Brief": 50, "Standard": 150, "Detailed": 300, "Comprehensive": 500},
    "emoji_usage":    ["None","Minimal","Moderate","Heavy"],
    "hashtag_usage":  ["None","Few (3-5)","Moderate (6-10)","Heavy (11+)"],
    "cta_style":      ["Direct","Soft","Question","Urgency","Benefit-led"],
}

# ── Social Platforms ───────────────────────────────────────────────────────────
SOCIAL_PLATFORMS = {
    "twitter":   {"label": "X / Twitter",  "color": "#60A5FA", "char_limit": 280,  "emoji_density": "low",    "hashtag_count": 2,  "default_enabled": True},
    "instagram": {"label": "Instagram",    "color": "#F472B6", "char_limit": 2200, "emoji_density": "medium", "hashtag_count": 10, "default_enabled": True},
    "linkedin":  {"label": "LinkedIn",     "color": "#60A5FA", "char_limit": 700,  "emoji_density": "low",    "hashtag_count": 5,  "default_enabled": True},
    "facebook":  {"label": "Facebook",     "color": "#818CF8", "char_limit": 500,  "emoji_density": "medium", "hashtag_count": 3,  "default_enabled": False},
    "tiktok":    {"label": "TikTok",       "color": "#F87171", "char_limit": 300,  "emoji_density": "high",   "hashtag_count": 5,  "default_enabled": False},
}

# ── Analytics Metrics ──────────────────────────────────────────────────────────
ANALYTICS_METRICS = [
    {"key": "brand_consistency",      "label": "Brand Consistency",      "icon": "🎯", "description": "How well content aligns with brand tone"},
    {"key": "creativity_score",       "label": "Creativity",             "icon": "✨", "description": "Originality and creative appeal"},
    {"key": "marketing_effectiveness","label": "Marketing Effectiveness","icon": "📈", "description": "Potential to achieve campaign goal"},
    {"key": "readability",            "label": "Readability",            "icon": "📖", "description": "Ease of reading and comprehension"},
    {"key": "seo_quality",            "label": "SEO Quality",            "icon": "🔍", "description": "Search optimization potential"},
    {"key": "engagement_prediction",  "label": "Engagement Prediction",  "icon": "💬", "description": "Predicted audience engagement"},
]

# ── Export Formats ─────────────────────────────────────────────────────────────
EXPORT_FORMATS = ["JSON", "ZIP", "DOCX"]

# --- PRO ADDITION: multi-channel adaptation targets ---
ADAPTATION_CHANNELS = [
    "B2B LinkedIn",
    "Gen-Z TikTok",
    "Parents Facebook",
]

# ── Output directory ───────────────────────────────────────────────────────────
# --- PRO ADDITION: shared output dir for images, videos, audio ---
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
OUTPUT_DIR.mkdir(exist_ok=True)
