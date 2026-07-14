"""Dynamic prompt assembly — no hardcoded strings.

PRO additions in this file:
  - ENERGY_MAP: tone → energy instruction block (Part 7)
  - CRITIC_SYSTEM: self-critique prompt (Part 4)
  - SCRIPT_ADAPTER: voiceover script rewriter (Part 5)
  - ADAPT_SYSTEM: multi-channel adaptation (Part 6)
  - All generation prompts now include an energy-matching instruction block (Part 7)
"""
from config import TEXT_SETTINGS, SOCIAL_PLATFORMS


# ══════════════════════════════════════════════════════════════════════════════
# --- PRO ADDITION: energy matching map (Part 7) ---
# Maps brand_tone → an explicit energy/intensity instruction that is injected
# into every text-generation prompt so tone is consistent across all assets.
# ══════════════════════════════════════════════════════════════════════════════
ENERGY_MAP: dict[str, str] = {
    "Playful":        "Use high-energy exclamatory language, casual phrasing, wordplay, and friendly contractions. Keep sentences short and punchy.",
    "Premium":        "Use elevated, measured language that signals quality. Avoid exclamation points. Favour latinate vocabulary and understated confidence.",
    "Eco-friendly":   "Use warm, nature-inspired language. Calm, optimistic energy. Avoid corporate jargon; lean into community and care.",
    "Professional":   "Use confident, no-nonsense language. No exclamation points. Clear declarative sentences. Measured, authoritative energy.",
    "Bold":           "Use direct, high-intensity language. Strong verbs, minimal filler. Commands over suggestions. Short sentences with impact.",
    "Minimalist":     "Say more with less. Short sentences, plain vocabulary, zero filler. Let white space and silence carry weight.",
    "Luxury":         "Use sensory, aspirational language. Slow, deliberate pacing. Rich adjectives, but never more than necessary.",
    "Friendly":       "Conversational and warm. Contract everything. Second-person ('you', 'your'). Light, approachable energy.",
    "Authoritative":  "Use formal, credentialed language. Cite or imply expertise. Confident assertions, no hedging.",
    "Inspirational":  "Use visionary, motivational language. Rhetorical questions, forward-looking statements. High emotional resonance.",
}

def _energy_block(brand_tone: str) -> str:
    """Return the energy-matching instruction for a given brand tone."""
    instruction = ENERGY_MAP.get(brand_tone, "Match the energy to the stated brand tone consistently.")
    return (
        f"\n\nTONE ENERGY RULE (apply to every sentence): brand_tone='{brand_tone}'. "
        f"{instruction} "
        "This energy must be consistent across tagline, blog, and social posts — "
        "do NOT let one asset read louder or quieter than the others."
    )


# ══════════════════════════════════════════════════════════════════════════════
# --- PRO ADDITION: CRITIC_SYSTEM (Part 4) ---
# Self-critique prompt. Returns structured JSON verdict for each text asset.
# Also checks cross-asset tone/energy consistency (Part 7 addition).
# ══════════════════════════════════════════════════════════════════════════════
CRITIC_SYSTEM = """
You are a senior content strategist reviewing campaign copy.

Grade each asset and return ONLY valid JSON — no prose, no markdown fences:
{
  "tagline": { "pass": true|false, "issue": "<string or null>" },
  "blog":    { "pass": true|false, "issue": "<string or null>" },
  "social":  { "pass": true|false, "issue": "<string or null>" },
  "cross_asset_tone": { "pass": true|false, "issue": "<string or null>" }
}

Fail an asset if ANY of:
- tone mismatch: the copy's energy/register does not match the stated brand_tone
- audience ignored: language, vocabulary, or references don't suit target_audience
- length exceeded: tagline > 10 words, blog intro > 500 words
- product description contradicted: makes claims not supported by the product brief

Fail cross_asset_tone if:
- the three assets are not at a consistent energy level (e.g. tagline is bold/exclamatory
  but blog is formal and flat, or social is jokey while tagline is solemn)

Set "issue" to a concise one-sentence fix instruction when pass=false, null when pass=true.
""".strip()


