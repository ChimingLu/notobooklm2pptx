# NotebookLM PDF 轉 PPTX 工具 (完全免費版)

將 NotebookLM 生成的 PDF 轉換為可編輯的 PowerPoint 簡報，保留原始排版和文字。

**v3.0 重大更新**：本專案已全面升級為**完全免費、本地執行版本**！不再需要 Google API Key，也沒有任何使用配額限制。

## ⭐ 特色

- **💰 完全免費**: 無 API 配額限制，想轉多少頁就轉多少頁
- **🏠 本地執行**: 資料不需上傳雲端，保護隱私
- **🎨 專業級去背**: 內建 Lama Cleaner 深度學習模型，自動移除文字水印
- **📝 多語言 OCR**: 使用 EasyOCR，支援中英文精確辨識
- **🖥️ 雙介面**: 提供直覺的 GUI 視窗版與高效的 CLI 命令列版
- **📂 完整可編輯**: 生成的 PPTX 文字與背景分離，可自由編輯

## 快速開始

### 1. 安裝環境

確保您已安裝 Python 3.10+。

```powershell
# 1. 下載專案
git clone https://github.com/your-repo/notobooklm2pptx.git
cd notobooklm2pptx

# 2. 安裝依賴套件
pip install -r requirements.txt
```

> **注意**：首次執行時會自動下載必要的 AI 模型（Lama Cleaner 與 EasyOCR），約需數百 MB，請耐心等待。

### 2. 開始使用

#### 🖥️ GUI 視窗版 (推薦)

最適合一般使用者，操作直覺。

```powershell
python gui.py
```

1. 點擊「選擇 PDF 檔案」
2. 等待處理完成 (進度條會顯示狀態)
3. 完成後會顯示檔案儲存路徑

#### 💻 CLI 命令列版

適合進階使用者或批次處理。

```powershell
python main.py
```

依照螢幕提示選擇功能即可。

### 3. 進階指令工具

如果您只想使用特定功能，可以直接執行對應腳本：

| 功能 | 指令 | 特點 |
|------|------|------|
| **高品質轉換** (推薦) | `python convert_ultimate.py input.pdf` | 使用 Lama Cleaner 去背 + EasyOCR (品質最佳) |
| **快速純文字** | `python convert_free.py input.pdf` | 僅提取文字，無背景圖 (速度最快) |

## 專案結構

清理後的專案結構更加精簡：

```
notobooklm2pptx/
├── gui.py                  # 🎨 GUI 主程式 (推薦入口)
├── main.py                 # 💻 CLI 主程式
├── convert_ultimate.py     # ⭐ 高品質轉換腳本
├── convert_free.py         # ⚡ 快速純文字轉換腳本
├── requirements.txt        # 📦 專案依賴
├── lib/                    # 📚 核心功能庫
│   ├── image_cleaner_lama.py   # Lama Cleaner 去背模組
│   ├── ocr_opensource.py       # EasyOCR 辨識模組
│   ├── pdf_processor.py        # PDF 處理
│   ├── pptx_generator.py       # PPTX 生成
│   └── config.py               # 參數設定
├── tools/                  # 🛠️ 輔助工具
│   ├── verify.py               # 環境驗證腳本
│   └── autotest.py             # 自動測試腳本
├── output/                 # 📂 輸出檔案預設路徑
├── logs/                   # 📋 系統日誌
```

## 🧪 測試與驗證

為確保您的環境設定正確，我們提供了多種驗證工具：

### 1. 環境驗證
檢查所有核心模組是否可正常載入：
```powershell
python tools/verify.py
```

### 2. 自動測試
使用內建的測試腳本，自動執行 PDF 轉 PPTX 的完整流程 (預設只測試幾頁)：
```powershell
python tools/autotest.py "測試檔案.pdf"
```

## 📊 效能基準

本地執行的速度取決於您的 CPU/GPU 效能。以下為預期處理時間（單頁）：

- **PDF 轉圖片**：< 1 秒
- **圖片去背 (Lama)**：5-15 秒 (視圖案複雜度與硬體而定)
- **文字辨識 (OCR)**：3-10 秒
- **PPTX 生成**：< 1 秒

> **💡 GPU 加速**：如果您的電腦有 NVIDIA 顯示卡並安裝了 CUDA 版本的 PyTorch，處理速度會大幅提升。

## 常見問題

### Q: 為什麼第一次執行這麼慢？
A: 首次執行需要下載 AI 模型（Lama Cleaner 和 EasyOCR），取決於網速可能需要幾分鐘。下載完成後，之後的執行就會非常快。

### Q: 支援 GPU 加速嗎？
A: 支援。如果您的電腦安裝了 CUDA 版本的 PyTorch，程式會自動使用 GPU 加速，處理速度會大幅提升。

### Q: 轉換後的文字排版有時會跑掉？
A: PDF 轉 PPTX 本身具有挑戰性。我們使用了「NotebookLM 最佳化」模式來處理雙欄排版，但複雜的版面仍可能需要您在 PowerPoint 中手動微調。

### Q: 需要 API Key 嗎？
A: **完全不需要！** 舊版依賴 Gemini API，但本版本已移除所有 API 依賴，完全本地運行。

## 授權

本專案使用多個開源組件：
- [Lama Cleaner (IOPaint)](https://github.com/Sanster/IOPaint) - Apache 2.0
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Apache 2.0
- [pypdfium2](https://github.com/pypdfium2-team/pypdfium2) - Apache 2.0 / BSD-3
- [python-pptx](https://github.com/scanny/python-pptx) - MIT License
