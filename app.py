"""AI Marketing Platform — Professional Dashboard."""
import streamlit as st, time, os, json
from config import (CAMPAIGN_FIELDS, IMAGE_SPECS, VIDEO_SPECS, TEXT_SETTINGS,
                    SOCIAL_PLATFORMS, ANALYTICS_METRICS, EXPORT_FORMATS,
                    TEXT_MODELS, IMAGE_MODELS, VIDEO_MODELS,
                    GROQ_KEY, REPLICATE_KEY)
from prompts import (build_image_prompt, build_tagline_prompt, build_blog_prompt,
                     build_social_prompt, build_video_prompt, get_temperature, get_max_tokens)
from providers import generate_text, generate_image, generate_video, parse_json_response
from analytics import score_campaign
from export_utils import get_export_bytes

st.set_page_config(page_title="AI Marketing Platform", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*,*::before,*::after{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stMainBlockContainer"],section.main{
  background:#0D0F12!important;font-family:'Inter',sans-serif!important;color:#E2E8F0!important}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
[data-testid="stSidebar"]{background:#13161B!important;border-right:1px solid #1E2530!important;width:290px!important;min-width:290px!important}
[data-testid="stSidebar"]>div:first-child{padding:0!important}
[data-testid="stMainBlockContainer"]{padding:20px 24px!important}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{
  background:#1A1F28!important;border:1px solid #2A3140!important;color:#E2E8F0!important;border-radius:8px!important;font-size:13px!important}
[data-testid="stTextInput"] label,[data-testid="stTextArea"] label,[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,[data-testid="stCheckbox"] label{color:#94A3B8!important;font-size:12px!important}
[data-testid="stSelectbox"]>div>div{background:#1A1F28!important;border:1px solid #2A3140!important;color:#E2E8F0!important;border-radius:8px!important}
[data-testid="stSelectbox"] svg{fill:#94A3B8!important}
[data-testid="stCheckbox"]>label>div{background:#1A1F28!important;border-color:#2A3140!important}
[data-testid="stBaseButton-primary"]{background:linear-gradient(135deg,#0D9488,#14B8A6)!important;border:none!important;
  border-radius:8px!important;font-weight:600!important;font-size:13px!important;color:#fff!important;
  box-shadow:0 2px 12px rgba(20,184,166,.3)!important;transition:all .2s!important}
[data-testid="stBaseButton-secondary"]{background:#1A1F28!important;border:1px solid #2A3140!important;
  border-radius:8px!important;font-weight:500!important;font-size:12px!important;color:#94A3B8!important}
[data-testid="stExpander"]{background:#13161B!important;border:1px solid #1E2530!important;border-radius:12px!important}
[data-testid="stExpander"] summary{color:#94A3B8!important;font-size:12px!important;font-weight:600!important}
.stProgress>div>div{background:linear-gradient(90deg,#14B8A6,#0D9488)!important;border-radius:99px!important}
[data-testid="stColumns"]{gap:14px!important}
.card{background:#13161B;border-radius:16px;border:1px solid #1E2530;
  box-shadow:0 2px 16px rgba(0,0,0,.35);padding:20px;margin-bottom:14px;
  transition:box-shadow .2s,transform .2s}
.card:hover{box-shadow:0 4px 28px rgba(0,0,0,.5);transform:translateY(-1px)}
.lo{color:#F59E0B;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:5px}
.lp{color:#A78BFA;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:5px}
.lt{color:#2DD4BF;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:5px}
.st{font-size:15px;font-weight:600;color:#F1F5F9;margin:0 0 12px;display:flex;align-items:center;gap:7px}
.tg{font-size:21px;font-weight:700;color:#F1F5F9;line-height:1.35;margin:8px 0 0}
.meta{font-size:11px;color:#475569;margin-top:8px;display:flex;gap:14px;flex-wrap:wrap}
.cf{border-top:1px solid #1E2530;margin-top:14px;padding-top:10px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.badge{display:inline-flex;align-items:center;gap:4px;padding:2px 9px;border-radius:99px;font-size:11px;font-weight:500}
.bg{background:#1E2530;color:#94A3B8}
.bgr{background:#2D0F0F;color:#F87171;border:1px solid #5B1A1A}
.bgg{background:#052E1A;color:#34D399;border:1px solid #064E2B}
.bgt{background:#042F2E;color:#2DD4BF;border:1px solid #0F4F4B}
.bgtw{background:#0C1A2E;color:#60A5FA;border:1px solid #1E3A5F}
.bgi{background:#2D0A1E;color:#F472B6;border:1px solid #5B1035}
.bgl{background:#0C1A2E;color:#818CF8;border:1px solid #2D3570}
.pc{font-size:13px;color:#CBD5E1;background:#0D1117;border:1px solid #1E2530;border-radius:8px;padding:10px 12px;line-height:1.6;white-space:pre-wrap;margin-bottom:10px}
.vph{background:linear-gradient(135deg,#1E0A3C,#3B1D6E,#5B3599);border-radius:12px;height:200px;
  display:flex;align-items:center;justify-content:center;flex-direction:column;gap:10px}
.iph{background:linear-gradient(135deg,#0A1628,#0C2244,#0E3366);border-radius:12px;height:200px;
  display:flex;align-items:center;justify-content:center;font-size:44px}
.sb-logo{padding:20px 18px 14px;border-bottom:1px solid #1E2530}
.sb-sec{font-size:10px;font-weight:600;color:#475569;letter-spacing:.07em;text-transform:uppercase;margin-bottom:10px}
.nav-item{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:9px;margin-bottom:3px;
  font-size:13px;font-weight:500;color:#94A3B8}
.nav-item:hover{background:#1A2030;color:#2DD4BF}
.nav-icon{width:28px;height:28px;border-radius:7px;background:#1A2030;display:flex;align-items:center;justify-content:center;font-size:14px}
.sc{margin:0 14px 8px;background:linear-gradient(135deg,#052E1A,#064E2B);border:1px solid #065F46;
  border-radius:12px;padding:12px 14px;display:flex;align-items:flex-start;gap:10px}
.et{background:#1A0A0A;border:1px solid #5B1A1A;border-radius:12px;padding:14px 18px;margin-bottom:12px;
  display:flex;align-items:flex-start;gap:10px;box-shadow:0 4px 20px rgba(239,68,68,.1)}
</style>
""", unsafe_allow_html=True)

# ── session state ──────────────────────────────────────────────────────────────
_defaults = {
    "brief": {f["key"]: f.get("default", "") for f in CAMPAIGN_FIELDS},
    "results": {},
    "settings": {
        "text":  {k: (list(v.keys())[1] if isinstance(v, dict) else v[0]) for k, v in TEXT_SETTINGS.items()},
        "image": {k: v[0] for k, v in IMAGE_SPECS.items()} | {"neg_prompt": "", "custom_instructions": ""},
        "video": {k: v[0] for k, v in VIDEO_SPECS.items()} | {"additional_instructions": ""},
        "text_model":  list(TEXT_MODELS.keys())[0],
        "image_model": list(IMAGE_MODELS.keys())[0],
        "video_model": list(VIDEO_MODELS.keys())[0],
        "platforms":   [k for k, v in SOCIAL_PLATFORMS.items() if v["default_enabled"]],
        "brand": {"brand_name": "", "brand_colors": "", "brand_guidelines": ""},
    },
    "analytics": {},
    "prompt_history": [],
    "campaigns": [],
    "errors": [],
    "gen_time": None,
    "prompt_overrides": {},
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Generation Logic ───────────────────────────────────────────────────────────
def run_generation(modes: set):
    brief    = st.session_state.brief
    settings = st.session_state.settings
    t_sets   = settings["text"]
    i_specs  = settings["image"]
    v_specs  = settings["video"]
    t_model  = settings["text_model"]
    v_model  = settings["video_model"]
    platforms= settings["platforms"]
    temp     = get_temperature(t_sets)
    tokens   = get_max_tokens(t_sets)
    errors   = []
    t0       = time.time()

    # build prompts
    tg_sys, tg_usr = build_tagline_prompt(brief, t_sets)
    bl_sys, bl_usr = build_blog_prompt(brief, t_sets, st.session_state.results.get("tg", ""))
    sc_sys, sc_usr = build_social_prompt(brief, t_sets, platforms or ["twitter"])
    img_prompt     = build_image_prompt(brief, i_specs)
    vid_prompt     = build_video_prompt(brief, v_specs)

    # store in history
    entry = {"time": time.strftime("%H:%M"), "product": brief.get("product_name", ""),
             "tagline_prompt": tg_usr, "image_prompt": img_prompt}
    st.session_state.prompt_history = ([entry] + st.session_state.prompt_history)[:20]

    # apply overrides
    ov = st.session_state.prompt_overrides
    if ov.get("tagline_user"):  tg_usr  = ov["tagline_user"]
    if ov.get("blog_user"):     bl_usr  = ov["blog_user"]
    if ov.get("social_user"):   sc_usr  = ov["social_user"]
    if ov.get("image_prompt"):  img_prompt = ov["image_prompt"]

    do_all   = "all" in modes
    do_text  = do_all or "text"  in modes
    do_image = do_all or "image" in modes
    do_video = do_all or "video" in modes

    steps  = []
    if do_text:  steps += [("Tagline", 15), ("Blog", 30), ("Social", 45)]
    if do_image: steps += [("Image",   70)]
    if do_video: steps += [("Video",   90)]
    steps += [("Done", 100)]
    total  = len(steps)

    prog = st.progress(0, text="Starting…")

    if do_text:
        if not GROQ_KEY:
            errors.append(("Text Generation", "GROQ_API_KEY missing in .env"))
        else:
            prog.progress(15, text="Generating tagline…")
            tg = generate_text(tg_sys, tg_usr, t_model, temp, 60)
            st.session_state.results["tg"] = tg
            if not tg or "[Error" in tg:
                errors.append(("Tagline", "Generation failed — check Groq API key"))

            prog.progress(30, text="Writing blog…")
            bl_sys2, bl_usr2 = build_blog_prompt(brief, t_sets, tg)
            if ov.get("blog_user"): bl_usr2 = ov["blog_user"]
            bl = generate_text(bl_sys2, bl_usr2, t_model, temp, tokens)
            st.session_state.results["bl"] = bl
            if not bl or "[Error" in bl:
                errors.append(("Blog", "Generation failed"))

            prog.progress(45, text="Crafting social posts…")
            sc_raw = generate_text(sc_sys, sc_usr, t_model, temp, 600)
            sc = parse_json_response(sc_raw)
            if not sc:
                sc = {p: sc_raw[:SOCIAL_PLATFORMS[p]["char_limit"]] for p in (platforms or ["twitter"])}
                errors.append(("Social Posts", "JSON parse failed — raw text used"))
            st.session_state.results["sc"] = sc

    if do_image:
        prog.progress(70, text="Generating hero image…")
        ar = i_specs.get("aspect_ratio", "16:9")
        w, h = {"16:9": (1280,720), "1:1": (768,768), "9:16": (720,1280),
                "4:3": (1024,768), "3:2": (1080,720)}.get(ar, (1280,720))
        im = generate_image(img_prompt, i_specs.get("neg_prompt",""), w, h)
        st.session_state.results["im"] = im
        if not im:
            errors.append(("Hero Image", "Pollinations AI failed — try again"))

    if do_video:
        prog.progress(90, text="Rendering video…")
        if not REPLICATE_KEY:
            st.session_state.results["vd"] = None
            errors.append(("Video", "REPLICATE_API_TOKEN missing — add to .env"))
        else:
            dur_str = v_specs.get("duration", "5s")
            dur = int(dur_str.replace("s", ""))
            res = v_specs.get("resolution", "480p")
            vd = generate_video(st.session_state.results.get("im"), vid_prompt, v_model, res, dur)
            st.session_state.results["vd"] = vd
            if not vd:
                errors.append(("Video", "Replicate generation failed"))

    prog.progress(100, text="Scoring campaign…")
    if st.session_state.results and GROQ_KEY:
        st.session_state.analytics = score_campaign(brief, st.session_state.results, t_model)

    st.session_state.gen_time = f"{time.time()-t0:.1f}s"
    st.session_state.errors   = errors

    # save to campaign history
    camp = {"time": time.strftime("%Y-%m-%d %H:%M"), "brief": dict(brief),
            "results": dict(st.session_state.results), "analytics": dict(st.session_state.analytics)}
    st.session_state.campaigns = ([camp] + st.session_state.campaigns)[:10]

    time.sleep(0.3)
    prog.empty()
    st.rerun()


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#0D9488,#14B8A6);
                    display:flex;align-items:center;justify-content:center;font-size:16px;">✦</div>
        <div>
          <div style="font-size:15px;font-weight:700;color:#F1F5F9">AI Marketing Platform</div>
          <div style="font-size:11px;color:#64748B">Campaign Generation Suite</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    S = st.session_state.settings

    # Campaign Brief
    with st.expander("📋 Campaign Brief", expanded=True):
        for f in CAMPAIGN_FIELDS:
            key = f["key"]
            if f["type"] == "text":
                S["text"] if False else None  # just spacing
                val = st.text_input(f["label"], value=st.session_state.brief.get(key, f.get("default","")), key=f"cf_{key}")
            elif f["type"] == "select":
                opts = f["options"]
                cur  = st.session_state.brief.get(key, f.get("default", opts[0]))
                idx  = opts.index(cur) if cur in opts else 0
                val  = st.selectbox(f["label"], opts, index=idx, key=f"cf_{key}")
            elif f["type"] == "textarea":
                val  = st.text_area(f["label"], value=st.session_state.brief.get(key, f.get("default","")), height=68, key=f"cf_{key}")
            else:
                val = f.get("default", "")
            st.session_state.brief[key] = val

    # Text Settings
    with st.expander("✍️ Text Settings"):
        ts = S["text"]
        for key, opts in TEXT_SETTINGS.items():
            label = key.replace("_", " ").title()
            if isinstance(opts, dict):
                keys = list(opts.keys())
                cur  = ts.get(key, keys[1])
                idx  = keys.index(cur) if cur in keys else 0
                ts[key] = st.select_slider(label, keys, value=keys[idx], key=f"ts_{key}")
            else:
                cur = ts.get(key, opts[0])
                idx = opts.index(cur) if cur in opts else 0
                ts[key] = st.selectbox(label, opts, index=idx, key=f"ts_{key}")

    # Image Specs
    with st.expander("🖼️ Image Specs"):
        isp = S["image"]
        for key in ["visual_style","mood","lighting","subject_focus","background","camera_angle","composition","color_theme","aspect_ratio","image_quality","detail_level"]:
            opts = IMAGE_SPECS.get(key, [])
            cur  = isp.get(key, opts[0])
            idx  = opts.index(cur) if cur in opts else 0
            isp[key] = st.selectbox(key.replace("_"," ").title(), opts, index=idx, key=f"is_{key}")
        isp["neg_prompt"]          = st.text_input("Negative Prompt",      value=isp.get("neg_prompt",""),          key="is_neg")
        isp["custom_instructions"] = st.text_area("Custom Instructions",  value=isp.get("custom_instructions",""), height=60, key="is_cust")

    # Video Specs
    with st.expander("🎬 Video Specs"):
        vsp = S["video"]
        for key in ["duration","motion_style","camera_movement","subject_motion","cinematic_style","resolution","motion_intensity"]:
            opts = VIDEO_SPECS.get(key, [])
            cur  = vsp.get(key, opts[0])
            idx  = opts.index(cur) if cur in opts else 0
            vsp[key] = st.selectbox(key.replace("_"," ").title(), opts, index=idx, key=f"vs_{key}")
        vsp["additional_instructions"] = st.text_area("Additional Instructions", value=vsp.get("additional_instructions",""), height=60, key="vs_add")

    # Model Selection
    with st.expander("🤖 Model Selection"):
        tm_opts = list(TEXT_MODELS.keys())
        cur_tm  = S.get("text_model", tm_opts[0])
        S["text_model"]  = st.selectbox("Text Model",  [TEXT_MODELS[k] for k in tm_opts],
                           index=tm_opts.index(cur_tm) if cur_tm in tm_opts else 0, key="mdl_txt")
        S["text_model"]  = tm_opts[[TEXT_MODELS[k] for k in tm_opts].index(S["text_model"])]

        im_opts = list(IMAGE_MODELS.keys())
        S["image_model"] = st.selectbox("Image Model", list(IMAGE_MODELS.values()), key="mdl_img")
        S["image_model"] = im_opts[[IMAGE_MODELS[k] for k in im_opts].index(S["image_model"])]

        vm_opts = list(VIDEO_MODELS.keys())
        cur_vm  = S.get("video_model", vm_opts[0])
        S["video_model"] = st.selectbox("Video Model", [VIDEO_MODELS[k] for k in vm_opts],
                           index=vm_opts.index(cur_vm) if cur_vm in vm_opts else 0, key="mdl_vid")
        S["video_model"] = vm_opts[[VIDEO_MODELS[k] for k in vm_opts].index(S["video_model"])]

    # Social Platforms
    with st.expander("📱 Social Platforms"):
        sel = []
        for pid, pcfg in SOCIAL_PLATFORMS.items():
            checked = pid in S.get("platforms", [pcfg["default_enabled"]])
            if st.checkbox(pcfg["label"], value=checked, key=f"plat_{pid}"):
                sel.append(pid)
        S["platforms"] = sel

    # Branding
    with st.expander("🎨 Branding"):
        br = S["brand"]
        br["brand_name"]       = st.text_input("Brand Name",      value=br.get("brand_name",""),      key="br_name")
        br["brand_colors"]     = st.text_input("Brand Colors (hex)", value=br.get("brand_colors",""), key="br_col")
        br["brand_guidelines"] = st.text_area("Brand Guidelines", value=br.get("brand_guidelines",""), height=68, key="br_guide")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Generation buttons
    gen_all  = st.button("✦  Generate Campaign", type="primary", use_container_width=True)
    c1, c2, c3 = st.columns(3)
    gen_text  = c1.button("Text",  use_container_width=True)
    gen_image = c2.button("Image", use_container_width=True)
    gen_video = c3.button("Video", use_container_width=True)

    # Status card
    u = st.session_state.results
    if u.get("tg") and u.get("im"):
        gt = st.session_state.gen_time or "—"
        st.markdown(f"""
        <div class="sc">
          <div style="font-size:20px">✅</div>
          <div>
            <div style="font-size:12px;font-weight:600;color:#34D399">Suite Generated</div>
            <div style="font-size:11px;color:#10B981">Completed in {gt}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Nav
    nav = [("📝","Tagline","tg"),("📖","Blog","bl"),("💬","Social","sc"),("🖼️","Image","im"),("🎬","Video","vd")]
    st.markdown('<div style="padding:10px 14px 2px"><div class="sb-sec">Sections</div></div>', unsafe_allow_html=True)
    for icon, label, key in nav:
        done = u.get(key)
        tick = "✓ " if done else ""
        st.markdown(f'<div class="nav-item"><div class="nav-icon">{icon}</div><span>{tick}{label}</span></div>', unsafe_allow_html=True)

# ── Trigger generation ─────────────────────────────────────────────────────────
if gen_all:   run_generation({"all"})
if gen_text:  run_generation({"text"})
if gen_image: run_generation({"image"})
if gen_video: run_generation({"video"})


# ── Error toasts ───────────────────────────────────────────────────────────────
for asset, msg in st.session_state.errors:
    st.markdown(f"""
    <div class="et">
      <div style="font-size:18px">⚠️</div>
      <div>
        <div style="font-size:12px;font-weight:600;color:#F87171">{asset} could not be created</div>
        <div style="font-size:11px;color:#FCA5A5;margin-top:2px">{msg}</div>
      </div>
    </div>""", unsafe_allow_html=True)

u   = st.session_state.results
br  = st.session_state.brief
S   = st.session_state.settings

# ── 3 columns ──────────────────────────────────────────────────────────────────
col_l, col_c, col_r = st.columns([1, 1.15, 0.95], gap="medium")

# ── LEFT COLUMN ────────────────────────────────────────────────────────────────
with col_l:
    st.markdown('<div class="st"><span>📋</span> Campaign Brief</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
      <div class="lo">Product</div>
      <div style="font-size:18px;font-weight:700;color:#F1F5F9;margin-bottom:10px">{br.get('product_name','—')}</div>
      <div class="lo">Audience</div>
      <div style="font-size:13px;color:#CBD5E1;margin-bottom:10px">{br.get('target_audience','—')}</div>
      <div class="lo">Goal</div>
      <div style="font-size:13px;color:#CBD5E1;margin-bottom:10px">{br.get('campaign_goal','—')}</div>
      <div style="display:flex;gap:6px;flex-wrap:wrap">
        <span class="badge bgt">{br.get('brand_tone','—')}</span>
        <span class="badge bg">{br.get('language','—')}</span>
        <span class="badge bg">{br.get('target_region','—')}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Prompt Engineering
    with st.expander("⚙️ Prompt Engineering"):
        ov = st.session_state.prompt_overrides
        tg_sys, tg_usr = build_tagline_prompt(br, S["text"])
        img_p = build_image_prompt(br, S["image"])
        vid_p = build_video_prompt(br, S["video"])

        st.markdown("**Tagline Prompt**")
        ov["tagline_user"] = st.text_area("Edit tagline prompt", value=ov.get("tagline_user", tg_usr), height=80, key="pe_tg", label_visibility="collapsed")
        st.markdown("**Image Prompt**")
        ov["image_prompt"] = st.text_area("Edit image prompt", value=ov.get("image_prompt", img_p), height=80, key="pe_img", label_visibility="collapsed")
        st.markdown("**Video Prompt**")
        st.code(vid_p, language=None)

        if st.session_state.prompt_history:
            st.markdown("**Recent Prompts**")
            for h in st.session_state.prompt_history[:5]:
                st.markdown(f'<div style="font-size:11px;color:#475569;margin-bottom:4px">{h["time"]} · {h["product"]}</div>', unsafe_allow_html=True)

    # Campaign History
    with st.expander("🕘 Campaign History"):
        camps = st.session_state.campaigns
        if not camps:
            st.markdown('<div style="font-size:12px;color:#475569">No campaigns yet.</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("Search", placeholder="Filter by product…", key="hist_search", label_visibility="collapsed")
            for i, c in enumerate(camps):
                pname = c["brief"].get("product_name","")
                if search and search.lower() not in pname.lower():
                    continue
                col_a, col_b = st.columns([3,1])
                col_a.markdown(f'<div style="font-size:12px;color:#94A3B8">{c["time"]} · {pname}</div>', unsafe_allow_html=True)
                if col_b.button("Load", key=f"load_{i}"):
                    st.session_state.brief   = dict(c["brief"])
                    st.session_state.results = dict(c["results"])
                    st.session_state.analytics = dict(c.get("analytics",{}))
                    st.rerun()


# ── CENTER COLUMN ──────────────────────────────────────────────────────────────
with col_c:
    st.markdown('<div class="st"><span>📄</span> Text Assets</div>', unsafe_allow_html=True)

    # Tagline
    tg = u.get("tg")
    st.markdown(f"""
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div class="lo">Campaign Tagline</div>
        {"<span class='badge bgg'>✓ Ready</span>" if tg and "[Error" not in str(tg) else ""}
      </div>
      <div class="tg">{tg if tg and "[Error" not in str(tg) else '<span style="color:#334155">Tagline will appear here…</span>'}</div>
    </div>""", unsafe_allow_html=True)
    if tg and "[Error" not in str(tg):
        c1, c2 = st.columns(2)
        if c1.button("📋 Copy Tagline", key="cp_tg"):
            st.toast("Tagline copied!", icon="✓")
        if c2.button("🔄 Regenerate", key="rg_tg"):
            run_generation({"text"})

    # Blog
    bl = u.get("bl")
    wc = len(bl.split()) if bl and "[Error" not in str(bl) else 0
    st.markdown(f"""
    <div class="card">
      <div class="lo">Blog Introduction</div>
      <div style="font-size:13px;color:#CBD5E1;line-height:1.7;margin-top:6px">
        {bl if bl and "[Error" not in str(bl) else '<span style="color:#334155">Blog content will appear here…</span>'}
      </div>
      {"" if not bl or "[Error" in str(bl) else f'<div class="cf"><span class="badge bg">📝 {wc} words</span><span class="badge bgt">{br.get("brand_tone","")}</span></div>'}
    </div>""", unsafe_allow_html=True)
    if bl and "[Error" not in str(bl):
        c1, c2, c3 = st.columns(3)
        if c1.button("📋 Copy", key="cp_bl"): st.toast("Blog copied!", icon="✓")
        if c2.download_button("⬇ .txt", bl.encode(), "blog.txt", "text/plain", key="dl_bl"): pass
        if c3.button("🔄 Regen", key="rg_bl"): run_generation({"text"})

    # Social Posts
    sc = u.get("sc")
    platforms_sel = S.get("platforms", [])
    if sc and isinstance(sc, dict):
        st.markdown("""<div class="card">""", unsafe_allow_html=True)
        st.markdown('<div class="lo">Social Media Posts</div>', unsafe_allow_html=True)
        # platform chips
        chips_html = "".join(
            f'<span class="badge {"bgtw" if p in ("twitter","linkedin") else "bgi" if p=="instagram" else "bgl"}">{SOCIAL_PLATFORMS[p]["label"]}</span> '
            for p in platforms_sel if p in sc
        )
        st.markdown(f'<div style="display:flex;gap:5px;flex-wrap:wrap;margin:6px 0 12px">{chips_html}</div>', unsafe_allow_html=True)

        for p in platforms_sel:
            if p not in sc: continue
            cfg = SOCIAL_PLATFORMS[p]
            txt = str(sc.get(p, ""))
            badge_cls = "bgtw" if p in ("twitter","linkedin") else "bgi" if p == "instagram" else "bgl"
            st.markdown(f'<div style="font-size:11px;font-weight:600;color:{cfg["color"]};margin-bottom:4px">{cfg["label"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="pc">{txt}</div>', unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            if cc1.button(f"📋 Copy", key=f"cp_sc_{p}"): st.toast(f"{cfg['label']} copied!", icon="✓")
            cc2.markdown(f'<span class="badge {badge_cls}">{len(txt)}c</span>', unsafe_allow_html=True)

        tw_len = len(str(sc.get("twitter","")))
        st.markdown(f'<div class="cf"><span class="badge bgtw">𝕏 {tw_len}c</span><span class="badge bgg">✓ JSON Parsed</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🔄 Regenerate Social", key="rg_sc"): run_generation({"text"})
    else:
        st.markdown("""
        <div class="card">
          <div class="lo">Social Media Posts</div>
          <div style="font-size:12px;color:#334155;margin-top:6px">Social posts will appear here…</div>
        </div>""", unsafe_allow_html=True)


# ── RIGHT COLUMN ───────────────────────────────────────────────────────────────
with col_r:
    st.markdown('<div class="st"><span>🖼️</span> Visual Assets</div>', unsafe_allow_html=True)

    # Hero Image
    im = u.get("im")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="lo">Hero Image</div>', unsafe_allow_html=True)
    if im and os.path.isfile(str(im)):
        st.image(im, use_container_width=True)
        ar = S["image"].get("aspect_ratio","16:9")
        vs = S["image"].get("visual_style","")
        st.markdown(f'<div class="meta"><span>🎨 {vs}</span><span>📐 {ar}</span><span>🤖 Pollinations</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with open(im,"rb") as f: img_bytes = f.read()
        c1.download_button("⬇ Download", img_bytes, "hero_image.png", "image/png", key="dl_im")
        if c2.button("🔄 Regen", key="rg_im"): run_generation({"image"})
    else:
        st.markdown('<div class="iph">🖼️</div><div style="font-size:11px;color:#475569;text-align:center;margin-top:6px">Hero image will appear here</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Video
    vd = u.get("vd")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="lp">Promotional Video</div>', unsafe_allow_html=True)
    if vd and os.path.isfile(str(vd)):
        st.video(vd)
        ms = S["video"].get("motion_style","")
        dur = S["video"].get("duration","5s")
        st.markdown(f'<div class="meta"><span>🎬 {ms}</span><span>⏱ {dur}</span><span>🤖 Replicate</span></div>', unsafe_allow_html=True)
        with open(vd,"rb") as f: vd_bytes = f.read()
        st.download_button("⬇ Download", vd_bytes, "video.mp4", "video/mp4", key="dl_vd")
    else:
        if not REPLICATE_KEY:
            st.markdown("""
            <div class="vph">
              <div style="font-size:28px">🎬</div>
              <div style="color:rgba(255,255,255,.5);font-size:12px;font-weight:500;text-align:center">Add REPLICATE_API_TOKEN<br>to .env to enable video</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="vph">
              <div style="font-size:36px">▶</div>
              <div style="color:rgba(255,255,255,.6);font-size:12px">Promotional Video</div>
            </div>""", unsafe_allow_html=True)
        if st.button("🔄 Generate Video", key="rg_vd"): run_generation({"video"})
    st.markdown('</div>', unsafe_allow_html=True)

    # Analytics
    an = st.session_state.analytics
    if an.get("scores"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="lt">Campaign Analytics</div>', unsafe_allow_html=True)
        for m in ANALYTICS_METRICS:
            score = an["scores"].get(m["key"], 0)
            st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:12px;color:#94A3B8;margin-bottom:2px"><span>{m["icon"]} {m["label"]}</span><span style="color:#F1F5F9;font-weight:600">{score}</span></div>', unsafe_allow_html=True)
            st.progress(score / 100)
        if an.get("insights"):
            with st.expander("💡 AI Insights"):
                st.markdown(f'<div style="font-size:12px;color:#CBD5E1;line-height:1.6">{an["insights"]}</div>', unsafe_allow_html=True)
                if an.get("suggestions"):
                    st.markdown('<div style="font-size:11px;font-weight:600;color:#F59E0B;margin-top:8px">Suggestions</div>', unsafe_allow_html=True)
                    for s in an["suggestions"]:
                        st.markdown(f'<div style="font-size:12px;color:#94A3B8;margin-left:8px">• {s}</div>', unsafe_allow_html=True)
                if an.get("alternatives"):
                    st.markdown('<div style="font-size:11px;font-weight:600;color:#A78BFA;margin-top:8px">Alternative Directions</div>', unsafe_allow_html=True)
                    for a in an["alternatives"]:
                        st.markdown(f'<div style="font-size:12px;color:#94A3B8;margin-left:8px">→ {a}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Export
    if u:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="lt">Export Campaign</div>', unsafe_allow_html=True)
        for fmt in EXPORT_FORMATS:
            try:
                data, fname, mime = get_export_bytes(fmt, br, u, an)
                st.download_button(f"⬇ {fmt}", data, fname, mime, key=f"exp_{fmt}", use_container_width=True)
            except Exception as e:
                st.markdown(f'<div style="font-size:11px;color:#F87171">{fmt} export error: {e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