# ══════════════════════════════════════════════════════════════════════════════
# --- PRO ADDITION: SCRIPT_ADAPTER (Part 5) ---
# Rewrites the blog intro as a TTS-ready voiceover script.
# ══════════════════════════════════════════════════════════════════════════════
SCRIPT_ADAPTER = """
Rewrite the provided blog intro as a voiceover script for a promotional video.
Rules:
- Add commas for natural breath pauses, ellipses (...) for dramatic pauses.
- Maximum 15 words per sentence. Break longer sentences.
- Remove all visual references (e.g. "as you can see", "shown above").
- No markdown, no bullet points, no stage directions. Output spoken text only.
- Preserve the brand tone and energy of the original exactly.
""".strip()


# ══════════════════════════════════════════════════════════════════════════════
# --- PRO ADDITION: ADAPT_SYSTEM (Part 6) ---
# Multi-channel text adaptation. Images and videos are NOT regenerated.
# ══════════════════════════════════════════════════════════════════════════════
ADAPT_SYSTEM = """
You are a channel strategist. Rewrite the provided campaign assets for the target channel.
Adapt tone, vocabulary, sentence length, emoji usage, and hashtag density to suit the channel's audience.
Return ONLY valid JSON with exactly these keys:
{ "tagline": "...", "blog": "...", "social": { ...same platform keys as input... } }

Channel behaviour guidelines:
- B2B LinkedIn: professional, insight-led, no emoji, 3-5 hashtags, longer sentences OK.
- Gen-Z TikTok: casual slang, high emoji density, ultra-short sentences, 5-7 hashtags, energetic hooks.
- Parents Facebook: warm and practical, 1-2 emoji per post, benefit-focused, relatable language.
""".strip()


# ══════════════════════════════════════════════════════════════════════════════
# Prompt builders
# ══════════════════════════════════════════════════════════════════════════════

def build_image_prompt(brief: dict, img_specs: dict) -> str:
    parts = []
    style = img_specs.get("visual_style", "")
    mood  = img_specs.get("mood", "")
    light = img_specs.get("lighting", "")
    subj  = img_specs.get("subject_focus", "Product Only")
    bg    = img_specs.get("background", "")
    angle = img_specs.get("camera_angle", "")
    comp  = img_specs.get("composition", "")
    color = img_specs.get("color_theme", "")
    qual  = img_specs.get("image_quality", "hd")
    detail= img_specs.get("detail_level", "Moderate")
    neg   = img_specs.get("neg_prompt", "")
    custom= img_specs.get("custom_instructions", "")

    desc  = brief.get("product_description") or brief.get("product_name", "product")
    tone  = brief.get("brand_tone", "Professional")
    goal  = brief.get("campaign_goal", "Brand Awareness")

    if style:  parts.append(f"{style} style")
    if mood:   parts.append(f"{mood} mood")
    if light:  parts.append(f"{light} lighting")
    parts.append(f"featuring {desc}")
    if subj:   parts.append(f"subject: {subj}")
    if bg:     parts.append(f"background: {bg}")
    if angle:  parts.append(f"camera angle: {angle}")
    if comp:   parts.append(f"composition: {comp}")
    if color:  parts.append(f"color theme: {color}")
    parts.append(f"brand tone: {tone}, goal: {goal}")
    parts.append(f"{detail} detail, {qual} quality")
    parts.append("no text overlays, no logos")
    if custom: parts.append(custom)

    prompt = ", ".join(p for p in parts if p)
    if neg:
        prompt += f". Avoid: {neg}"
    return prompt


