"""
使用 Lama Cleaner (IOPaint) 進行圖片清理
專業級文字移除和背景修復
"""

from PIL import Image, ImageDraw
import numpy as np
import io
import lib.config


def create_text_mask_from_ocr(pil_image, text_blocks, expand_pixels=15):
    """
    根據 OCR 結果建立文字遮罩，並使用形態學膨脹確保邊緣覆蓋完整。

    Args:
        pil_image: PIL Image 物件
        text_blocks: OCR 辨識的文字區塊列表
        expand_pixels: 矩形邊界擴大像素數（預設 15，比原本 5 大以改善邊緣殘留）

    Returns:
        PIL Image (遮罩，白色=要移除的區域)
    """
    import cv2

    mask = Image.new('L', pil_image.size, 0)
    draw = ImageDraw.Draw(mask)

    img_width, img_height = pil_image.size

    for block in text_blocks:
        if 'box_2d' not in block:
            continue
        box = block['box_2d']  # [ymin, xmin, ymax, xmax]，0-1000 比例

        ymin = int((box[0] / 1000) * img_height)
        xmin = int((box[1] / 1000) * img_width)
        ymax = int((box[2] / 1000) * img_height)
        xmax = int((box[3] / 1000) * img_width)

        # 初步矩形擴大
        ymin = max(0, ymin - expand_pixels)
        xmin = max(0, xmin - expand_pixels)
        ymax = min(img_height, ymax + expand_pixels)
        xmax = min(img_width, xmax + expand_pixels)

        draw.rectangle([xmin, ymin, xmax, ymax], fill=255)

    # 形態學膨脹：進一步圓滑遮罩邊緣，減少尖角殘留
    mask_np = np.array(mask)
    kernel_size = max(3, expand_pixels)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    mask_np = cv2.dilate(mask_np, kernel, iterations=1)

    return Image.fromarray(mask_np)


# Global cache for Lama models
_lama_models = {}
_failed_models = set()


def get_lama_model(model_name):
    global _lama_models, _failed_models

    if model_name in _failed_models:
        return None

    if model_name not in _lama_models:
        try:
            from iopaint.model_manager import ModelManager

            print(f"  [Lama] 正在載入模型: {model_name}...")

            try:
                _lama_models[model_name] = ModelManager(name=model_name, device="cpu")
            except Exception as e:
                if model_name == 'lama':
                    print(f"  [Lama] ModelManager 失敗，嘗試直接載入: {e}")
                    try:
                        from iopaint.model.lama import LaMa

                        class LaMaWrapper:
                            def __init__(self):
                                self.model = LaMa(device="cpu")

                            def __call__(self, image, mask, config):
                                return self.model.forward(image, mask, config)

                        _lama_models[model_name] = LaMaWrapper()
                        print("  [Lama] 直接載入成功！")
                    except Exception as direct_e:
                        print(f"  [Lama] 直接載入也失敗: {direct_e}")
                        raise e
                else:
                    raise e

        except Exception as e:
            print(f"  [Lama] 模型載入失敗: {e}")
            _failed_models.add(model_name)
            return None

    return _lama_models[model_name]


