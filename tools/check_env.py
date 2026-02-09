import flet as ft
import inspect

print(f"Flet version: {ft.version}")
try:
    print(f"FilePicker args: {inspect.signature(ft.FilePicker)}")
except Exception as e:
    print(f"Could not inspect FilePicker: {e}")

try:
    fp = ft.FilePicker()
    print("FilePicker instantiated successfully via default constructor.")
    if hasattr(fp, 'on_result'):
        print("FilePicker has on_result property.")
    else:
        print("FilePicker does NOT have on_result property.")
except Exception as e:
    print(f"FilePicker instantiation failed: {e}")