def build_tagline_prompt(brief: dict, text_settings: dict,
                          critic_feedback: str = "") -> tuple:
    """Build tagline system/user prompts.

    --- PRO ADDITION (Part 7): energy block injected into system prompt.
    --- PRO ADDITION (Part 4): optional critic_feedback injected into user prompt.
    """
    tone   = brief.get("brand_tone", "Professional")
    goal   = brief.get("campaign_goal", "Brand Awareness")
    prod   = brief.get("product_name", "the product")
    aud    = brief.get("target_audience", "customers")
    cta    = brief.get("call_to_action", "")
    e_tone = text_settings.get("emotional_tone", "Positive")
    cta_s  = text_settings.get("cta_style", "Direct")

    energy = _energy_block(tone)  # --- PRO ADDITION: energy matching ---

    sys = (
        f"You are a creative director. Write ONE tagline — max 10 words. "
        f"Tone: {tone}. Emotional register: {e_tone}. CTA style: {cta_s}. "
        f"No hashtags. No quotes.{energy}"
    )
    usr = (
        f"Product: {prod}\nAudience: {aud}\nGoal: {goal}"
        + (f"\nCTA: {cta}" if cta else "")
        + (f"\n\nCRITIC FEEDBACK TO FIX: {critic_feedback}" if critic_feedback else "")
    )
    return sys, usr


def build_blog_prompt(brief: dict, text_settings: dict, tagline: str,
                       critic_feedback: str = "") -> tuple:
    """Build blog system/user prompts.

    --- PRO ADDITION (Part 7): energy block injected.
    --- PRO ADDITION (Part 4): optional critic_feedback injected.
    """
    prod    = brief.get("product_name", "the product")
    aud     = brief.get("target_audience", "readers")
    tone    = brief.get("brand_tone", "Professional")
    lang    = brief.get("language", "English")
    length  = text_settings.get("output_length", "Standard")
    words   = TEXT_SETTINGS["output_length"].get(length, 150)
    style   = text_settings.get("writing_style", "Storytelling")
    level   = text_settings.get("reading_level", "High School")
    formal  = text_settings.get("formality", "Neutral")
    emoji   = text_settings.get("emoji_usage", "None")

    energy = _energy_block(tone)  # --- PRO ADDITION: energy matching ---

    sys = (
        f"You are a content strategist writing for {aud}. "
        f"Writing style: {style}. Reading level: {level}. Formality: {formal}. "
        f"Emoji usage: {emoji}. Language: {lang}.{energy}"
    )
    usr = (
        f"Write a {words}-word blog introduction for {prod}. "
        f"Brand tone: {tone}."
        + (f" Weave in this tagline: \"{tagline}\"." if tagline else "")
        + (f"\n\nCRITIC FEEDBACK TO FIX: {critic_feedback}" if critic_feedback else "")
    )
    return sys, usr


def build_social_prompt(brief: dict, text_settings: dict, platforms: list,
                         critic_feedback: str = "") -> tuple:
    """Build social posts system/user prompts.

    --- PRO ADDITION (Part 7): energy block injected.
    --- PRO ADDITION (Part 4): optional critic_feedback injected.
    """
    prod   = brief.get("product_name", "the product")
    aud    = brief.get("target_audience", "customers")
    tone   = brief.get("brand_tone", "Professional")
    goal   = brief.get("campaign_goal", "Brand Awareness")
    cta    = brief.get("call_to_action", "")
    emoji  = text_settings.get("emoji_usage", "Minimal")
    htags  = text_settings.get("hashtag_usage", "Few (3-5)")
    cta_s  = text_settings.get("cta_style", "Direct")
    lang   = brief.get("language", "English")

    plat_instructions = []
    for p in platforms:
        cfg = SOCIAL_PLATFORMS.get(p, {})
        lim = cfg.get("char_limit", 280)
        plat_instructions.append(f'"{p}": max {lim} chars')

    energy = _energy_block(tone)  # --- PRO ADDITION: energy matching ---

    sys = (
        f"Output ONLY valid JSON. Keys: {', '.join(platforms)}. "
        f"Language: {lang}. Emoji usage: {emoji}. Hashtags: {htags}. "
        f"CTA style: {cta_s}.{energy}"
    )
    usr = (
        f"Create social posts for {prod} targeting {aud}. "
        f"Tone: {tone}. Goal: {goal}. CTA: {cta}. "
        f"Constraints: {'; '.join(plat_instructions)}."
        + (f"\n\nCRITIC FEEDBACK TO FIX: {critic_feedback}" if critic_feedback else "")
    )
    return sys, usr


