"""Dynamic prompt assembly — no hardcoded strings."""
from config import TEXT_SETTINGS, SOCIAL_PLATFORMS

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
    qual  = img_specs.get("image_quality", "High")
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
        prompt += f" --no {neg}"
    return prompt

def build_tagline_prompt(brief: dict, text_settings: dict) -> tuple:
    tone   = brief.get("brand_tone", "Professional")
    goal   = brief.get("campaign_goal", "Brand Awareness")
    prod   = brief.get("product_name", "the product")
    aud    = brief.get("target_audience", "customers")
    cta    = brief.get("call_to_action", "")
    e_tone = text_settings.get("emotional_tone", "Positive")
    cta_s  = text_settings.get("cta_style", "Direct")

    sys = (f"You are a creative director. Write ONE tagline — max 10 words. "
           f"Tone: {tone}. Emotional register: {e_tone}. CTA style: {cta_s}. No hashtags. No quotes.")
    usr = (f"Product: {prod}\nAudience: {aud}\nGoal: {goal}"
           + (f"\nCTA: {cta}" if cta else ""))
    return sys, usr

def build_blog_prompt(brief: dict, text_settings: dict, tagline: str) -> tuple:
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

    sys = (f"You are a content strategist writing for {aud}. "
           f"Writing style: {style}. Reading level: {level}. Formality: {formal}. "
           f"Emoji usage: {emoji}. Language: {lang}.")
    usr = (f"Write a {words}-word blog introduction for {prod}. "
           f"Brand tone: {tone}."
           + (f" Weave in this tagline: \"{tagline}\"." if tagline else ""))
    return sys, usr

def build_social_prompt(brief: dict, text_settings: dict, platforms: list) -> tuple:
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

    sys = (f"Output ONLY valid JSON. Keys: {', '.join(platforms)}. "
           f"Language: {lang}. Emoji usage: {emoji}. Hashtags: {htags}. CTA style: {cta_s}.")
    usr = (f"Create social posts for {prod} targeting {aud}. "
           f"Tone: {tone}. Goal: {goal}. CTA: {cta}. "
           f"Constraints: {'; '.join(plat_instructions)}.")
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
    sys  = ("You are a senior marketing strategist. Analyze the campaign content and provide: "
            "1) 2-sentence overall insight, 2) 3 specific improvement suggestions as a JSON list, "
            "3) 2 alternative creative directions as a JSON list. "
            "Output ONLY valid JSON with keys: insight, suggestions, alternatives.")
    usr  = (f"Product: {prod}\nTagline: {tg}\nBlog intro: {bl[:300]}")
    return sys, usr

def get_temperature(text_settings: dict) -> float:
    level = text_settings.get("creativity", "Medium")
    return TEXT_SETTINGS["creativity"].get(level, 0.7)

def get_max_tokens(text_settings: dict) -> int:
    length = text_settings.get("output_length", "Standard")
    words  = TEXT_SETTINGS["output_length"].get(length, 150)
    return max(200, words * 2)
