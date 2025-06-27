import os
import urllib.request

MODELS = {
    "GFPGANv1.3.pth": "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.3.pth",
    "wav2lip.pth": "https://storage.googleapis.com/wav2lip/wav2lip.pth",
}

os.makedirs("models", exist_ok=True)

for fname, url in MODELS.items():
    out = os.path.join("models", fname)
    if not os.path.exists(out):
        print(f"Downloading {fname}...")
        urllib.request.urlretrieve(url, out)
    else:
        print(f"{fname} already exists.")
