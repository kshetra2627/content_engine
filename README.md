# 🚀 AI Marketing Platform

> Generate complete AI-powered marketing campaigns from a single brief.

A modern **Streamlit** application that creates end-to-end marketing content using multiple AI models. In just one click, generate compelling taglines, engaging blog introductions, platform-specific social media posts, AI-generated hero images, promotional videos, and campaign analytics.

Designed with a premium dark interface, customizable prompt engineering, and export capabilities, this platform serves as an all-in-one AI marketing assistant.

---

## 📸 Preview

> Add your screenshots below.

### Dashboard

![Dashboard](https://github.com/user-attachments/assets/9ba71483-1794-4489-b2bc-a082cdd27bca)

### Generated Campaign

![Campaign](https://github.com/user-attachments/assets/92b07ee2-04a6-4bad-aba3-94ee5602c242)

### Analytics

![Analytics](https://github.com/user-attachments/assets/59ede30d-a7fc-424c-966e-74c5fe5dc430)

---

# ✨ Features

### 🎯 Complete Campaign Generation

Generate an entire marketing campaign from a single prompt:

- ✍️ Brand Tagline
- 📝 Blog Introduction
- 📱 Social Media Posts
- 🖼️ AI Hero Image
- 🎥 Promotional Video

---

### 🧠 Prompt Engineering

- Live prompt preview
- Modify prompts before generation
- Dynamic prompt assembly
- Easily extendable templates

---

### ⚙️ Fully Configurable

Everything is controlled through `config.py`.

Configure:

- AI Models
- Social Platforms
- Writing Tones
- Languages
- Image Styles
- Video Settings
- Analytics Metrics

No UI modifications required.

---

### 📊 Campaign Analytics

Automatically evaluates every campaign using heuristic scoring.

Includes:

- Readability
- Engagement
- CTA Strength
- Platform Suitability
- AI-generated Improvement Suggestions

---

### 📂 Campaign History

- Save campaigns
- Reload previous campaigns
- Search history
- Compare outputs

---

### 📤 Export Options

Download campaigns as:

- JSON
- DOCX
- ZIP (including generated assets)

---

### 🎨 Premium UI

Built with Streamlit featuring:

- Dark Theme
- Glassmorphism Cards
- Responsive Layout
- Inter Typography
- Modern Dashboard Design

---

# 🏗️ Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Streamlit |
| Text Generation | Groq (Llama 3.3 70B) |
| Image Generation | Pollinations AI |
| Video Generation | Replicate (Wan 2.2 Fast) |
| Prompt Engine | Custom Dynamic Prompt Builder |
| Analytics | Custom Heuristic + AI Insights |

---

# 📁 Project Structure

```
contentengine/
│
├── app.py                # Streamlit UI
├── config.py             # Configurations
├── prompts.py            # Prompt Builder
├── providers.py          # AI Providers
├── analytics.py          # Campaign Analytics
├── export_utils.py       # Export Functions
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/contentengine.git
cd contentengine
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_groq_key
REPLICATE_API_TOKEN=your_replicate_key
```

> Pollinations AI requires no API key.

---

## 4. Launch Application

```bash
streamlit run app.py
```

Visit:

```
http://localhost:8501
```

---

# 🔑 API Keys

| Provider | Purpose | Free Tier |
|----------|---------|-----------|
| Groq | Text Generation | ✅ Yes |
| Pollinations AI | Image Generation | ✅ No API Key Required |
| Replicate | Video Generation | ✅ $5 Free Credits |

---

# ⚙️ Configuration

Almost every feature is configurable via `config.py`.

You can easily customize:

- Supported Models
- Writing Styles
- Languages
- Target Platforms
- Image Specifications
- Video Models
- Analytics Rules

Example:

```python
TEXT_MODELS = {
    "llama-3.3-70b-versatile": "Llama 3.3 70B",
    "your-model": "Custom Model"
}
```

---

# 📈 Workflow

```
Campaign Brief
      │
      ▼
Prompt Builder
      │
      ▼
 AI Providers
 ├── Groq
 ├── Pollinations
 └── Replicate
      │
      ▼
Generated Assets
      │
      ▼
Analytics Engine
      │
      ▼
Export / History
```

---

# 💡 Future Improvements

- Multi-language support
- Email campaign generation
- Landing page copy generation
- SEO keyword optimization
- Brand voice training
- Team collaboration
- Campaign scheduling
- Performance prediction

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future development.
