"""
統一設定模組
集中管理 API 模型名稱、重試參數等設定
"""

# Gemini API 模型設定
MODEL_IMAGE_GEN = "gemini-2.0-flash"  # 圖片生成模型 (支援 responseModalities: ["IMAGE"])
MODEL_OCR = "gemini-2.0-flash"  # OCR 文字辨識模型

# API 重試設定
MAX_RETRIES = 6
RETRY_DELAYS = [1, 2, 4, 8, 16, 32]  # 指數退避延遲（秒）

# PPTX 輸出設定
DEFAULT_SLIDE_WIDTH_INCHES = 13.333  # 16:9 寬螢幕
DEFAULT_SLIDE_HEIGHT_INCHES = 7.5
DEFAULT_FONT_SIZE = 12

# PDF 處理設定
DEFAULT_PDF_DPI = 100  # PDF 轉圖片的 DPI

# 輸出路徑設定
import os
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")  # 輸出資料夾路徑

def ensure_output_dir():
    """確保輸出資料夾存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    return OUTPUT_DIR

def get_output_path(filename):
    """取得完整的輸出檔案路徑"""
    ensure_output_dir()
    return os.path.join(OUTPUT_DIR, filename)

# 圖片清理設定
IMAGE_CLEAN_PROMPT = (
    "Please remove all main text from this image and output a clean background version. "
    "Fill gaps naturally with background texture or context. "
    "IMPORTANT: Also remove the 'NotebookLM' logo and watermark text typically found "
    "in the bottom right corner of the image."
)

# OCR 提示詞設定
OCR_BASE_PROMPT = (
    "請辨識圖片中所有文字。回傳 JSON ARRAY，每個物件包含："
    "text, box_2d [ymin, xmin, ymax, xmax], font_size, is_bold, align, color。"
    "座標比例 0-1000。"
)

OCR_NOTEBOOKLM_PROMPT = (
    " 【最佳化指令】來源文件為 NotebookLM 生成之 PDF。"
    "請特別注意處理雙欄位排版與標題層級。"
    "若有右下角的 'NOTEBOOKLM' 水印字樣，請務必辨識並精確標註位置。"
)

OCR_IGNORE_WATERMARK_PROMPT = " 請忽略右下角常見的 'NOTEBOOKLM' 水印文字。"

OCR_PRECISION_MODE_PROMPT = " 採取「逐行掃描模式」極其精確地辨識每一行。"

OCR_PARAGRAPH_MODE_PROMPT = " 採取「段落辨識模式」，將視覺上屬於同一段落的文字內容合併。"
