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
import os
import sys

# 資源路徑設定 (支援 PyInstaller)
def get_resource_path(relative_path):
    """取得資源的絕對路徑，支援開發環境與 PyInstaller 打包環境"""
    try:
        # PyInstaller 建立的臨時資料夾
        base_path = sys._MEIPASS
    except Exception:
        # 開發環境：專案根目錄 (lib 的上一層)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

# 模型存放與環境變數設定 (強制離線模式)
MODELS_DIR = get_resource_path("models")
if not os.path.exists(MODELS_DIR):
    # 如果是開發環境且目錄不存在，也不要報錯，讓它自動建立或由使用者建立
    # 在打包環境中，這裡應該是唯讀的，但 PyInstaller 會解壓到臨時目錄，是可讀寫的嗎？
    # 通常 _MEIPASS 是唯讀的，但我們只需要讀取。
    # 如果需要下載，應該在打包前完成。
    # 這裡我們嘗試建立 (針對開發環境)
    try:
        os.makedirs(MODELS_DIR, exist_ok=True)
    except Exception:
        pass

# 設定環境變數，引導庫使用我們的模型目錄
os.environ["HF_HOME"] = MODELS_DIR
os.environ["TORCH_HOME"] = MODELS_DIR
# EasyOCR 的 model_storage_directory 會在呼叫時傳入，但也可以設個變數方便參照

# 輸出路徑設定
# 預設輸出到使用者的「文件」資料夾下的 NotebookLM2PPTX_Output，避免權限問題
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "NotebookLM2PPTX_Output")
OUTPUT_DIR = DEFAULT_OUTPUT_DIR

def set_output_dir(path):
    """設定輸出的資料夾路徑"""
    global OUTPUT_DIR
    OUTPUT_DIR = path
    ensure_output_dir()

def ensure_output_dir():
    """確保輸出資料夾存在"""
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except OSError as e:
            print(f"Error creating output directory {OUTPUT_DIR}: {e}")
            # Fallback to temp if documents fails? No, let it fail explicitly or handle in GUI.
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
