from iopaint.model_manager import ModelManager
import traceback

print("Checking LaMa availability...")
try:
    from iopaint.model.lama import LaMa
    print("LaMa class import: SUCCESS")
except Exception:
    traceback.print_exc()

print("\nChecking ModelManager models...")
m = ModelManager(name="cv2", device="cpu")
print("Available models:", list(m.available_models.keys()))

if "lama" in m.available_models:
    print("Lama is in available_models")
else:
    print("Lama is NOT in available_models")
