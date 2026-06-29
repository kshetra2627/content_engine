# AI Marketing Platform

A professional AI-powered marketing campaign generator built with Streamlit. Generate taglines, blog intros, social media posts, hero images, and promotional videos from a single campaign brief.

![Dark dashboard UI](https://image.pollinations.ai/prompt/dark%20SaaS%20dashboard%20UI%20screenshot%20AI%20marketing%20platform%20teal%20accent?width=1200&height=630&nologo=true)

---

## Features

- **Full campaign generation** — tagline, blog intro, social posts, hero image, and video in one click
- **Configurable everything** — all options, models, tones, specs, and platforms defined in `config.py`
- **Prompt engineering panel** — preview and edit prompts before generation
- **Campaign history** — save, search, and reload previous campaigns
- **Analytics dashboard** — heuristic scores + AI-generated insights for each campaign
- **Export** — download as JSON, ZIP (with all assets), or DOCX
- **Dark premium UI** — Inter font, teal accent, glassmorphism cards

---

## Tech Stack

| Layer | Provider |
|---|---|
| Text generation | [Groq](https://console.groq.com) — Llama 3.3 70B (free tier) |
| Image generation | [Pollinations.AI](https://pollinations.ai) — completely free, no key |
| Video generation | [Replicate](https://replicate.com) — Wan 2.2 Fast ($5 free credits) |
| UI | [Streamlit](https://streamlit.io) |

---

## Quick Start

### 1. Clone and install

```bash
git clone <your-repo-url>
cd contentengine
pip install -r requirements.txt
```

### 2. Configure API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=gsk_...          # https://console.groq.com — free
REPLICATE_API_TOKEN=r8_...    # https://replicate.com — $5 free credits
```

> **Image generation works without any key** — Pollinations.AI is fully free.

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Getting API Keys

| Key | Where to get | Cost |
|---|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys | Free (14,400 req/day) |
| `REPLICATE_API_TOKEN` | [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) | $5 free on signup |

---

## Project Structure

```
contentengine/
├── app.py              # Streamlit dashboard (UI only)
├── config.py           # All options, models, fields — edit here to extend
├── prompts.py          # Dynamic prompt assembly
├── providers.py        # API calls (Groq, Pollinations, Replicate)
├── analytics.py        # Campaign scoring + AI insights
├── export_utils.py     # JSON / ZIP / DOCX export
├── requirements.txt
├── .env                # Your API keys (never committed)
└── .env.example        # Template
```

---

## Extending the Platform

Everything is data-driven. No UI changes needed to add new options:

**Add a new text model** — edit `TEXT_MODELS` in `config.py`:
```python
TEXT_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B",
    "my-new-model-id": "My New Model",   # ← just add here
}
```

**Add a new social platform** — edit `SOCIAL_PLATFORMS` in `config.py`:
```python
SOCIAL_PLATFORMS = {
    ...
    "threads": {"label": "Threads", "color": "#F1F5F9", "char_limit": 500, ...},
}
```

**Add a new image style** — edit `IMAGE_SPECS["visual_style"]` in `config.py`.

**Add a new analytics metric** — add to `ANALYTICS_METRICS` in `config.py` and implement scoring in `analytics.py`.

---

## License

MIT