def clean_image_with_lama(pil_image, mask, model_name='lama'):
    """
    使用 Lama Cleaner 移除圖片中的文字。

    改善策略：
    - 使用 HDStrategy.CROP 對高解析度圖片分區處理，比 ORIGINAL 效果更好
    - crop_trigger_size=1280：裁切區域小於此值時以原始解析度修復
    - crop_margin=128：提供足夠的上下文讓 Lama 更準確地填補背景

    Args:
        pil_image: PIL Image 物件
        mask: PIL Image 遮罩（白色=要移除）
        model_name: 模型名稱

    Returns:
        處理後的 PIL Image 或 None
    """
    global _failed_models

    if model_name in _failed_models and model_name != 'cv2':
        return _fallback_cv2_inpaint(pil_image, mask)

    try:
        from iopaint.schema import InpaintRequest, HDStrategy

        model = get_lama_model(model_name)
        if model is None:
            raise RuntimeError(f"無法載入模型: {model_name}")

        image_np = np.array(pil_image)
        mask_np = np.array(mask)

        # 依圖片大小選擇最佳策略
        img_w, img_h = pil_image.size
        if max(img_w, img_h) > 1024:
            # 大圖：CROP 策略，對每個文字區塊分別以高解析度修復
            config = InpaintRequest(
                hd_strategy=HDStrategy.CROP,
                hd_strategy_crop_margin=128,       # 給足夠的上下文
                hd_strategy_crop_trigger_size=1280, # 大於此值才縮圖
                hd_strategy_resize_limit=2048,
            )
            print(f"  [Lama] 大圖模式（CROP策略），圖片尺寸: {img_w}x{img_h}")
        else:
            # 小圖：直接以原始解析度處理
            config = InpaintRequest(
                hd_strategy=HDStrategy.ORIGINAL,
                hd_strategy_crop_margin=64,
                hd_strategy_crop_trigger_size=800,
                hd_strategy_resize_limit=1024,
            )

        result_np = model(image_np, mask_np, config)

        # IOPaint 回傳 BGR，需轉回 RGB
        if len(result_np.shape) == 3 and result_np.shape[2] == 3:
            import cv2
            result_np = cv2.cvtColor(result_np, cv2.COLOR_BGR2RGB)

        return Image.fromarray(result_np)

    except ImportError:
        print("  [錯誤] 未安裝 iopaint。請執行: pip install iopaint")
        return None
    except Exception as e:
        if model_name not in _failed_models:
            print(f"  [錯誤] Lama Cleaner 失敗: {e}")
            print("  [提示] 切換至 OpenCV 備援模式...")
        return _fallback_cv2_inpaint(pil_image, mask)


def _fallback_cv2_inpaint(pil_image, mask):
    """
    OpenCV Inpainting 備援方案（當 Lama 不可用時）。
    使用 Navier-Stokes 演算法（INPAINT_NS），適合較小的文字遮罩。
    """
    try:
        import cv2
        image_np = np.array(pil_image)
        mask_np = np.array(mask)

        # 確保遮罩為 uint8
        if mask_np.dtype != np.uint8:
            mask_np = mask_np.astype(np.uint8)

        # INPAINT_TELEA 對文字修復效果通常優於 INPAINT_NS
        result_np = cv2.inpaint(image_np, mask_np, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
        print("  [cv2] OpenCV Inpainting 完成")
        return Image.fromarray(result_np)
    except Exception as e:
        print(f"  [cv2] OpenCV 備援也失敗: {e}")
        return None


def clean_image_lama_auto(pil_image, ocr_engine='easyocr', model_name='lama', expand_pixels=15, mask_min_confidence=0.1):
    """
    自動偵測文字並使用 Lama Cleaner 清理。

    流程：
    1. 使用低信心度門檻（預設 0.1）的 OCR 偵測所有可能的文字位置（用於建立遮罩）
    2. 形態學膨脹遮罩，確保文字邊緣完整覆蓋
    3. Lama Cleaner 修復（大圖用 CROP 策略）

    注意：遮罩用 OCR 使用 min_confidence（比 PPTX 文字框用的 0.3 更寬鬆），
    目的是確保遮罩覆蓋率最大化，即使有誤判也無妨，因為 Lama 會以背景填補。

    Args:
        pil_image: PIL Image 物件
        ocr_engine: OCR 引擎
        model_name: Lama 模型名稱
        expand_pixels: 遮罩擴大像素（預設 15）
        mask_min_confidence: 遮罩辨識的信心度門檻（預設 0.1）

    Returns:
        處理後的 PIL Image 或 None
    """
    try:
        # 使用低門檻偵測更多文字（遮罩用途，不影響 PPTX 文字框品質）
        print(f"  [1/3] OCR 偵測文字位置（遮罩模式，門檻 {mask_min_confidence}）...")
        from lib.ocr_opensource import extract_text_opensource

        text_blocks = extract_text_opensource(pil_image, engine=ocr_engine, min_confidence=mask_min_confidence)

        if not text_blocks:
            print("  [警告] 未偵測到文字，返回原圖")
            return pil_image

        print(f"  [OCR] 偵測到 {len(text_blocks)} 個文字區塊")

        print("  [2/3] 建立遮罩（含形態學膨脹）...")
        mask = create_text_mask_from_ocr(pil_image, text_blocks, expand_pixels)

        print("  [3/3] Lama Cleaner 修復...")
        result = clean_image_with_lama(pil_image, mask, model_name)

        return result if result else pil_image

    except Exception as e:
        print(f"  [錯誤] 自動清理失敗: {e}")
        return None
