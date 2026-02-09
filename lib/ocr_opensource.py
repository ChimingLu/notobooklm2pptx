"""
使用免費開源 OCR 的文字辨識模組
支援：Tesseract OCR 和 EasyOCR
"""

from PIL import Image
import io

def extract_text_with_tesseract(pil_image):
    """
    使用 Tesseract OCR 進行文字辨識
    """
    try:
        import pytesseract
        
        # 辨識中英文
        text = pytesseract.image_to_string(pil_image, lang='chi_tra+eng')
        
        # 取得詳細資訊（包含位置）
        data = pytesseract.image_to_data(pil_image, lang='chi_tra+eng', output_type=pytesseract.Output.DICT)
        
        # 轉換為我們的格式
        text_blocks = []
        n_boxes = len(data['text'])
        img_width, img_height = pil_image.size
        
        for i in range(n_boxes):
            if int(data['conf'][i]) > 30:  # 信心度過濾
                text = data['text'][i].strip()
                if text:
                    # 轉換座標到 0-1000 比例
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    
                    xmin = int((x / img_width) * 1000)
                    ymin = int((y / img_height) * 1000)
                    xmax = int(((x + w) / img_width) * 1000)
                    ymax = int(((y + h) / img_height) * 1000)
                    
                    text_blocks.append({
                        'text': text,
                        'box_2d': [ymin, xmin, ymax, xmax],
                        'font_size': h,  # 使用高度作為字體大小參考
                        'is_bold': False,
                        'align': 'left',
                        'color': '000000'
                    })
        
        return text_blocks
        
    except ImportError:
        print("  [錯誤] 未安裝 pytesseract。請執行: pip install pytesseract")
        print("  並下載 Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        return []
    except Exception as e:
        print(f"  [錯誤] Tesseract OCR 失敗: {e}")
        return []

# Global cache for EasyOCR reader
_easyocr_reader = None

def get_easyocr_reader():
    global _easyocr_reader
    if _easyocr_reader is None:
        import easyocr
        # Initialize reader (will download model on first use)
        # Check for CUDA availability if needed, but defaulting to CPU for broad compatibility as per original code
        _easyocr_reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)
    return _easyocr_reader

def extract_text_with_easyocr(pil_image):
    """
    使用 EasyOCR 進行文字辨識
    """
    try:
        import easyocr
        import numpy as np
        
        # 獲取 reader (使用快取)
        reader = get_easyocr_reader()
        
        # 轉換 PIL 為 numpy array
        img_array = np.array(pil_image)
        
        # 辨識
        results = reader.readtext(img_array)
        
        # 轉換為我們的格式
        text_blocks = []
        img_width, img_height = pil_image.size
        
        for (bbox, text, confidence) in results:
            if confidence > 0.3:  # 信心度過濾
                # bbox 是 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                xmin = int((min(x_coords) / img_width) * 1000)
                ymin = int((min(y_coords) / img_height) * 1000)
                xmax = int((max(x_coords) / img_width) * 1000)
                ymax = int((max(y_coords) / img_height) * 1000)
                
                height = max(y_coords) - min(y_coords)
                
                text_blocks.append({
                    'text': text,
                    'box_2d': [ymin, xmin, ymax, xmax],
                    'font_size': int(height * 0.8),
                    'is_bold': False,
                    'align': 'left',
                    'color': '000000'
                })
        
        return text_blocks
        
    except ImportError:
        print("  [錯誤] 未安裝 easyocr。請執行: pip install easyocr")
        return []
    except Exception as e:
        print(f"  [錯誤] EasyOCR 失敗: {e}")
        return []

def extract_text_opensource(pil_image, engine='tesseract'):
    """
    使用開源 OCR 工具進行文字辨識
    
    Args:
        pil_image: PIL Image 物件
        engine: 'tesseract' 或 'easyocr'
    
    Returns:
        文字區塊列表
    """
    if engine == 'tesseract':
        return extract_text_with_tesseract(pil_image)
    elif engine == 'easyocr':
        return extract_text_with_easyocr(pil_image)
    else:
        print(f"  [錯誤] 不支援的引擎: {engine}")
        return []
