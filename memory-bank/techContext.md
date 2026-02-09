# Technology Context

## 核心技術

### 1. 語言與環境

*   **Python 3.10+** (目前使用 Python 3.12)
*   **PIP** 套件管理
*   **Virtualenv** 或 **Conda** 環境

### 2. 關鍵依賴

*   **`google-genai`**: ❌ 移除
*   **`python-dotenv`**: ❌ 移除
*   **`pypdfium2`**: 用於 PDF 解析為高解析度圖片 (Bitmap)。
*   **`python-pptx`**: 生成 PowerPoint 檔案，處理排版與圖層。
*   **`easyocr`**: 本地執行的高精度 OCR 文字辨識引擎，支援中英混合辨識。
*   **`iopaint` (Lama Cleaner)**: 本地執行的 AI 圖片修復模型，用於去除背景上的文字與水印。
*   **`flet`**: 基於 Flutter 的 Python GUI 框架，用於開發桌面視窗介面。
*   **`rich`, `questionary`**: 提供現代化的 CLI 互動體驗。

## 系統架構

### 核心模組 (`lib/`)

*   **`pdf_processor.py`**: 負責將 PDF 頁面轉換為 PIL Image 物件。
*   **`ocr_opensource.py`**: 封裝 EasyOCR，負責提取文字內容與位置 (bbox)。
*   **`image_cleaner_lama.py`**: 封裝 Lama Cleaner，負責去除圖片上的文字，生成乾淨背景。
*   **`pptx_generator.py`**: 將清理後的背景圖與提取的文字組合成 PPTX 檔案。
*   **`config.py`**: 集中管理全域常數與設定。

### 主程式

*   **`main.py`**: CLI 入口點，提供選單式操作。
*   **`gui.py`**: GUI 入口點，提供檔案拖放與進度顯示。
*   **`convert_ultimate.py`**: 獨立的高品質轉換腳本。
*   **`convert_free.py`**: 獨立的純文字轉換腳本。

### 數據流

1.  **Input**: PDF 檔案
2.  **Step 1 (Parse)**: `pypdfium2` -> List[Image]
3.  **Step 2 (Clean)**: `Lama Cleaner` -> List[Cleaned Background Image]
4.  **Step 3 (OCR)**: `EasyOCR` -> List[Text Block Info]
5.  **Step 4 (Gen)**: `python-pptx` -> PPTX 檔案
6.  **Output**: PPTX 檔案

## 開發環境限制

*   本地執行需要下載較大的 AI 模型 (Lama, EasyOCR)，初始啟動時間較長。
*   依賴 CPU/GPU 運算能力，處理速度受硬體限制。
*   目前僅支援 Windows 環境 (路徑處理可能需適配 Linux/Mac)。
