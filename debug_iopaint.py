from iopaint.model_manager import ModelManager
import sys

print("Python executable:", sys.executable)
try:
    print("Attempting to load Lama model...")
    model = ModelManager(name="lama", device="cpu")
    print("Lama model loaded successfully!")
except Exception as e:
    print(f"Error loading Lama: {e}")

try:
    print("Attempting to load cv2 model...")
    model = ModelManager(name="cv2", device="cpu")
    print("cv2 model loaded successfully!")
except Exception as e:
    print(f"Error loading cv2: {e}")
