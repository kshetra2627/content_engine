"""Check free video generation options via Gradio Spaces."""
import requests

# Try Wan2.2 Gradio Space API
spaces = [
    "https://r3gm-wan2-2-14b-fast-preview.hf.space",
    "https://r3gm-wan2-2-14b-preview.hf.space",
    "https://zerogpu-aoti-wan2-2-14b-fast.hf.space",
]

for base in spaces:
    print(f"\n=== Testing {base} ===")
    # Test various Gradio API endpoints
    endpoints = [
        ("/api/predict/", "GET"),
        ("/gradio_api/api", "GET"),
        ("/gradio_api/api/predict/", "GET"),
        ("/api", "GET"),
        ("/predict", "POST"),
    ]
    for path, method in endpoints:
        url = f"{base}{path}"
        try:
            if method == "GET":
                r = requests.get(url, timeout=10)
            else:
                r = requests.post(url, json={"data": ["test"]}, timeout=10)
            print(f"  {method} {path}: {r.status_code}", end="")
            if r.status_code == 200:
                print(f"  {r.text[:150]}")
            else:
                print()
        except requests.Timeout:
            print(f"  {method} {path}: Timeout")
        except Exception as e:
            print(f"  {method} {path}: {type(e).__name__}")