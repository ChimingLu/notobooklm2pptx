"""
圖片檔案輸入處理模組
支援 PNG / JPG / JPEG / WebP / BMP / TIFF 作為來源，
回傳與 pdf_to_images 相同格式，方便後續流程統一處理。
"""

import os
from PIL import Image

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.tif'}


def is_supported_image(path: str) -> bool:
    """判斷檔案是否為支援的圖片格式"""
    return os.path.splitext(path)[1].lower() in SUPPORTED_EXTENSIONS


def images_to_slides(image_paths: list) -> tuple:
    """
    將圖片檔案列表轉換為投影片資料。
    輸入的圖片清單應事先依檔名排序。

    回傳:
        (images, page_sizes)
        - images: list of PIL Image (RGB)
        - page_sizes: list of (width_pt, height_pt)
          以像素尺寸換算（1 pixel = 1 pt，適用於 72 dpi 基準）
    """
    images = []
    page_sizes = []

    for path in image_paths:
        try:
            img = Image.open(path).convert('RGB')
            width_px, height_px = img.size
            # 以 72 dpi 為基準，pixel 數等同於 pt 數
            page_sizes.append((float(width_px), float(height_px)))
            images.append(img)
        except Exception as e:
            print(f"  [image_processor] 無法載入圖片 {os.path.basename(path)}: {e}")

    return images, page_sizes


def collect_images_from_paths(paths: list) -> list:
    """
    從傳入的路徑列表中收集所有支援的圖片檔案。
    - 若路徑為資料夾，遞迴找出其中所有圖片並依檔名排序
    - 若路徑為檔案，直接加入
    回傳依檔名（自然排序）排列的圖片路徑列表。
    """
    collected = []

    for p in paths:
        if os.path.isdir(p):
            for fname in sorted(os.listdir(p)):
                full = os.path.join(p, fname)
                if os.path.isfile(full) and is_supported_image(full):
                    collected.append(full)
        elif os.path.isfile(p) and is_supported_image(p):
            collected.append(p)

    # 依檔名自然排序（確保 slide01 < slide02 < slide10）
    collected.sort(key=lambda x: os.path.basename(x).lower())
    return collected