def build_video_prompt(brief: dict, vid_specs: dict) -> str:
    motion  = vid_specs.get("motion_style", "Cinematic")
    cam     = vid_specs.get("camera_movement", "Push In")
    cine    = vid_specs.get("cinematic_style", "Commercial")
    subj_m  = vid_specs.get("subject_motion", "None")
    bg_m    = vid_specs.get("background_motion", "Static")
    intens  = vid_specs.get("motion_intensity", "Medium")
    extra   = vid_specs.get("additional_instructions", "")
    prod    = brief.get("product_name", "product")

    parts = [
        f"{motion} motion",
        f"camera: {cam}",
        f"{cine} cinematic style",
        f"subject motion: {subj_m}",
        f"background: {bg_m}",
        f"intensity: {intens}",
        f"featuring {prod}",
    ]
    if extra: parts.append(extra)
    return ", ".join(parts)


def build_insights_prompt(brief: dict, results: dict) -> tuple:
    prod = brief.get("product_name", "the product")
    tg   = results.get("tg", "")
    bl   = results.get("bl", "")
    sys  = (
        "You are a senior marketing strategist. Analyze the campaign content and provide: "
        "1) 2-sentence overall insight, 2) 3 specific improvement suggestions as a JSON list, "
        "3) 2 alternative creative directions as a JSON list. "
        "Output ONLY valid JSON with keys: insight, suggestions, alternatives."
    )
    usr  = f"Product: {prod}\nTagline: {tg}\nBlog intro: {bl[:300]}"
    return sys, usr


# --- PRO ADDITION: critic prompt builder (Part 4) ---
def build_critic_prompt(brief: dict, results: dict) -> str:
    """Build the user-facing message for the critic call."""
    return (
        f"Product: {brief.get('product_name', '')}\n"
        f"Brand tone: {brief.get('brand_tone', '')}\n"
        f"Target audience: {brief.get('target_audience', '')}\n"
        f"Product description: {brief.get('product_description', '')}\n\n"
        f"TAGLINE:\n{results.get('tg', '')}\n\n"
        f"BLOG INTRO:\n{results.get('bl', '')}\n\n"
        f"SOCIAL POSTS:\n{results.get('sc', '')}"
    )


# --- PRO ADDITION: voiceover script prompt builder (Part 5) ---
def build_voiceover_prompt(blog_text: str) -> tuple:
    """Return (system, user) tuple for the script-adapter call."""
    return SCRIPT_ADAPTER, f"Rewrite this blog intro as a voiceover script:\n\n{blog_text}"


# --- PRO ADDITION: channel adaptation prompt builder (Part 6) ---
def build_adapt_prompt(channel: str, tagline: str, blog: str, social: dict) -> tuple:
    """Return (system, user) tuple for a channel-adaptation call."""
    import json as _json
    usr = (
        f"Channel: {channel}\n\n"
        f"1. Tagline: {tagline}\n"
        f"2. Blog: {blog}\n"
        f"3. Social: {_json.dumps(social, ensure_ascii=False)}\n\n"
        "Rewrite all three assets for this channel. "
        "Return JSON with keys: tagline, blog, social."
    )
    return ADAPT_SYSTEM, usr


def get_temperature(text_settings: dict) -> float:
    level = text_settings.get("creativity", "Medium")
    return TEXT_SETTINGS["creativity"].get(level, 0.7)


def get_max_tokens(text_settings: dict) -> int:
    length = text_settings.get("output_length", "Standard")
    words  = TEXT_SETTINGS["output_length"].get(length, 150)
    return max(200, words * 2)
