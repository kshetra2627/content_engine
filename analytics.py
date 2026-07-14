"""Campaign scoring and AI insights."""
from config import ANALYTICS_METRICS
from prompts import build_insights_prompt
from providers import generate_text, parse_json_response

def score_campaign(brief: dict, results: dict, text_model: str) -> dict:
    scores  = _heuristic_scores(brief, results)
    sys_p, usr_p = build_insights_prompt(brief, results)
    raw     = generate_text(sys_p, usr_p, text_model, temperature=0.6, max_tokens=400)
    parsed  = _parse_insights(raw)
    return {"scores": scores, **parsed}

def _heuristic_scores(brief: dict, results: dict) -> dict:
    tg  = results.get("tg", "") or ""
    bl  = results.get("bl", "") or ""
    sc  = results.get("sc", {}) or {}
    tone = brief.get("brand_tone", "").lower()
    cta  = brief.get("call_to_action", "").lower()

    all_text = " ".join([tg, bl] + list(sc.values() if isinstance(sc, dict) else [])).lower()

    # brand_consistency: tone keywords present
    tone_words = {"playful":["fun","joy","smile","playful"],
                  "premium":["premium","luxury","crafted","exclusive"],
                  "eco-friendly":["eco","green","sustainable","planet"],
                  "professional":["professional","expert","solution","results"]}
    kws   = tone_words.get(tone, ["quality","great","best"])
    hits  = sum(1 for k in kws if k in all_text)
    brand = min(100, 50 + hits * 15)

    # creativity: tagline word uniqueness proxy
    tg_words = set(tg.lower().split())
    common   = {"the","a","an","and","or","for","to","with","of","in","is","are","your","our"}
    unique   = tg_words - common
    creative = min(100, 40 + len(unique) * 8)

    # marketing_effectiveness: CTA present
    cta_hit = 1 if cta and cta in all_text else 0
    mktg    = min(100, 55 + cta_hit * 20 + (10 if tg else 0) + (10 if bl else 0))

    # readability: avg sentence length proxy
    sentences = [s for s in bl.split(".") if s.strip()]
    avg_len   = (sum(len(s.split()) for s in sentences) / len(sentences)) if sentences else 20
    readability = max(30, min(100, int(110 - avg_len * 2)))

    # seo_quality: product name + keywords in content
    prod_kws  = brief.get("product_name", "").lower().split()
    seo_hits  = sum(1 for k in prod_kws if k in all_text)
    seo       = min(100, 45 + seo_hits * 15)

    # engagement: social post length balance
    sc_texts  = list(sc.values()) if isinstance(sc, dict) else []
    eng_score = 0
    for txt in sc_texts:
        words = len(str(txt).split())
        eng_score += 20 if 10 <= words <= 60 else 10
    engagement = min(100, 40 + (eng_score // max(1, len(sc_texts))))

    return {
        "brand_consistency":       brand,
        "creativity_score":        creative,
        "marketing_effectiveness": mktg,
        "readability":             readability,
        "seo_quality":             seo,
        "engagement_prediction":   engagement,
    }

def _parse_insights(raw: str) -> dict:
    d = parse_json_response(raw)
    return {
        "insights":     d.get("insight", raw[:300] if raw else ""),
        "suggestions":  d.get("suggestions", []),
        "alternatives": d.get("alternatives", []),
    }
