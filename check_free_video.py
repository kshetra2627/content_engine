"""Utility: probe free HuggingFace Gradio spaces for video generation availability.

--- PRO ADDITION: config-driven URL list ---
Space URLs are defined in FREE_VIDEO_SPACES below — no hardcoded strings in
the logic code.  Add, remove, or override entries without touching probe logic.
"""

import requests

# ── Config: known free HuggingFace video spaces ────────────────────────────────
# Update this list freely; do NOT embed URLs inside the probe logic below.
FREE_VIDEO_SPACES: list[str] = [
    "https://r3gm-wan2-2-14b-fast-preview.hf.space",
    "https://r3gm-wan2-2-14b-preview.hf.space",
    "https://zerogpu-aoti-wan2-2-14b-fast.hf.space",
]

# Gradio API paths to probe (method, path)
_PROBE_ENDPOINTS: list[tuple[str, str]] = [
    ("GET",  "/api/predict/"),
    ("GET",  "/gradio_api/api"),
    ("GET",  "/gradio_api/api/predict/"),
    ("GET",  "/api"),
    ("POST", "/predict"),
]


def probe_spaces(spaces: list[str] = FREE_VIDEO_SPACES,
                 timeout: int = 10) -> dict[str, list[dict]]:
    """Probe each space and return a dict mapping base_url → list of results."""
    results: dict[str, list[dict]] = {}
    for base in spaces:
        print(f"\n=== Testing {base} ===")
        space_results: list[dict] = []
        for method, path in _PROBE_ENDPOINTS:
            url = f"{base}{path}"
            try:
                if method == "GET":
                    r = requests.get(url, timeout=timeout)
                else:
                    r = requests.post(url, json={"data": ["test"]}, timeout=timeout)
                snippet = r.text[:150] if r.status_code == 200 else ""
                print(f"  {method} {path}: {r.status_code}{('  ' + snippet) if snippet else ''}")
                space_results.append({"method": method, "path": path,
                                       "status": r.status_code, "snippet": snippet})
            except requests.Timeout:
                print(f"  {method} {path}: Timeout")
                space_results.append({"method": method, "path": path, "status": "timeout"})
            except Exception as e:
                print(f"  {method} {path}: {type(e).__name__}")
                space_results.append({"method": method, "path": path, "status": str(type(e).__name__)})
        results[base] = space_results
    return results


if __name__ == "__main__":
    probe_spaces()
