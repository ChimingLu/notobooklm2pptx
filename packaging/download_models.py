import os
import sys
import shutil

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.config import MODELS_DIR

def download_easyocr_model():
    print("Downloading EasyOCR models...")
    try:
        import easyocr
        # This will trigger download to the specified directory
        reader = easyocr.Reader(['ch_tra', 'en'], gpu=False, model_storage_directory=MODELS_DIR, download_enabled=True)
        print("EasyOCR models downloaded.")
    except Exception as e:
        print(f"Error downloading EasyOCR models: {e}")

def download_lama_model():
    print("Downloading Lama Cleaner model...")
    # IOPaint handles model downloading differently. 
    # Usually it downloads to cache dir (e.g. ~/.cache/torch/hub/checkpoints or similar for torch, and HF_HOME for others)
    # Since we set HF_HOME and TORCH_HOME in config.py, we need to ensure those env vars are set before importing/running.
    
    os.environ["HF_HOME"] = MODELS_DIR
    os.environ["TORCH_HOME"] = MODELS_DIR
    
    try:
        from iopaint.model_manager import ModelManager
        # Trigger download
        manager = ModelManager(name="lama", device="cpu")
        print("Lama model downloaded.")
    except BaseException as e:
        import traceback
        print("======== LAMA DOWNLOAD ERROR ========")
        print(traceback.format_exc())
        print(f"Error details: {e}")
        print("=====================================")

if __name__ == "__main__":
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        
    print(f"Models will be stored in: {MODELS_DIR}")
    
    download_easyocr_model()
    download_lama_model()
    
    # pypdfium2 handles PDF rendering, so Poppler is not required.
    
    print("\nModel preparation complete.")
    print(f"Check the directory: {MODELS_DIR}")
