"""Central configuration — all options, models, and settings live here."""
import os
from dotenv import load_dotenv
load_dotenv()

# ── API Keys ───────────────────────────────────────────────────────────────────
GROQ_KEY      = os.getenv("GROQ_API_KEY", "")
REPLICATE_KEY = os.getenv("REPLICATE_API_TOKEN", "")
MAX_RETRIES   = 3
PROMPT_HISTORY_LIMIT = 20

# ── Models ─────────────────────────────────────────────────────────────────────
TEXT_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B (Default)",
    "llama-3.1-8b-instant":    "Llama 3.1 8B (Fast)",
    "mixtral-8x7b-32768":      "Mixtral 8x7B",
    "gemma2-9b-it":            "Gemma 2 9B",
}
IMAGE_MODELS = {
    "pollinations": "Pollinations AI (Free)",
}
VIDEO_MODELS = {
    "wan-video/wan-2.2-i2v-fast": "Wan 2.2 Fast (Replicate)",
    "wan-video/wan-2.5-i2v-fast": "Wan 2.5 Fast (Replicate)",
}

# ── Campaign Brief Fields ──────────────────────────────────────────────────────
CAMPAIGN_FIELDS = [
    {"key": "product_name",        "label": "Product Name",        "type": "text",     "default": "EcoBottle Pro", "required": True},
    {"key": "product_category",    "label": "Product Category",    "type": "select",   "default": "Consumer Goods",
     "options": ["Consumer Goods","SaaS","E-commerce","Healthcare","Finance","Education","Food & Beverage","Fashion","Travel","Real Estate","Technology","Other"]},
    {"key": "product_description", "label": "Product Description", "type": "textarea", "default": "A premium eco-friendly reusable water bottle.", "required": True},
    {"key": "target_audience",     "label": "Target Audience",     "type": "text",     "default": "Eco-conscious professionals", "required": True},
    {"key": "brand_tone",          "label": "Brand Tone",          "type": "select",   "default": "Professional",
     "options": ["Playful","Premium","Eco-friendly","Professional","Bold","Minimalist","Luxury","Friendly","Authoritative","Inspirational"]},
    {"key": "campaign_goal",       "label": "Campaign Goal",       "type": "select",   "default": "Brand Awareness",
     "options": ["Brand Awareness","Lead Generation","Product Launch","Sales Conversion","Customer Retention","Event Promotion","App Downloads"]},
    {"key": "industry",            "label": "Industry",            "type": "select",   "default": "Technology",
     "options": ["Technology","Healthcare","Finance","Retail","Education","Food","Travel","Real Estate","Entertainment","Other"]},
    {"key": "target_region",       "label": "Target Region",       "type": "select",   "default": "Global",
     "options": ["Global","North America","Europe","Asia Pacific","Latin America","Middle East","Africa"]},
    {"key": "language",            "label": "Language",            "type": "select",   "default": "English",
     "options": ["English","Spanish","French","German","Portuguese","Arabic","Hindi","Chinese","Japanese"]},
    {"key": "call_to_action",      "label": "Call to Action",      "type": "text",     "default": "Learn More"},
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
    "aspect_ratio":      ["16:9","1:1","9:16","4:3","3:2"],
    "image_quality":     ["Standard","High","Ultra"],
    "detail_level":      ["Minimal","Moderate","Highly Detailed"],
}

# ── Video Specs ────────────────────────────────────────────────────────────────
VIDEO_SPECS = {
    "duration":          ["3s","5s","8s","10s"],
    "motion_style":      ["Cinematic","Dynamic","Subtle","Dramatic","Smooth","Energetic"],
    "camera_movement":   ["Static","Push In","Pull Out","Pan Left","Pan Right","Tilt Up","Tilt Down","Orbit","Handheld"],
    "subject_motion":    ["None","Walk","Run","Dance","Gesture","Idle"],
    "background_motion": ["Static","Parallax","Flowing","Bokeh Shift"],
    "cinematic_style":   ["Hollywood","Documentary","Commercial","Music Video","Social Media"],
    "resolution":        ["480p","720p","1080p"],
    "motion_intensity":  ["Low","Medium","High"],
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
