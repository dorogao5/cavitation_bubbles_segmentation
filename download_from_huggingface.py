from huggingface_hub import snapshot_download

HF_USERNAME = "ShockOfWave"
MODEL_NAME = "cavitation_bubbles_segmentation"
HF_MODEL_REPO = f"{HF_USERNAME}/{MODEL_NAME}"

def download_model(version="latest"):
    print(f"🔍 Downloading model {MODEL_NAME}, version: {version}...")
    snapshot_download(repo_id=HF_MODEL_REPO, revision=version)
    print(f"✅ Model {MODEL_NAME} (version {version}) downloaded!")

if __name__ == "__main__":
    download_model()