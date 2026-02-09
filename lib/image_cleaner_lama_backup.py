"""
使用 Lama Cleaner (IOPaint) 進行圖片清理
專業級文字移除和背景修復
"""

from PIL import Image, ImageDraw
import numpy as np
import io

def create_text_mask_from_ocr(pil_image, text_blocks, expand_pixels=5):
    """
    根據 OCR 結果建立文字遮罩
    
    Args:
        pil_image: PIL Image 物件
        text_blocks: OCR 辨識的文字區塊列表
        expand_pixels: 擴大遮罩邊界（避免殘留）
    
    Returns:
        PIL Image (遮罩，白色=要移除的區域)
    """
    # 建立黑色遮罩
    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)
    
    img_width, img_height = pil_image.size
    
    for block in text_blocks:
        if 'box_2d' in block:
            # box_2d 格式: [ymin, xmin, ymax, xmax] (0-1000 比例)
            box = block['box_2d']
            
            # 轉換為像素座標
            ymin = int((box[0] / 1000) * img_height)
            xmin = int((box[1] / 1000) * img_width)
            ymax = int((box[2] / 1000) * img_height)
            xmax = int((box[3] / 1000) * img_width)
            
            # 擴大邊界
            ymin = max(0, ymin - expand_pixels)
            xmin = max(0, xmin - expand_pixels)
            ymax = min(img_height, ymax + expand_pixels)
            xmax = min(img_width, xmax + expand_pixels)
            
            # 繪製白色矩形（要移除的區域）
            draw.rectangle([xmin, ymin, xmax, ymax], fill=255)
    
    return mask

# Global cache for Lama models
_lama_models = {}

def get_lama_model(model_name):
    global _lama_models
    if model_name not in _lama_models:
        from iopaint.model_manager import ModelManager
        print(f"  [Lama] 正在載入模型: {model_name} (首次需下載)...")
        _lama_models[model_name] = ModelManager(
            name=model_name,
            device="cpu"  # Default to CPU
        )
    return _lama_models[model_name]

def clean_image_with_lama(pil_image, mask, model_name='lama'):
    """
    使用 Lama Cleaner 移除圖片中的文字
    
    Args:
        pil_image: PIL Image 物件
        mask: PIL Image 遮罩（白色=要移除）
        model_name: 模型名稱 ('lama', 'ldm', 'zits', 'mat')
    
    Returns:
        處理後的 PIL Image 或 None
    """
    try:
        from iopaint.schema import InpaintRequest, HDStrategy, LDMSampler
        
        # 取得模型 (使用快取)
        model = get_lama_model(model_name)
        
        # 轉換為 numpy array
        image_np = np.array(pil_image)
        mask_np = np.array(mask)
        
        # 設定修復參數
        config = InpaintRequest(
            hd_strategy=HDStrategy.ORIGINAL,  # 保持原始解析度
            hd_strategy_crop_margin=32,
            hd_strategy_crop_trigger_size=512,
            hd_strategy_resize_limit=512,
        )
        
        # 執行修復
        # print(f"  [Lama] 處理中...") # Reduce log noise
        result_np = model(image_np, mask_np, config)
        
        # 轉回 PIL Image
        result = Image.fromarray(result_np)
        
        # print(f"  [Lama] ✓ 完成") # Reduce log noise
        return result
        
    except ImportError:
        print("  [錯誤] 未安裝 iopaint。請執行: pip install iopaint")
        return None
    except Exception as e:
        print(f"  [錯誤] Lama Cleaner 失敗: {e}")
        if model_name != 'cv2':
            print(f"  [提示] 嘗試切換至基本修復模式 (cv2)...")
            return clean_image_with_lama(pil_image, mask, model_name='cv2')
        return None

def clean_image_lama_auto(pil_image, ocr_engine='easyocr', model_name='lama', expand_pixels=5):
    """
    自動檢測文字並使用 Lama Cleaner 清理
    
    Args:
        pil_image: PIL Image 物件
        ocr_engine: OCR 引擎 ('easyocr' 或 'tesseract')
        model_name: Lama 模型名稱
        expand_pixels: 遮罩擴大像素
    
    Returns:
        處理後的 PIL Image 或 None
    """
    try:
        # 1. OCR 檢測文字位置
        print(f"  [1/3] OCR 檢測文字位置...")
        from lib.ocr_opensource import extract_text_opensource
        
        text_blocks = extract_text_opensource(pil_image, engine=ocr_engine)
        
        if not text_blocks:
            print(f"  [警告] 未檢測到文字，返回原圖")
            return pil_image
        
        print(f"  [OCR] 檢測到 {len(text_blocks)} 個文字區塊")
        
        # 2. 建立遮罩
        print(f"  [2/3] 建立文字遮罩...")
        mask = create_text_mask_from_ocr(pil_image, text_blocks, expand_pixels)
        
        # 3. Lama 修復
        print(f"  [3/3] Lama Cleaner 修復...")
        result = clean_image_with_lama(pil_image, mask, model_name)
        
        return result if result else pil_image
        
    except Exception as e:
        print(f"  [錯誤] 自動清理失敗: {e}")
        return None
