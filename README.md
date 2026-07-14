# 🚀 Content Engine Pro

> Generate complete AI-powered marketing campaigns from a single brief — with self-critique, voiceover, multi-channel adaptation, and swappable providers.

A modern **Streamlit** application that creates end-to-end marketing content using multiple AI models. In one click, generate taglines, blog introductions, platform-specific social posts, AI hero images, promotional videos, voiceover audio, and campaign analytics.

---

## ✨ Pro Features (v2)

| Feature | What it does |
|---------|-------------|
| **Self-Critique Loop** | After text generation a critic LLM grades each asset. Failing assets are auto-regenerated (up to 2 retries). A visible warning flag is shown if quality still doesn't pass. |
| **Voiceover Generation** | The blog intro is adapted into a TTS-ready script then synthesised to MP3 via OpenAI TTS. An audio player renders inline. |
| **Multi-Channel Adaptation** | A dropdown lets you rewrite text for B2B LinkedIn, Gen-Z TikTok, or Parents Facebook — without regenerating images or video. |
| **Energy Matching** | Every generation prompt injects a tone-energy rule block so all assets (tagline, blog, social) read at the same intensity level. |
| **OpenAI Image Generation** | Replaced Pollinations with DALL-E 3 / gpt-image-1 for dramatically better prompt adherence and quality. |
| **OpenRouter Video** | Video generation now routes through OpenRouter's unified `/api/v1/videos` API (Wan 2.7, Veo 3.1, Kling, etc.) with Replicate as a fallback. Swappable via `VIDEO_PROVIDER` env var. |
| **Zero hardcoded secrets** | Every credential and mutable model ID lives in `.env`. Sample campaign data moved to `default_campaign.json`. |

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in your keys.

### Required

| Variable | Purpose |
|----------|---------|
| `GROQ_API_KEY` | Text generation (Groq — free tier available) |
| `OPENAI_API_KEY` | Image generation (DALL-E 3) **and** TTS voiceover |

### Required for video

| Variable | Purpose | When needed |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Video via OpenRouter (default) | `VIDEO_PROVIDER=openrouter` |
| `REPLICATE_API_TOKEN` | Video via Replicate (fallback) | `VIDEO_PROVIDER=replicate` or as fallback |

### Optional overrides

| Variable | Default | Notes |
|----------|---------|-------|
| `VIDEO_PROVIDER` | `openrouter` | `"openrouter"` or `"replicate"` |
| `IMAGE_MODEL` | `dall-e-3` | `"dall-e-3"` or `"gpt-image-1"` |
| `TEXT_MODEL_DEFAULT` | `llama-3.3-70b-versatile` | Any Groq model ID |
| `OPENROUTER_VIDEO_MODEL` | `alibaba/wan-2.7` | Any OpenRouter video model slug |
| `REPLICATE_VIDEO_MODEL` | `wan-video/wan-2.2-i2v-fast` | Any Replicate video model |
| `GROQ_API_BASE` | `https://api.groq.com/openai/v1` | Override for self-hosted proxy |
| `OPENAI_API_BASE` | `https://api.openai.com/v1` | Override for self-hosted proxy |
| `OPENROUTER_API_BASE` | `https://openrouter.ai/api/v1` | Override for self-hosted proxy |
| `OUTPUT_DIR` | `output` | Directory for generated images, videos, audio |

---

## 🎬 Video Provider Decision (Part 3)

**OpenRouter is the default video backend** (`VIDEO_PROVIDER=openrouter`).

OpenRouter launched a unified video generation API in April 2026 (`POST /api/v1/videos`) that supports image-to-video via `frame_images`, normalises parameters across providers, and gives access to top-tier models under a single key:

| Model slug | Capability |
|-----------|------------|
| `alibaba/wan-2.7` | Image-to-video, up to 1080p, 5–10s **(default)** |
| `google/veo-3.1-fast` | Text+image, 720p/1080p, native audio |
| `kwaivgi/kling-v3.0-pro` | Image-to-video, 3–15s, 16:9/9:16/1:1 |
| `minimax/hailuo-2.3` | Cinematic image-to-video |
| `bytedance/seedance-2.0` | Strong character consistency |

**Replicate remains as a fallback.** If `OPENROUTER_API_KEY` is missing or the OpenRouter call fails, the app automatically retries with Replicate's Wan 2.2. Set `VIDEO_PROVIDER=replicate` to force Replicate permanently.

---

## 🚀 Getting Started

```bash
git clone https://github.com/yourusername/content-engine-pro.git
cd content-engine-pro
pip install -r requirements.txt
cp .env.example .env        # fill in your keys
streamlit run app.py
```

Visit `http://localhost:8501`

---

## 📁 Project Structure

```
content_engine/
├── app.py                  # Streamlit UI (Pro: critic UI, voiceover player, channel adaptation)
├── config.py               # All config — env-sourced, no hardcoded secrets
├── providers.py            # API calls: Groq text, OpenAI image+TTS, OpenRouter/Replicate video
├── prompts.py              # Prompt builders + CRITIC_SYSTEM, SCRIPT_ADAPTER, ADAPT_SYSTEM
├── analytics.py            # Heuristic + AI campaign scoring
├── export_utils.py         # JSON / ZIP / DOCX export
├── image_gen.py            # Standalone image helper (wraps providers)
├── video_gen.py            # Standalone video helper (wraps providers)
├── text_gen.py             # Standalone text helper (wraps providers)
├── check_free_video.py     # HuggingFace space prober (URLs in config list)
├── default_campaign.json   # Editable campaign brief defaults (no sample data in code)
├── .env.example            # Template — copy to .env
├── requirements.txt
└── README.md
```

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Text Generation | Groq (Llama 3.3 70B) |
| Image Generation | OpenAI DALL-E 3 / gpt-image-1 |
| Voiceover TTS | OpenAI TTS (tts-1) |
| Video Generation | OpenRouter (Wan 2.7 default) + Replicate fallback |
| Self-Critique | Groq LLM critic loop |
| Channel Adaptation | Groq LLM rewriter |
| Analytics | Custom heuristic + AI insights |

---

## 📊 Workflow

```
Campaign Brief
      │
      ▼
Prompt Builder (energy-matched)
      │
      ▼
 AI Providers
 ├── Groq → Tagline + Blog + Social
 │         └── Critic Loop (auto-retry up to 2×)
 │         └── Script Adapter → OpenAI TTS → .mp3
 ├── OpenAI → Hero Image (DALL-E 3)
 └── OpenRouter → Promotional Video (Wan 2.7)
      │
      ▼
Channel Adaptation (optional, text only)
      │
      ▼
Analytics + Export (JSON / ZIP / DOCX)
```

---

## 🔬 Hardest Part & What RAG / Agents Would Improve

**Hardest addition: the self-critique loop (Part 4).**

Reliably getting the critic to emit parseable, actionable JSON verdicts — especially the `cross_asset_tone` check — required careful prompt engineering and a forgiving JSON extractor. The critic sometimes conflates tone issues with length issues, producing vague `issue` strings that aren't useful for re-generation.

**RAG (Day 4) would improve it** by grounding the critic against a brand-voice knowledge base. Instead of inferring what "Premium" tone means from the brief alone, the critic could retrieve documented brand guidelines, competitor examples, or approved copy snippets and compare against those concrete references — producing much more precise, actionable verdicts.

**Agents (Day 6) would improve the full pipeline** by turning the generate → critique → regenerate loop into a proper tool-calling agent that can decide how many retries to attempt, when to escalate to a human, and which specific part of a failing asset to fix — rather than regenerating the entire asset on every retry.

---

## 📄 License

MIT
